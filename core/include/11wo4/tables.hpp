#pragma once

#include "types.hpp"
#include <unordered_map>
#include <array>

namespace t11w04 {

struct PatternTables {
    // Core patterns remain same
    static constexpr std::array<std::array<Tile, 3>, 21> SOENG_PATTERNS = {{
        {1, 2, 3}, {2, 3, 4}, {3, 4, 5}, {4, 5, 6}, {5, 6, 7}, {6, 7, 8}, {7, 8, 9},
        {10, 11, 12}, {11, 12, 13}, {12, 13, 14}, {13, 14, 15}, {14, 15, 16}, {15, 16, 17}, {16, 17, 18},
        {19, 20, 21}, {20, 21, 22}, {21, 22, 23}, {22, 23, 24}, {23, 24, 25}, {24, 25, 26}, {25, 26, 27}
    }};

    // HK scoring patterns
    struct HandPattern {
        uint32_t fan;            // Fan value (doubles)
        bool concealed_only;     // Must be concealed to count
        std::string name;        // Pattern name
        std::function<bool(const TileList&, const std::vector<std::vector<Tile>>&)> validator;
    };

    // Common hand patterns (Great winds, small dragons, etc)
    static const std::unordered_map<std::string, HandPattern>& get_scoring_patterns();
    
    // Points for basic patterns
    static constexpr uint32_t PUNG_POINTS[] = {
        2,  // Simple tiles
        4,  // Terminals/Honors
        8   // Concealed
    };

    static constexpr uint32_t GONG_POINTS[] = {
        8,   // Simple tiles
        16,  // Terminals/Honors
        32   // Concealed
    };

    // Validation methods
    static bool is_valid_meld(const std::vector<Tile>& tiles);
    static bool is_valid_soeng(const std::vector<Tile>& tiles);
    static bool is_valid_pung(const std::vector<Tile>& tiles);
    static bool is_valid_gong(const std::vector<Tile>& tiles);
    static bool is_valid_pair(const std::vector<Tile>& tiles);

    // HK scoring calculation
    static uint32_t calculate_hand_points(
        const TileList& hand,
        const std::vector<std::vector<Tile>>& exposed,
        Wind seat_wind,
        Wind prevailing_wind,
        bool self_drawn,
        const std::vector<Tile>& flowers
    );

private:
    static std::unordered_map<std::string, HandPattern> initialize_scoring_patterns();
    static uint32_t calculate_basic_points(const TileList& hand, const std::vector<std::vector<Tile>>& exposed);
    static uint32_t calculate_bonus_points(const std::vector<Tile>& flowers, Wind seat_wind);
};

} // namespace t11w04