from typing import List, Optional, Any
import random

from .player import Player
from actions import *
from utils import *

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
            "moves" : {
                "discard" : {},
                "pickup" : {}
            },
            "postgame" : {},
        }

        self.pile = List[int] = []
        self.takable: Optional[int] = None
        
        # Abstracting away the entire pre-game dice roll ... stuff
        self.current_player: int = random.randint(0,3)
        self.next_player: int = (self.current_player + 1) % 4

        self.wind_round: int = 0

        self.game_over: bool = False
        self.winner: Optional[int] = None
        self.winning_score: int = 0

    def _initialise_game(self):
        # Deal starting hands
        for i, player in enumerate(self.players):
            if i == self.current_player:
                for _ in range(14):
                    tile = self.deck.pop(0)
                    player.recieve_tile(tile)
            else:
                for _ in range(13):
                    tile = self.deck.pop(0)
                    player.recieve_tile(tile)
        
        # Assign wind + Expose specials and redraw + Sort hands
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

            player.hand.sort()

        # Save pregame daata
        self.data["pregame"] = {
            "deck" : self.deck,
            "starting_hands" : [player.deck for player in self.players],
            "starting_player" : self.current_player,
            "starting_wind" : self.wind_round
        }

    # From actions.py

    def _draw(self):
        return draw(self.deck, self.players[self.current_player])
    
    def _discard(self, action):
        tile = discard(action, self.players[self.current_player])
        self.takable = tile
        self.pile.append(tile)

    # From utils.py

