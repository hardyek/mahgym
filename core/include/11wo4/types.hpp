#pragma once 

#include <vector>
#include <array>
#include <cstdint>

namespace t11wo4 {

// tile type using uint8_t since only ranges from 1-42
using Tile = uint8_t;
using TileList = std::vector<Tile>;

// winds
enum class Wind : uint8_t {
    EAST = 0,
    SOUTH = 1,
    WEST = 2,
    NORTH = 3,
};

// actions
enum class Action : uint8_t {
    DISCARD,
    SOENG,
    PUNG,
    GONG,
    DRAW,
    SKIP // player can pickup but choses to draw
};

// tile categories
enum class TileCategory : uint8_t {
    NUMERIC = 0,        // 1  - 9   (9 tiles)
    CIRCLES = 1,        // 10 - 18  (9 tiles)
    BAMBOO = 2,         // 19 - 27  (9 tiles)
    WINDS = 3,          // 28 - 31  (4 tiles)
    DRAGONS = 4,        // 32 - 34  (3 tiles)
    FLOWERS = 5,        // 35 - 38  (4 tiles)
    SEASONS = 6,        // 39 - 42  (4 tiles)
};

// exposed meld types
struct Meld {
    std::vector<Tile> tiles;
    Action type;
};

// game state flags
struct StateFlags {
    bool game_over : 1;
    bool can_seong : 1;
    bool can_pung : 1;
    bool can_gong : 1;
    bool is_last_tile : 1;
};

// constants
constexpr size_t NUM_PLAYERS = 4;
constexpr size_t HAND_SIZE = 13;
constexpr size_t MAX_TILES = 144;
constexpr size_t NUM_UNIQUE_TILES = 42;

struct TileRanges {
    static constexpr Tile NUMERIC_START = 1;
    static constexpr Tile NUMERIC_END = 9;
    static constexpr Tile CIRCLES_START = 10;
    static constexpr Tile CIRCLES_END = 18;
    static constexpr Tile BAMBOO_START = 19;
    static constexpr Tile BAMBOO_END = 27;
    static constexpr Tile WINDS_START = 28;
    static constexpr Tile WINDS_END = 31;
    static constexpr Tile DRAGONS_START = 32;
    static constexpr Tile DRAGONS_END = 34;
    static constexpr Tile FLOWERS_START = 35;
    static constexpr Tile FLOWERS_END = 38;
    static constexpr Tile SEASONS_START = 39;
    static constexpr Tile SEASONS_END = 42;
};

// overall observation
struct GameObservation {
    TileList pile;
    TileList hand;
    std::vector<std::vector<Tile>> exposed;
    TileList specials;
    Wind seat_wind;
    Wind prevailing_wind;
};

}