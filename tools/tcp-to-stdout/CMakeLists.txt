cmake_minimum_required(VERSION 3.31)
project(tcp_to_stdout)

set(CMAKE_CXX_STANDARD 20)

find_package(spdlog CONFIG REQUIRED)
find_package(cxxopts CONFIG REQUIRED)

add_executable(tcp-to-stdout main.cpp)
target_link_libraries(tcp-to-stdout PRIVATE spdlog::spdlog cxxopts::cxxopts)
