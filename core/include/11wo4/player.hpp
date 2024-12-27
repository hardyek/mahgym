#pragma once

#include "types.hpp"
#include <algorithm>

namespace t11wo4 {

class Player {
public:
    explicit Player(uint8_t seat_number)
        :   seat_(seat_number)
        ,   wind_(Wind::EAST) {}
    
    void recieve(Tile tile) { 
        hand_.push_back(tile); 
    }

    Tile discard(size_t index) {
        Tile discarded = hand_[index];
        hand_.erase(hand_.begin() + index);
        return discarded;
    }

    void reveal_meld(const std::vector<Tile>& meld) {
        for (const Tile& tile : meld) {
            auto it = std::find(hand_.begin(), hand_.end(), tile);
            if (it != hand_.end()) {
                hand_.erase(it);
            }
        }
        exposed_.push_back(meld);
    }

    // getters
    const TileList& get_hand() const { return hand_; }
    const std::vector<std::vector<Tile>>& get_exposed() const { return exposed_; }
    const TileList& get_specials() const { return specials_; }
    Wind get_wind() const { return wind_; }
    uint8_t get_seat() const { return seat_; }

    // setters
    void set_wind(Wind wind) { wind_ = wind; }

    // util
    void sort_hand() {
        std::sort(hand_.begin(), hand_.end());
    }
    
private:
    uint8_t seat_;
    Wind wind_;
    TileList hand_;
    std::vector<std::vector<Tile>> exposed_;
    TileList specials_;
};

}