#include "player.hpp"
#include "errors.hpp"
#include <algorithm>

namespace t11wo4 {

Player::Player(uint8_t seat_number)
    : seat_(seat_number)
    , wind_(Wind::EAST)
{
    hand_.reserve(HAND_SIZE + 1); // +1 for potential winning hand
}

void Player::receive(Tile tile) {
    hand_.push_back(tile);
}

Tile Player::discard(size_t index) {
    if (index >= hand_.size()) {
        throw InvalidMoveError("Invalid discard index");
    }
    Tile discarded = hand_[index];
    hand_.erase(hand_.begin() + index);
    return discarded;
}

void Player::reveal_meld(const std::vector<Tile>& meld) {
    for (const Tile& tile : meld) {
        auto it = std::find(hand_.begin(), hand_.end(), tile);
        if (it != hand_.end()) {
            hand_.erase(it);
        } else {
            throw InvalidMoveError("Cannot reveal meld : tile not in hand");
        }
    }
    exposed_.push_back(meld);
}

void Player::add_special(Tile tile) {
    auto it = std::find(hand_.begin(), hand_.end(), tile);
    if (it != hand_.end()) {
        hand_.erase(it);
    } else {
        throw InvalidMoveError("Cannot add special : tile not in hand");
    }
    specials_.push_back(tile);
}

void Player::sort_hand() {
    std::sort(hand_.begin(), hand_.end());
}

}