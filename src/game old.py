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
        self.last_discarder: int = 0

        self.game_over: bool = False
        self.winner: Optional[int] = None
        self.winning_score: int = 0

    def initialise_game(self):
        # Shuffle the deck
        random.shuffle(self.deck)
        # Roll the 3 dice
        self.dice_roll = random.randint(3,18)
        # Calculate the starting player
        self.starting_player = self.roller + (self.dice_roll % 4 - 1) - 1
        # Sync this value to be the player who's turn it is
        self.current_player = self.starting_player
        # Deal the starting hands
        self.deal_starting_hands()
        # Assign winds to players
        self.assign_winds()
        # Expose specials and redraw
        self.expose_redraw_specials()

    def deal_starting_hands(self):
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

    def assign_winds(self):
        # Assigns winds to players based on the starting player
        for i in range(4):
            self.players[(self.starting_player + i) % 4].wind = i

    def expose_redraw_specials(self):
        # Add any specials to the specials array for the player and redraw from back of the deck
        special_encodings = [35, 36, 37, 38, 39, 40, 41, 42]
        for player in self.players:
            for i in range(len(player.hand)):
                if player.hand[i] in special_encodings:
                    player.specials.append(player.hand[i])
                    # Technically it doesn't really matter where this tile is drawn from but whatever
                    # Good to stick to the rules i guess
                    player.hand[i] = self.deck.pop(-1)

    def make_action_pickup(self, action):
        if action == 0:
            self.draw()
        if action == 1:
            ... # Pong
        if action == 2:
            ... # Chow
        if action == 3:
            ... # Kong
        if action == 4:
            ... # Hu

    def make_action_discard(self, action):
        self.discard(action)

    def draw(self):
        # Take tile from front of the deck
        tile = self.deck.pop(0)
        # Check for special cases
        while tile >= 35 or self.players[self.current_player].hand.count(tile) == 4:
            if tile >= 35: # Special tile (flower or season)
                self.players[self.current_player].specials.append(tile)
                tile = self.deck.pop(-1) # Draw from the back of the deck
            elif self.players[self.current_player].hand.count(tile) == 4: # Concealed Kong
                meld = [tile] * 4 # Create the Kong meld
                self.players[self.current_player].reveal_meld(meld)
                tile = self.deck.pop(-1) # Draw from the back of the deck
        # Add non special tile to players hand
        self.players[self.current_player].recieve(tile)

    def pong(self):
        tile = self.takable
        self.takable = 0
        meld = [tile] * 3
        self.players[self.current_player].reveal_meld(meld)

    def chow(self):
        ...
    
    def kong(self): # Exposed Kong
        tile = self.takable
        self.takable = 0
        meld = [tile] * 4
        self.players[self.current_player].reveal_meld(meld)

    def hu(self):
        ...

    def is_pickup_action_legal(self, action) -> bool:
        if action == 0: # Draw
            return True # Drawing will always be a legal move (if deck is empty game will draw not the players fault)
        if action == 1: # Pong
            ... # Pong
        if action == 2:
            ... # Chow
        if action == 3:
            ... # Kong
        if action == 4:
            ... # Hu

    def discard(self, tile):
        # Discard tile from players hand to the pile (also now the takable tile)
        self.players[self.current_player].discard(tile)
        self.takable = tile
        self.pile.append(tile)
        self.last_discarder = self.current_player

    def is_discard_action_legal(self, action) -> bool:
        # Check if discarded tile is actually in the hand of the player
        legal = action in self.players[self.current_player].hand
        return legal    

    def turn(self):
        # Turn body
        pickup_action = ... # Placeholder for pickup action logic
        self.make_action_pickup(pickup_action)
        discard_action = ... # Placeholder for discard action logic
        self.make_action_discard(discard_action)
        # Setting up for next players turn
        self.current_player += 1


