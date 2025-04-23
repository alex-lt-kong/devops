#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <stdexcept>
#include <random>
#include <algorithm>

struct Options {
    std::string target;
    std::size_t sizeInBytes = 0;
};

void printUsage(const char* progName) {
    std::cout << "Usage: " << progName
        << " [--target|-t] <file-path> [--size|-s] <file-size-in-bytes>"
        << std::endl;
}

Options parseArguments(int argc, char* argv[]) {
    Options opts;

    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        if (arg == "--target" || arg == "-t") {
            if (i + 1 < argc) {
                opts.target = argv[++i];
            }
            else {
                throw std::runtime_error("Error: " + arg + " flag requires an argument.");
            }
        }
        else if (arg == "--size" || arg == "-s") {
            if (i + 1 < argc) {
                try {
                    opts.sizeInBytes = std::stoull(argv[++i]);
                }
                catch (const std::exception&) {
                    throw std::runtime_error("Error: Invalid size value.");
                }
            }
            else {
                throw std::runtime_error("Error: " + arg + " flag requires an argument.");
            }
        }
    }

    if (opts.target.empty()) {
        throw std::runtime_error("Error: Target file path not specified.");
    }
    if (opts.sizeInBytes == 0) {
        throw std::runtime_error("Error: File size must be greater than 0.");
    }

    return opts;
}

int main(int argc, char* argv[]) {
    try {
        Options opts = parseArguments(argc, argv);

        const std::size_t bufferSize = 1024 * 1024 * 64;
        std::vector<char> buffer(bufferSize);
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dist(0, 255);
        std::generate(buffer.begin(), buffer.end(), [&]() { return static_cast<char>(dist(gen)); });

        std::ofstream file(opts.target, std::ios::binary);
        if (!file) {
            std::cerr << "Error: Unable to create file at " << opts.target << std::endl;
            return 1;
        }

        std::size_t writtenBytes = 0;
        while (writtenBytes < opts.sizeInBytes) {
            std::size_t chunkSize = std::min(bufferSize, opts.sizeInBytes - writtenBytes);
            file.write(buffer.data(), chunkSize);
            writtenBytes += chunkSize;
            std::cout.imbue(std::locale(""));
            std::cout << "written: " << writtenBytes << ", total: " << opts.sizeInBytes << ", progress: " << 100 * writtenBytes / opts.sizeInBytes << "%\n";
            std::cout.imbue(std::locale::classic());
        }

        file.close();
        std::cout << "File created successfully: " << opts.target << std::endl;

    }
    catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        printUsage(argv[0]);
        return 1;
    }

    return 0;
}