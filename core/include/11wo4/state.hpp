#pragma once

#include "types.hpp"
#include "player.hpp"
#include <array>
#include <random>
#include <optional>

namespace t11wo4 {

class GameState {
public: 
    GameState(int8_t previous_winner = -1);

    void initialise_game();
    std::pair<int8_t, TileList> game_loop();
    
    // core game actions
    void play_discard_turn();
    void play_pickup_turn ();
    void draw();
    void discard(size_t action);

    // state checks
    int8_t check_if_mahjong() const;
    int8_t check_if_winner() const;
    bool check_for_mahjong(const Player& player, std::optional<Tile> tile) const;
    bool is_winning_hand(const TileList& hand, const std::vector<std::vector<Tile>>& exposed) const;
    bool can_form_four_sets(const TileList& hand, const std::vector<std::vector<Tile>>& exposed) const;

    // interrupt handling
    std::vector<std::pair<uint8_t, Action>> build_interrupt_stack(Tile tile) const;
    std::vector<std::pair<uint8_t, Action>> check_for_pung_or_gong(Tile tile) const;
    std::vector<std::pair<uint8_t, Action>> check_for_soeng(Tile tile) const;

    // getters
    GameObservation get_observations() const;

private:
    void sort_hands();
    void deal_starting_hands();
    void assign_winds();
    void expose_redraw_specials();

    std::array<Player, NUM_PLAYERS> players_;
    TileList deck_;
    TileList pile_;
    std::optional<Tile> takable_;
    
    std::vector<std::tuple<Tile, Tile, Tile>> soeng_patterns_;
    
    uint8_t roller_;
    uint8_t dice_roll_;
    uint8_t starting_player_;
    uint8_t current_player_;
    uint8_t wind_round_;
    
    bool game_over_;
    std::optional<uint8_t> winner_;
    uint32_t winning_score_;

    std::mt19937 rng_{std::random_device{}()};
};

}