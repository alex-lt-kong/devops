#include <algorithm>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <print>
#include <stdexcept>
#include <string>
#include <vector>

namespace fs = std::filesystem;

struct Options {
  std::string target;
  int pass_count = 1;
};

void printUsage(const char *progName) {
  std::cout
      << "Usage: " << progName
      << " [--target|-t] <file or directory> [--pass|-p] <number-of-passes>"
      << std::endl;
}

Options parseArguments(int argc, char *argv[]) {
  Options opts;

  for (int i = 1; i < argc; i++) {
    std::string arg = argv[i];
    if (arg == "--target" || arg == "-t") {
      if (i + 1 < argc) {
        opts.target = argv[++i];
      } else {
        throw std::runtime_error("Error: " + arg +
                                 " flag requires an argument.");
      }
    } else if (arg == "--pass" || arg == "-p") {
      if (i + 1 < argc) {
        try {
          opts.pass_count = std::stoi(argv[++i]);
          if (opts.pass_count < 1 || opts.pass_count > 255) {
            throw std::runtime_error(
                "Error: Number of passes must be between 1 and 255.");
          }
        } catch (const std::exception &) {
          throw std::runtime_error("Error: Invalid number for pass count.");
        }
      } else {
        throw std::runtime_error("Error: " + arg +
                                 " flag requires an argument.");
      }
    }
  }

  if (opts.target.empty()) {
    throw std::runtime_error("Error: Target not specified.");
  }

  return opts;
}

void process_file(const fs::path &file, int pass_count) {
  if (!fs::is_regular_file(file))
    return;

  // use of uintmat_t could be a trap:
  // https://thephd.dev/intmax_t-hell-c++-cc
  uintmax_t file_size = fs::file_size(file);
  std::cout.imbue(std::locale(""));
  std::cout << "Processing file: " << file << " (Size: " << std::fixed
            << file_size << " bytes)" << std::endl;
  std::cout.imbue(std::locale::classic());

  std::fstream fs(file, std::ios::in | std::ios::out | std::ios::binary);
  if (!fs) {
    std::cerr << "Error: Unable to open file " << file << std::endl;
    return;
  }

  constexpr size_t buffer_size = 4096;
  std::vector<char> buffer(buffer_size);

  for (unsigned char pass = 0; pass < pass_count; ++pass) {
    // unsigned char byteVal = static_cast<unsigned char>(pass);
    std::fill(buffer.begin(), buffer.end(), pass);

    fs.seekp(0); // Restart the file write pointer.
    uintmax_t written = 0;
    std::cout << "Pass " << (pass + 1) << ": writing byte 0x" << std::hex
              << std::setw(2) << std::setfill('0') << static_cast<int>(pass)
              << std::dec << std::endl;

    while (written < file_size) {
      auto to_write = std::min(buffer_size, file_size - written);
      fs.write(buffer.data(), to_write);
      if (!fs) {
        std::cerr << "Error: Failed to write to file " << file << std::endl;
        return;
      }
      written += to_write;
    }
    fs.flush();
  }
  fs.close();

  fs::path newPath = file.parent_path();
  std::string newName = file.filename().string() + ".done";
  // file.stem().string() + "_shredded" + file.extension().string();
  newPath /= newName;

  try {
    fs::rename(file, newPath);
    std::cout << "Renamed file: " << file.filename().string() << " -> "
              << newPath.filename().string() << std::endl;
  } catch (const fs::filesystem_error &e) {
    std::cerr << "Error renaming file " << file << " to " << newPath << ": "
              << e.what() << std::endl;
  }
}

std::vector<fs::path> getFilesInPath(const std::string &path) {
  fs::path p(path);

  if (!fs::exists(p)) {
    throw std::runtime_error("The provided path does not exist: " + path);
  }

  std::vector<fs::path> file_paths;

  if (fs::is_regular_file(p)) {
    file_paths.push_back(p);
  } else if (fs::is_directory(p)) {
    for (const auto &entry : fs::recursive_directory_iterator(p)) {
      if (fs::is_regular_file(entry.path())) {
        file_paths.push_back(entry.path());
      }
    }
  }

  else {
    throw std::runtime_error(
        "The provided path is neither a regular file nor a directory: " + path);
  }

  return file_paths;
}

int main(int argc, char *argv[]) {
  Options opts;
  try {
    opts = parseArguments(argc, argv);
  } catch (const std::exception &ex) {
    std::cerr << ex.what() << std::endl;
    printUsage(argv[0]);
    return 1;
  }

  auto file_paths = getFilesInPath(opts.target);
  for (const auto &file_path : file_paths) {
    process_file(file_path, opts.pass_count);
  }

  return 0;
}
