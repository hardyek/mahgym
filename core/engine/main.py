from typing import List, Type, Dict, Optional
import random

from ..agents.agent import Agent

import utils

from shorthand import to_shorthand, meld_to_shorthand

from scoring import ScoringInfo, score

class Game:
    def __init__(self, agent_array: List[Type[Agent]], round_wind):

        self.players: List[Type[Agent]] = agent_array

        self.deck: List[int] = [
             # Characters
            1, 2, 3, 4, 5, 6, 7, 8, 9,
            1, 2, 3, 4, 5, 6, 7, 8, 9,
            1, 2, 3, 4, 5, 6, 7, 8, 9,
            1, 2, 3, 4, 5, 6, 7, 8, 9,
            # Circles
            11, 12, 13, 14, 15, 16, 17, 18, 19,
            11, 12, 13, 14, 15, 16, 17, 18, 19,
            11, 12, 13, 14, 15, 16, 17, 18, 19,
            11, 12, 13, 14, 15, 16, 17, 18, 19,
            # Bamboo
            21, 22, 23, 24, 25, 26, 27, 28, 29,
            21, 22, 23, 24, 25, 26, 27, 28, 29,
            21, 22, 23, 24, 25, 26, 27, 28, 29,
            21, 22, 23, 24, 25, 26, 27, 28, 29,
            # Winds
            31, 31, 31, 31, # North
            32, 32, 32, 32, # East
            33, 33, 33, 33, # South
            34, 34, 34, 34, # West
            # Dragons
            41, 41, 41, 41, # White
            42, 42, 42, 42, # Green
            43, 43, 43, 43, # Red
            # Specials
            51, 52, 53, 54, # Flowers
            61, 62, 63, 64 # Seasons
        ]
        random.shuffle(self.deck) # hopefully self-explanatory

        self.data = {
            'pregame' : {},
            'interrupts' : [],
            'actions' : [],
            'postgame' : {},
        }

        self.pile: List[int] = []
        self.takable: int = -1 # Initialised as -1 for Typing

        # Abstracting away the entire pre-game dice roll ... stuff
        self.starting_player: int = random.randint(0,3) # Necessary to keep for scoring
        self.current_player: int = self.starting_player

        self.round_wind: int = round_wind

        self.heaven: bool = True

        self.discarder: int = -1

        self.game_over: bool = False
        self.winner: int = -1 # Initialised as -1 for Typing
        self.winning_score: int = 0

        self.last_gong_made = False  # Track if the last action was a gong
        self.last_gong_player = -1   # Track who made the last gong

    def _initialise_game(self):
        # Deal starting hands
        # not a proper way of dealing but since the deck is shuffled it doesn't matter anyway
        for i, player in enumerate(self.players):
            if i == self.current_player:
                for _ in range(14):
                    tile = self.deck.pop(0)
                    player.recieve_tile(tile)
            else:
                for _ in range(13):
                    tile = self.deck.pop(0)
                    player.recieve_tile(tile)

        # Assign wind + Expose specials and redraw
        for i in range(4):

            self.players[(self.current_player + i) % 4].wind = i

            player = self.players[(self.current_player + i) % 4]
            # Get indices of all special tiles at once
            special_indices = [i for i, tile in enumerate(player.hand) if tile > 40]
            while special_indices:
                player.specials.extend(player.hand[i] for i in special_indices)
                # Replace specials with new tiles
                for i in special_indices:
                    player.hand[i] = self.deck.pop(-1)
                # Check for new specials after replacement
                special_indices = [i for i, tile in enumerate(player.hand) if tile > 40]

        # Save pregame daata
        self.data['pregame'] = {
            'deck' : self.deck,
            'starting_hands' : [player.hand for player in self.players],
            'starting_player' : self.current_player,
            'starting_wind' : self.round_wind
        }

    # Main Game Loop
    def _main_loop(self):
        self.data['actions'].append(f'B{self.current_player}') # Shorthand B{player} game start on player.

        potential_winner = utils.check_for_valid_14(self.current_player, self.players, -1) # heavenly hand

        if potential_winner != -1:
            scoring_info = self._game_end_check(potential_winner)
            if scoring_info:
                self.data['actions'].append(f'M{self.current_player}') # Shorthand M{player} declare win!
                self.data['postgame'] = scoring_info
                return scoring_info
            
        self.heaven = False

        while True:

            # Discard Turn
            self._complete_discard_turn()
            potential_winner = utils.check_for_valid_14(self.current_player, self.players, self.takable)
            if potential_winner != -1:
                scoring_info = self._game_end_check(potential_winner)
                if scoring_info:
                    break

            # Pickup Turn
            self._complete_pickup_turn()
            potential_winner = utils.check_for_valid_14(self.current_player, self.players, self.takable)
            if potential_winner != -1:
                scoring_info = self._game_end_check(potential_winner)
                if scoring_info:
                    break

            # Empty deck check
            if len(self.deck) == 0:
                self.data['actions'].append('L0') # Shorthand L0 declare draw
                self.data['postgame'] = {'result': 'draw'}
                return self.data['postgame']

        self.data['actions'].append(f'M{self.current_player}') # Shorthand M{player} declare win!
        self.data['postgame'] = scoring_info if scoring_info else {'result' : 'draw'}
        return scoring_info

    # Discard Turn
    def _complete_discard_turn(self):
        action = self.players[self.current_player].make_discard()
        self.data['actions'].append(f'D{self.current_player}{to_shorthand[action]}') # Shorthand D{player}{tile} DISCARD
        self._discard(action)

    # Pickup Turn
    def _complete_pickup_turn(self):
        interupt_queue = utils.build_interupt_queue(self.takable, self.current_player, self.players)

        self.data['interrupts'].append(interupt_queue)
        self.data['actions'].append(f'E{len(self.data['interrupts'])}') # Shorthand E{turn} END OF TURN

        pickup_action: int = 0

        for interupt in interupt_queue:
            pickup_action = self.players[interupt[0]].make_pickup(interupt)

            if pickup_action == 1:
                self.current_player = interupt[0]
                self.players[self.current_player].recieve_tile(self.takable)

                if interupt[1] == 0: # Pung
                    self.players[self.current_player].reveal_meld([self.takable] * 3)
                    self.pile.pop(-1) # Remove takable from the pile

                    self.data['actions'].append(f'P{self.current_player}{to_shorthand[self.takable]}') # Shorthand P{player}{tile} PUNG

                elif interupt[1] == 1: # Gong
                    self.players[self.current_player].reveal_meld([self.takable] * 4)
                    self.pile.pop(-1)

                    self.data['actions'].append(f'G{self.current_player}{to_shorthand[self.takable]}') # Shorthand G{player}{tile} GONG

                    self.last_gong_made = True  # For scoring
                    self.last_gong_player = self.current_player

                    extra_tile = self._draw()
                    if extra_tile != -1:
                        self.data['actions'].append(f'T{self.current_player}{to_shorthand[extra_tile]}')

                elif interupt[1] == 2: # Seong
                    self.players[self.current_player].reveal_meld(interupt[2])
                    self.pile.pop(-1)

                    self.data['actions'].append(f'S{self.current_player}{meld_to_shorthand(interupt[2])}') # Shorthand S{player}{meld} SEONG

                break

        if pickup_action == 0:
            self.current_player = (self.current_player + 1) % 4
            tile = self._draw()

            if tile != -1:
                self.data['actions'].append(f'T{self.current_player}{to_shorthand[tile]}') # Shorthand T{player}{tile} DRAW

        self.takable = -1

    def _draw(self) -> int:
        tile = self.deck.pop(0)
        while tile > 50 or self.players[self.current_player].count_tile(tile) == 3 or utils.check_promote_pung(tile, self.players[self.current_player]) != -1:
            if len(self.deck) == 0:
                return -1

            if tile > 50:
                self.players[self.current_player].add_special(tile)

                self.data['actions'].append(f'X{self.current_player}{to_shorthand[tile]}') # Shorthand X{player}{tile} REVEAL SPECIAL

            elif self.players[self.current_player].count_tile(tile) == 3:
                self.players[self.current_player].reveal_meld([tile] * 4)

                self.data['actions'].append(f'H{self.current_player}{to_shorthand[tile]}') # Shorthand H{player}{tile} CONCEALED GONG

                self.last_gong_made = True # For scoring
                self.last_gong_player = self.current_player

            else:
                action = self.players[self.current_player].make_promote()
                if action == 1:
                    for i in range(4):
                        check_player = (self.current_player + i) % 4
                        if check_player != self.current_player:
                            if utils.check_for_valid_14(check_player, self.players, tile) != -1:
                                # Someone can rob the gong!
                                self.current_player = check_player
                                self.players[check_player].recieve_tile(tile)
                                self.takable = tile  # Set takable for scoring
                                self.data['actions'].append(f'R{check_player}{to_shorthand[tile]}')  # Shorthand R{player}{tile} ROBBING GONG
                                return tile  # Return the tile so game flow continues normally
                    
                    self.players[self.current_player].exposed[utils.check_promote_pung(tile, self.players[self.current_player])].append(tile)

                    self.data['actions'].append(f'G{self.current_player}{to_shorthand[tile]}') # Shorthand G{player}{tile} GONG

                    self.last_gong_made = True
                    self.last_gong_player = self.current_player

                    extra_tile = self._draw()
                    if extra_tile != -1:
                        self.data['actions'].append(f'T{self.current_player}{to_shorthand[extra_tile]}')
                else:
                    break

            tile = self.deck.pop(-1)

        self.players[self.current_player].recieve_tile(tile)
        return tile

    def _discard(self, action) -> int:
        tile = self.players[self.current_player].discard_tile(action)
        self.takable = tile
        self.pile.append(tile)
        self.discarder = self.current_player
        return tile

    def _game_end_check(self, potential_winner) -> Optional[Dict]:
        scoring_info = ScoringInfo(
        concealed_hand = self.players[potential_winner].hand,
        exposed_melds = self.players[potential_winner].exposed,
        specials = self.players[potential_winner].specials,
        winning_tile = self.takable,
        is_self_drawn = self.takable == -1,  # if takable is -1, it was a self-drawn win
        is_last_tile = len(self.deck) == 0,
        is_robbing_Gong = ('R' + str(potential_winner)) in [action[:2] for action in self.data['actions'][-1:]],
        is_last_Gong = self.last_gong_made and self.last_gong_player == potential_winner,
        seat_wind = self.players[potential_winner].wind,
        round_wind = self.round_wind,
        declared_gongs = [meld for meld in self.players[potential_winner].exposed if len(meld) == 4],
        is_dealer = self.players[potential_winner].wind == 0,
        heaven = self.heaven,
        discarderd = self.discarder
        )

        points = score(scoring_info)
        if points >= 3:
            return {
                'result': 'win',
                'winner': potential_winner,
                'scoring_info': scoring_info,
                'points': points
            }
        return None