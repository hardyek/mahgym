from typing import List, Any
import random

from .player import Player
import actions
import utils

class Game:
    def __init__(self, agent_array: List[Any]):

        self.players: List[Player] = [Player(i) for i in range(4)]
        self.agents = agent_array

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
            "pregame" : {},
            "interupts" : {},
            "moves" : [],
            "postgame" : {},
        }

        self.pile: List[int] = []
        self.takable: int = -1 # Initialised as -1 for Typing

        # Abstracting away the entire pre-game dice roll ... stuff
        self.starting_player: int = random.randint(0,3) # Necessary to keep for scoring
        self.current_player: int = self.starting_player
        self.next_player: int = (self.current_player + 1) % 4

        self.wind_round: int = 0

        self.game_over: bool = False
        self.winner: int = -1 # Initialised as -1 for Typing
        self.winning_score: int = 0

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
        self.data["pregame"] = {
            "deck" : self.deck,
            "starting_hands" : [player.hand for player in self.players],
            "starting_player" : self.current_player,
            "starting_wind" : self.wind_round
        }

    # Main Game Loop
    def _main_loop(self):
        winner = utils.check_for_winner(self.current_player, self.players, -1) # heavenly hand

        if winner != -1:
            winning_hand = (self.players[winner].hand, self.players[winner].exposed, self.players[winner].specials, True)
            return winner, winning_hand

        while True:

            # Discard Turn
            self._complete_discard_turn()
            winner = utils.check_for_winner(self.current_player, self.players, self.takable)
            if winner != -1:
                winning_hand = (self.players[winner].hand + [self.takable], self.players[winner].exposed, self.players[winner].specials, False)
                break

            # Empty deck check
            if len(self.deck) == 0:
                winning_hand = ([-1] * 14, [], [], True)
                break

            # Pickup Turn
            self._complete_pickup_turn()
            winner = utils.check_for_winner(self.current_player, self.players, self.takable)
            if winner != -1:
                winning_hand = (self.players[winner].hand, self.players[winner].exposed, self.players[winner].specials, True)
                break

        return winner, winning_hand

    # Discard Turn
    def _complete_discard_turn(self):
        action = self.agents[self.current_player].make_discard()
        self._discard(action)

    # Pickup Turn
    def _complete_pickup_turn(self):
        interupt_queue = utils.build_interupt_queue(self.takable, self.current_player, self.players)

        pickup_action: int = 0

        for interupt in interupt_queue:
            pickup_action = self.agents[interupt[0]].make_pickup(interupt)

            if pickup_action == 1:
                self.current_player = interupt[0]
                self.players[self.current_player].recieve_tile(self.takable)

                if interupt[1] == 0: # Pung
                    self.players[self.current_player].reveal_meld([self.takable] * 3)
                    self.pile.pop(-1) # Remove takable from the pile
                elif interupt[1] == 1: # Gong
                    self.players[self.current_player].reveal_meld([self.takable] * 4)
                    self.pile.pop(-1)
                elif interupt[1] == 2: # Seong
                    self.players[self.current_player].reveal_meld(interupt[2])
                    self.pile.pop(-1)

                break

        if pickup_action == 0:
            self.current_player = (self.current_player + 1) % 4
            self._draw()

    # Post Game
    def _post_game(self, scores):
        pass
        # return new_scores

    # From actions.py
    def _draw(self):
        actions.draw(self.deck, self.players[self.current_player])

    def _discard(self, action):
        tile = actions.discard(action, self.players[self.current_player])
        self.takable = tile
        self.pile.append(tile)
