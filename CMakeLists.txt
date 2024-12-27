cmake_minimum_required(VERSION 3.15)
project(11w04 VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(BUILD_TESTS "Build tests" ON)
option(BUILD_PYTHON_BINDINGS "Build Python bindings" ON)

# Find pybind11
find_package(pybind11 CONFIG REQUIRED)

add_subdirectory(core)