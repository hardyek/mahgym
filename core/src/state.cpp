#include "state.hpp"
#include "errors.hpp"
#include <algorithm>
#include <random>

namespace t11wo4 {
    
    GameState::GameState(int8_t previous_winner)
        : players_{Player(0), Player(1), Player(2), Player(3)}
        , roller_{previous_winner == -1 ? static_cast<uint8_t>(std::uniform_int_distribution<>(0, 3)(rng_))
                                        : static_cast<uint8_t>(previous_winner)}
        , game_over_{false}
        , winner_{std::nullopt}
        , winner_score_{0} {

        // initialise tiles
        deck_.reserve(MAX_TILES);
        // non specials
        for (Tile t = 1; t <= 34; ++t) {
            for (int i = 0; i < 4; ++i) {
                deck_.push_back(t);
            }
        }
        // specials
        for (Tile t = 35; t <= 42; ++t) {
            deck_.push_back(t);
        }

        // initialise soeng patterns
        for (Tile t = 1; t <= 25; t += 9){
            for (Tile i = t; i < t + 7; ++i) {
                soeng_patterns_.push_back({i, static_cast<Tile>(i + 1), static_cast<Tile>(i + 2)});
            }
        }
    }

    void GameState::initialise_game() {
        // shuffle deck
        std::shuffle(deck_.begin(), deck_.end(), rng_);

        // roll dice
        dice_roll_ = std::uniform_int_distribution<>(3, 18)(rng_);

        // calculate starting player
        starting_player_ = (roller_ + (dice_roll_ - 1)) % 4;
        current_player_ = starting_player_;

        deal_starting_hands();
        assign_winds();
        expose_redraw_specials();
        sort_hands();
    }

    void GameState::deal_starting_hands() {
        for (size_t i = 0; i < NUM_PLAYERS; ++i) {
            size_t tiles_to_deal = (i == starting_player_) ? 14 : 13;
            for (size_t j = 0; j < tiles_to_deal; ++j) {
                players_[i].receive(deck_.back());
                deck_.pop_back();
            }
        }
    }

    void GameState::assign_winds() {
        for (size_t i = 0; i < NUM_PLAYERS; ++i) {
            players_[(starting_player_ + i) % 4].set_wind(static_cast<Wind>(i));
        }
    }

    void GameState::expose_redraw_specials() {
        for (auto& player : players_) {
            bool has_special;
            do {
                has_special = false;
                auto& hand = player.get_hand();
                for (auto it = hand.begin(); it != hand.end(); ) {
                    if (*it >= TileRanges::FLOWERS_START) {
                        // move to specials
                        has_special = true;
                        player.add_special(*it);
                        // draw replacement from back not that it matters
                        if (!deck_.empty()) {
                            player.receive(deck_.back());
                            deck_.pop_back();
                        }
                        break;
                    }
                    ++it;
                }
            } while (has_special && !deck_.empty());
        }
    }

    std::pair<int8_t, TileList> GameState::game_loop() {
        // check for 10wo4 (smile)
        if (auto winner = check_if_winner(); winner != -1) {
            return {winner, players_[winner].get_hand()};
        }
        
        while (!game_over_ && !deck_.empty()) {
            play_discard_turn();
            
            if (auto winner = check_if_mahjong(); winner != -1) {
                auto winning_tiles = players_[winner].get_hand();
                if (takable_) winning_tiles.push_back(*takable_);
                return {winner, winning_tiles};
            }

            play_pickup_turn();
            
            if (auto winner = check_if_winner(); winner != -1) {
                return {winner, players_[winner].get_hand()};
            }
        }
        return {-1, TileList(14, -1)}; // drawn game
    }

    void GameState::play_discard_turn() {
        // TODO: Implement agent interaction
        // For now, just discard first tile
        discard(0);
    }

    void GameState::play_pickup_turn() {
        auto interrupts = build_interrupt_stack(*takable_);
        
        // TODO: Implement agent decisions
        // For now, just draw next tile
        current_player_ = (current_player_ + 1) % 4;
        draw();
        sort_hands();
    }

    void GameState::draw() {
        if (deck_.empty()) {
            throw IllegalStateEror("Cannot draw from an empty deck");
        }

        Tile drawn = deck_.back();
        deck_.pop_back();

        while (!deck_.empty() && (drawn >= TileRanges::FLOWERS_START || players_[current_player_].get_hand().count(drawn) == 3)) {
            if (drawn >= TileRanges::FLOWERS_START) {
                players_[current_player_].add_special(drawn);
            } else {
                // concealed gong
                players_[current_player_].reveal_meld(std::vector<Tile>(4, drawn));
            }
            drawn = deck_.back();
            deck_.pop_back();
        }
        
        players_[current_player_].receive(drawn);
    }

    void GameState::discard(size_t action) {
        auto& player = players_[current_player_];
        if (action >= player.get_hand().size()) {
            throw InvalidMoveError("Invalid discard index");
        }
        
        Tile discarded = player.discard(action);
        takable_ = discarded;
        pile_.push_back(discarded);
    }

    int8_t GameState::check_if_mahjong() const {
        uint8_t next_player = (current_player_ + 1) % 4;
        do {
            if (check_for_mahjong(players_[next_player], takable_)) {
                return next_player;
            }
            next_player = (next_player + 1) % 4;
        } while (next_player != current_player_);
        return -1;
    }

