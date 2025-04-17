#include <iostream>
#include <filesystem>
#include <fstream>
#include <vector>
#include <algorithm>
#include <string>
#include <cstdint>
#include <stdexcept>
#include <print>

namespace fs = std::filesystem;

struct Options {
    std::string target;
    int passCount = 1;
};

// Prints a usage message.
void printUsage(const char* progName) {
    std::cout << "Usage: " << progName 
              << " [--target|-t] <file or directory> [--pass|-p] <number-of-passes>" 
              << std::endl;
}

// Parses command-line arguments using only the standard library.
// Returns an Options struct holding the target path and pass count.
Options parseArguments(int argc, char* argv[]) {
    Options opts;
    
    // Loop over the arguments.
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        if (arg == "--target" || arg == "-t") {
            if (i + 1 < argc) {
                opts.target = argv[++i];
            } else {
                throw std::runtime_error("Error: " + arg + " flag requires an argument.");
            }
        } else if (arg == "--pass" || arg == "-p") {
            if (i + 1 < argc) {
                try {
                    opts.passCount = std::stoi(argv[++i]);
                    if (opts.passCount < 1 || opts.passCount > 255) {
                        throw std::runtime_error("Error: Number of passes must be between 1 and 255.");
                    }
                } catch (const std::exception&) {
                    throw std::runtime_error("Error: Invalid number for pass count.");
                }
            } else {
                throw std::runtime_error("Error: " + arg + " flag requires an argument.");
            }
        } else {
            // If the target isn't yet specified, assume this argument is the target path.
            if (opts.target.empty()) {
                opts.target = arg;
            }
        }
    }
    
    if (opts.target.empty()) {
        throw std::runtime_error("Error: Target not specified.");
    }
    
    return opts;
}


void processFile(const fs::path& file, int passCount) {
    if (!fs::is_regular_file(file))
        return;

    // Get the file size.
    uintmax_t fileSize = fs::file_size(file);
    std::cout << "Processing file: " << file 
              << " (Size: " << fileSize << " bytes)" << std::endl;

    // Open file for reading/writing in binary mode.
    std::fstream fileStream(file, std::ios::in | std::ios::out | std::ios::binary);
    if (!fileStream) {
        std::cerr << "Error: Unable to open file " << file << std::endl;
        return;
    }

    constexpr size_t bufferSize = 4096;
    std::vector<char> writeBuffer(bufferSize);

    for (int pass = 0; pass < passCount; ++pass) {
        unsigned char byteVal = static_cast<unsigned char>(pass);
        std::fill(writeBuffer.begin(), writeBuffer.end(), static_cast<char>(byteVal));

        fileStream.seekp(0);  // Restart the file write pointer.
        uintmax_t written = 0;
        std::cout << "Pass " << (pass + 1) 
                  << ": writing byte 0x" << std::hex << static_cast<int>(byteVal)
                  << std::dec << std::endl;

        // Write the buffer repeatedly until the entire file is overwritten.
        while (written < fileSize) {
            size_t toWrite = static_cast<size_t>(std::min<uintmax_t>(bufferSize, fileSize - written));
            fileStream.write(writeBuffer.data(), toWrite);
            if (!fileStream) {
                std::cerr << "Error: Failed to write to file " << file << std::endl;
                return;
            }
            written += toWrite;
        }
        fileStream.flush();
    }
    fileStream.close();

    // Construct a new file name by appending "_shredded" before the extension.
    fs::path newPath = file.parent_path();
    std::string newName = file.stem().string() + "_shredded" + file.extension().string();
    newPath /= newName;

    // Rename the file.
    try {
        fs::rename(file, newPath);
        std::cout << "Renamed file: " << file.filename().string() 
                  << " -> " << newPath.filename().string() << std::endl;
    } catch (const fs::filesystem_error& e) {
        std::cerr << "Error renaming file " << file << " to " 
                  << newPath << ": " << e.what() << std::endl;
    }
}

int main(int argc, char* argv[]) {
    Options opts;
    try {
        opts = parseArguments(argc, argv);
    } catch (const std::exception& ex) {
        std::cerr << ex.what() << std::endl;
        printUsage(argv[0]);
        return 1;
    }

    fs::path targetPath(opts.target);
    try {
        if (!fs::exists(targetPath)) {
            std::cerr << "Error: Path does not exist: " << targetPath << std::endl;
            return 1;
        }

        if (fs::is_regular_file(targetPath)) {
            processFile(targetPath, opts.passCount);
        } else if (fs::is_directory(targetPath)) {
            for (const auto& entry : fs::directory_iterator(targetPath)) {
                if (fs::is_regular_file(entry.status())) {
                    processFile(entry.path(), opts.passCount);
                }
            }
        } else {
            std::cerr << "Error: Unsupported file type: " << targetPath << std::endl;
            return 1;
        }
    } catch (const fs::filesystem_error& e) {
        std::cerr << "Filesystem Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
