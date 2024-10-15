from typing import List, Optional
import random

from player import Player

class MahjongGame:
    def __init__(self, previous_winner=random.randint(0,3)):
        self.players: List[Player] = [Player(i) for i in range(4)]

        self.deck: List[int] = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, # Numeric 1 - 9 
            1, 2, 3, 4, 5, 6, 7, 8, 9,
            1, 2, 3, 4, 5, 6, 7, 8, 9,
            1, 2, 3, 4, 5, 6, 7, 8, 9,

            10, 11, 12, 13, 14, 15, 16, 17, 18, # Circles 1 - 9
            10, 11, 12, 13, 14, 15, 16, 17, 18,
            10, 11, 12, 13, 14, 15, 16, 17, 18,
            10, 11, 12, 13, 14, 15, 16, 17, 18,

            19, 20, 21, 22, 23, 24, 25, 26, 27, # Bamboo 1 - 9
            19, 20, 21, 22, 23, 24, 25, 26, 27,
            19, 20, 21, 22, 23, 24, 25, 26, 27,
            19, 20, 21, 22, 23, 24, 25, 26, 27,

            28, 28, 28, 28, # North 
            29, 29, 29, 29, # East
            30, 30, 30, 30, # South
            31, 31, 31, 31, # West

            32, 32, 32, 32, # White
            33, 33, 33, 33, # Green
            34, 34, 34, 34, # Red

            35, 36, 37, 38, 39, 40, 41, 42 # 4 Flowers +  4 Seasons
        ]
        self.pile: List[int] = []
        self.takable: Optional[int] = None

        self.roller: int = previous_winner
        self.dice_roll: int = 0
        self.starting_player: int = 0

        self.wind_round: int = 0

        self.current_player: int = 0

        self.game_over: bool = False
        self.winner: Optional[int] = None
        self.winning_score: int = 0

    def initialise_game(self):
        # Shuffle the deck
        random.shuffle(self.deck)
        # Roll the 3 dice
        self.dice_roll = random.randint(3,18)
        # Calculate the starting player
        self.starting_player = self.roller + (self.dice_roll % 4 - 1)
        # Sync this value to be the player who's turn it is
        self.current_player = self.starting_player
        # Deal the starting hands
        self.deal_starting_hands()
        # Assign winds to players
        self.assign_winds()