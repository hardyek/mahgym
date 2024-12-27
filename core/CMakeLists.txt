# Core library
add_library(11w04_core
    # Add your source files here as they are created
    # src/game_state.cpp
    # src/observation.cpp
    # etc...
)

target_include_directories(11w04_core
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Compiler warnings
target_compile_options(11w04_core
    PRIVATE
        $<$<CXX_COMPILER_ID:MSVC>:/W4>
        $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -Wpedantic>
)

# Python bindings
if(BUILD_PYTHON_BINDINGS)
    pybind11_add_module(11w04_python
        bindings/python/bindings.cpp
        # Add more binding files as they are created
    )

    target_link_libraries(11w04_python
        PRIVATE
            11w04_core
    )
endif()

# Tests
if(BUILD_TESTS)
    find_package(GTest REQUIRED)
    
    # C++ tests
    add_executable(11w04_tests
        # Add test files as they are created
        # tests/cpp/test_game_state.cpp
        # tests/cpp/test_observation.cpp
        # etc...
    )

    target_link_libraries(11w04_tests
        PRIVATE
            11w04_core
            GTest::GTest
            GTest::Main
    )

    add_test(NAME 11w04_tests COMMAND 11w04_tests)
endif()