    int8_t GameState::check_if_winner() const {
        if (check_for_mahjong(players_[current_player_], std::nullopt)) {
            return current_player_;
        }
        return -1;
    }

    bool GameState::check_for_mahjong(const Player& player, std::optional<Tile> tile) const {
        TileList temp_hand = player.get_hand();
        if (tile) {
            temp_hand.push_back(*tile);
        }
        return is_winning_hand(temp_hand, player.get_exposed());
    }

    bool GameState::is_winning_hand(const TileList& hand, const std::vector<std::vector<Tile>>& exposed) const {
        TileList sorted_hand = hand;
        std::sort(sorted_hand.begin(), sorted_hand.end());
        
        // Try each possible pair
        for (auto it = sorted_hand.begin(); it != sorted_hand.end();) {
            Tile tile = *it;
            auto next = std::find(std::next(it), sorted_hand.end(), tile);
            if (next != sorted_hand.end()) {
                // Found a pair, remove it and check if remaining tiles form valid sets
                TileList remaining = sorted_hand;
                remaining.erase(std::find(remaining.begin(), remaining.end(), tile));
                remaining.erase(std::find(remaining.begin(), remaining.end(), tile));
                
                if (can_form_four_sets(remaining, exposed)) {
                    return true;
                }
            }
            it = std::find_if(std::next(it), sorted_hand.end(), 
                            [tile](Tile t) { return t != tile; });
        }
        return false;
    }

    bool GameState::can_form_four_sets(const TileList& hand, const std::vector<std::vector<Tile>>& exposed) const {
        size_t sets_needed = 4 - exposed.size();
        if (hand.size() != sets_needed * 3) {
            return false;
        }

        std::function<bool(const TileList&, size_t)> try_form_sets = 
            [&](const TileList& tiles, size_t sets_formed) {
                if (sets_formed == sets_needed) {
                    return true;
                }
                if (tiles.empty()) {
                    return false;
                }

                TileList remaining = tiles;
                
                // Try forming a pung
                if (tiles.size() >= 3 && 
                    tiles[0] == tiles[1] && 
                    tiles[1] == tiles[2]) {
                    remaining.erase(remaining.begin(), remaining.begin() + 3);
                    if (try_form_sets(remaining, sets_formed + 1)) {
                        return true;
                    }
                    remaining = tiles;  // backtrack
                }

                // Try forming a soeng
                if (tiles.size() >= 3) {
                    for (const auto& pattern : soeng_patterns_) {
                        if (std::includes(tiles.begin(), tiles.end(), 
                                        std::get<0>(pattern), std::get<2>(pattern))) {
                            remaining.erase(std::find(remaining.begin(), remaining.end(), std::get<0>(pattern)));
                            remaining.erase(std::find(remaining.begin(), remaining.end(), std::get<1>(pattern)));
                            remaining.erase(std::find(remaining.begin(), remaining.end(), std::get<2>(pattern)));
                            if (try_form_sets(remaining, sets_formed + 1)) {
                                return true;
                            }
                            remaining = tiles;  // backtrack
                        }
                    }
                }
                
                return false;
            };

        TileList sorted_hand = hand;
        std::sort(sorted_hand.begin(), sorted_hand.end());
        return try_form_sets(sorted_hand, 0);
    }

    std::vector<std::pair<uint8_t, Action>> GameState::build_interrupt_stack(Tile tile) const {
        auto interrupts = check_for_pung_or_gong(tile);
        auto soeng_interrupts = check_for_soeng(tile);
        interrupts.insert(interrupts.end(), soeng_interrupts.begin(), soeng_interrupts.end());
        return interrupts;
    }

    std::vector<std::pair<uint8_t, Action>> GameState::check_for_pung_or_gong(Tile tile) const {
        std::vector<std::pair<uint8_t, Action>> interrupts;
        uint8_t next_player = (current_player_ + 1) % 4;

        do {
            size_t count = std::count(players_[next_player].get_hand().begin(),
                                    players_[next_player].get_hand().end(), 
                                    tile);
            if (count == 2) {
                interrupts.emplace_back(next_player, Action::PUNG);
            } else if (count == 3) {
                interrupts.emplace_back(next_player, Action::GONG);
            }
            next_player = (next_player + 1) % 4;
        } while (next_player != current_player_);

        return interrupts;
    }

    std::vector<std::pair<uint8_t, Action>> GameState::check_for_soeng(Tile tile) const {
        std::vector<std::pair<uint8_t, Action>> interrupts;
        uint8_t next_player = (current_player_ + 1) % 4;
        
        const auto& hand = players_[next_player].get_hand();
        TileList hand_with_tile = hand;
        hand_with_tile.push_back(tile);
        std::sort(hand_with_tile.begin(), hand_with_tile.end());

        for (const auto& pattern : soeng_patterns_) {
            if (std::includes(hand_with_tile.begin(), hand_with_tile.end(),
                            std::get<0>(pattern), std::get<2>(pattern))) {
                interrupts.emplace_back(next_player, Action::SOENG);
            }
        }

        return interrupts;
    }

    void GameState::sort_hands() {
        for (auto& player : players_) {
            player.sort_hand();
        }
    }

}