from typing import List, Optional
import random

from src.player import Player

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
        self.starting_player: int = None

        self.wind_round: int = 0

        self.current_player: int = 0
        self.next_player: int = 0
        self.game_over: bool = False
        self.winner: Optional[int] = None
        self.winning_score: int = 0

    #
    # Initialise a game
    #
    def initialise_game(self):
        # Shuffle the deck
        random.shuffle(self.deck)
        # Roll the 3 dice
        self.dice_roll = random.randint(3,18)
        # Calculate the starting player
        self.starting_player = (self.roller + (self.dice_roll - 1)) % 4
        # Sync this value to be the player who's turn it is
        self.current_player = self.starting_player
        self.next_player = (self.current_player + 1) % 4

        # Deal the starting hands
        def deal_starting_hands():
            # Deals 14 tiles to the starting player
            # and 13 to the other three player
            # removing them from the deck in the process
            for i, player in enumerate(self.players):
                if i == self.starting_player:
                    for _ in range(14):
                        tile = self.deck.pop(0)
                        player.hand.append(tile)
                else:
                    for _ in range(13):
                        tile = self.deck.pop(0)
                        player.hand.append(tile)
        deal_starting_hands()

        # Assign winds to players
        def assign_winds():
            # Assigns winds to players based on the starting player
            for i in range(4):
                self.players[(self.starting_player + i) % 4].wind = i
        assign_winds()

        # Expose specials and redraw
        def expose_redraw_specials():
            # Add any specials to the specials array for the player and redraw from back of the deck
            special_encodings = [35, 36, 37, 38, 39, 40, 41, 42]
            for player in self.players:
                for i in range(len(player.hand)):
                    if player.hand[i] in special_encodings:
                        player.specials.append(player.hand[i])
                        # Technically it doesn't really matter where this tile is drawn from but whatever
                        # Good to stick to the rules i guess
                        player.hand[i] = self.deck.pop(-1)
        expose_redraw_specials()
        self.sort_hands()

    #
    # Gameplay
    #
    


    #
    # Postgame 
    #

    #
    # Utility functions
    #
    def increment_player(self):
        # Increments the current and next players in a counter clockwise motion
        self.current_player = (self.current_player + 1) % 4
        self.next_player = (self.next_player + 1) % 4

    def sort_hands(self):
        for player in self.players:
            player.hand.sort()