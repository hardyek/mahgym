#pragma once

#include <stdexcept>
#include <string>

namespace t11w04 {

class MahjongError : public std::runtime_error {
public:
    explicit MahjongError(const std::string& msg) : std::runtime_error(msg) {}
};

class InvalidMoveError : public MahjongError {
public:
    explicit InvalidMoveError(const std::string& msg) : MahjongError(msg) {}
};

class IllegalStateError : public MahjongError {
public:
    explicit IllegalStateError(const std::string& msg) : MahjongError(msg) {}
};

}