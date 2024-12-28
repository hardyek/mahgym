#pragma once

#include "types.hpp"
#include <string>
#include <unordered_map>

namespace t11wo4 {
    
    struct TileEncoder {
        static const std::unordered_map<Tile, std::string> to_shorthand();
        static const std::unordered_map<Wind, str::string> wind_to_string();

        static std::string tile_to_string(Tile tile);
        static std::string encode_hand(const TileList& tiles);
        static Wind index_to_wind(uint8_t index);
    }
}