cmake_minimum_required(VERSION 3.10)

project(shred-files VERSION 1.0 LANGUAGES CXX)


set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)


add_executable(shred-files shred-files.cpp)
add_executable(big-file big-file.cpp)
