#include <cxxopts.hpp>
#include <boost/asio.hpp>
#include <spdlog/spdlog.h>
#include <fmt/ranges.h>

#include <iostream>
#include <thread>
#include <vector>
#include <iomanip>

using namespace boost::asio;
using namespace std;

void log_received_data(int port, const char* data, size_t length) {
    stringstream hex_stream, str_stream;

    hex_stream << std::hex << std::setfill('0');

    for (size_t i = 0; i < length; ++i) {
        unsigned char c = static_cast<unsigned char>(data[i]);
        hex_stream << std::setw(2) << static_cast<int>(c) << " "; // Format as hex

        if (isprint(c)) {
            str_stream << c; // Print printable characters
        } else {
            str_stream << '.'; // Replace non-printable characters with '.'
        }
    }

    spdlog::info("Received {} bytes on port {}", length, port);
    spdlog::info("Hex   : [{}]", hex_stream.str());
    spdlog::info("String: [{}]", str_stream.str());
}

void handle_connection(ip::tcp::socket& socket, int port) {
    try {
        auto remote_endpoint = socket.remote_endpoint();
        std::string source_ip = remote_endpoint.address().to_string();
        int source_port = remote_endpoint.port();
        spdlog::info("Client {}:{} connected on port {}", source_ip, source_port, port);

        while (true) {
            char buffer[65536];
            boost::system::error_code error;
            size_t bytes_received = socket.read_some(boost::asio::buffer(buffer), error);


            if (error == error::eof) {
                spdlog::info("Connection closed on port {}", port);
                break;
            } else if (error) {
                spdlog::error("Error receiving data on port {}: {}", port, error.message());
                break;
            }
            log_received_data(port, buffer, bytes_received);
        }
    } catch (const std::exception& e) {
        spdlog::error("Connection error on port {}: {}", port, e.what());
    }
}

void listen_on_port(io_context& io_context, int port) {
    try {
        ip::tcp::acceptor acceptor(io_context, ip::tcp::endpoint(ip::tcp::v4(), port));
        //boost::asio::ip::tcp::acceptor::reuse_address option(false);
        //acceptor.set_option(option);
        spdlog::info("Listening on port {}...", port);

        while (true) {
            ip::tcp::socket socket(io_context);
            acceptor.accept(socket);
            std::thread([socket = std::move(socket), port]() mutable {
                handle_connection(socket, port);
            }).detach();
        }
    } catch (const boost::system::system_error& e) {
        if (e.code() == error::address_in_use) {
            spdlog::error("Port {} is already in use. Another instance may be listening.", port);
        } else {
            spdlog::error("Error on port {}: {}", port, e.what());
        }
    } catch (const std::exception& e) {
        spdlog::error("Error on port {}: {}", port, e.what());
    }
}

vector<int> parse_ports(const string& port_string) {
    vector<int> ports;
    stringstream ss(port_string);
    string port;

    while (getline(ss, port, ',')) {
        try {
            ports.push_back(stoi(port));  // Convert string to int
        } catch (const invalid_argument&) {
            spdlog::error("Invalid port number: {}", port);
        }
    }
    return ports;
}

int main(const int argc, char* argv[]) {
    std::vector<int> ports;
    try {
        cxxopts::Options options("TCP To Stdout", "A simple TCP server that prints whatever it receives to stdout");

        options.add_options()
            ("p,ports", "Comma-separated ports to listen on", cxxopts::value<std::vector<int>>())
            ("i,interface", "Network interface to bind to", cxxopts::value<std::string>()->default_value("0.0.0.0"))
            ("h,help", "Print usage");

        const auto result = options.parse(argc, argv);

        if (result.count("help")) {
            std::cout << options.help() << std::endl;
            return 0;
        }

        if (result.count("ports")) {
            ports = result["ports"].as<std::vector<int>>();
        } else {
            std::cerr << "Error: --ports argument is required." << std::endl;
            return 1;
        }
        auto interface = result["interface"].as<std::string>();
        spdlog::info("Listening {} on interface: {}", fmt::join(ports, ","), interface);
    }
    catch (const cxxopts::exceptions::exception& e) {
        std::cerr << "Error parsing options: " << e.what() << std::endl;
        return 1;
    }

    io_context io_context;
    vector<thread> threads;

    for (int port : ports) {
        threads.emplace_back(listen_on_port, ref(io_context), port);
    }

    for (auto& t : threads) {
        t.join();
    }

    return 0;
}