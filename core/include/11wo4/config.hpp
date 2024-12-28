#pragma once

namespace t11w04 {
namespace config {

// Hong Kong Rules
constexpr bool ALLOW_KONG_AFTER_PUNG = true;
constexpr bool ALLOW_ROBBING_KONG = true;
constexpr bool ALLOW_MELDING_OWN_DISCARD = false;
constexpr bool REQUIRE_SELF_DRAW_FOR_BONUS = true;

// HK Scoring
constexpr uint32_t MIN_FAN = 3;
constexpr uint32_t BASE_POINTS = 1000;
constexpr uint32_t SELF_DRAW_FAN = 1;
constexpr uint32_t ALL_CONCEALED_FAN = 1;
constexpr uint32_t FLOWER_POINTS = 100;
constexpr uint32_t SEASON_POINTS = 100;

// Limits
constexpr uint32_t MAX_FAN = 13;    // Maximum fan (doubles)
constexpr uint32_t LIMIT_HAND = 13;  // Fan for limit hands

// Debug/Testing
constexpr bool ENABLE_VALIDATION = true;
constexpr bool ENABLE_LOGGING = true;

}
}