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

        self.chows = [(i, i+1, i+2) for i in range(1, 8)] + \
        [(i, i+1, i+2) for i in range(10, 17)] + \
        [(i, i+1, i+2) for i in range(19, 26)]

        self.roller: int = previous_winner
        self.dice_roll: int = 0
        self.starting_player: int = None

        self.wind_round: int = 0

        self.current_player: int = 0

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
            
            def check_specials(hand):
                for item in hand:
                    if item >= 35:
                        return True
                return False

            for player in self.players:
                while check_specials(player.hand):
                    for i in range(len(player.hand)):
                        if player.hand[i] >= 35:
                            player.specials.append(player.hand[i])
                            # Technically it doesn't really matter where this tile is drawn from but whatever
                            # Good to stick to the rules i guess
                            player.hand[i] = self.deck.pop(-1)
        expose_redraw_specials()

        self.sort_hands()

    #
    # Gameplay
    #
    def play_turn(self):
        # It starts with the current player discarding a tile
        discard_action = int(input(f"Enter discard action {self.players[self.current_player].hand}")) # Placeholder (use current player)
        self.discard(discard_action)

        interupt_stack = self.build_interupt_stack(self.takable)

        pickup_action = -1

        for item in interupt_stack:
            # Process the action 
            pickup_action = int(input(f"Enter pickup action for {item[0],self.takable, self.players[item[0]].hand}")) # Placeholder (use current player)

            if pickup_action == 1:
                self.current_player = item[0]
                self.players[self.current_player].recieve(self.takable)

                if item[1] == 0: # Pong
                    self.players[self.current_player].reveal_meld([self.takable] * 3)
                elif item[1] == 1: # Kong
                    self.players[self.current_player].reveal_meld([self.takable] * 4)
                elif item[1] == 2: # Chow
                    self.players[self.current_player].reveal_meld(item[2])
                
                break
        
        if pickup_action == -1 or pickup_action == 0:
            self.current_player = (self.current_player + 1) % 4
            self.draw()

        # End the turn by sorting the hands (for rendering mainly)
        self.sort_hands()

    #
    # Gameplay Helper Functions
    #
    def draw(self):
        # Take tile from front of the deck
        tile = self.deck.pop(0)
        # Check for special cases
        while tile >= 35 or self.players[self.current_player].hand.count(tile) == 4:
            if tile >= 35: # Special tile (flower or season)
                self.players[self.current_player].specials.append(tile)
                tile = self.deck.pop(-1) # Draw from the back of the deck
            elif self.players[self.current_player].hand.count(tile) == 4: # Concealed Kong
                self.players[self.current_player].reveal_meld([tile] * 4)
                tile = self.deck.pop(-1) # Draw from the back of the deck
        # Add non special tile to players hand
        self.players[self.current_player].recieve(tile)

    def discard(self,action):
        tile = self.players[self.current_player].discard(action)
        self.takable = tile
        self.pile.append(tile)

    def check_for_hu(self,player,tile):
        temp_hand = player.hand + [tile]
        if self.is_winning_hand(temp_hand,player.exposed):
            return player.seat
        else:
            return -1
        
    def is_winning_hand(self, hand, exposed):
        sorted_hand = hand.sort()
        for tile in set(sorted_hand): # Check all possible pairs
            if sorted_hand.count(tile) >= 2: 
                # [:] Creates a copy of the list
                remaining = sorted_hand[:]
                remaining.remove(tile)
                remaining.remove(tile)
                if self.can_form_four_sets(remaining,exposed):
                    return True
        return False

    def can_form_four_sets(self, hand, exposed):
        sets_to_form = 4 - len(exposed)

        hand = hand.sort()

        stack = [(hand, 0)]

        while stack:
            current_hand, formed_sets = stack.pop()
            if formed_sets == sets_to_form:
                return True
            
            if not current_hand:
                continue
            
            # Try to form a triplet
            if len(current_hand) >= 3 and current_hand[0] == current_hand[1] == current_hand[2]:
                new_hand = current_hand[3:]
                stack.append((new_hand, formed_sets + 1))
            
            # Try to form a sequence
            if len(current_hand) >= 3:
                if current_hand[0] + 1 in current_hand and current_hand[0] + 2 in current_hand:
                    new_hand = current_hand[:]
                    new_hand.remove(current_hand[0])
                    new_hand.remove(current_hand[0] + 1)
                    new_hand.remove(current_hand[0] + 2)
                    stack.append((new_hand, formed_sets + 1))
        
        # If we've exhausted all possibilities without returning True, it's not possible
        return False
    
        


    def build_interupt_stack(self,tile):
        # Build the stack of actions that could occur
        interupt_stack = self.check_for_pong_or_kong(tile) + self.check_for_chow(tile)
        return interupt_stack

    def check_for_pong_or_kong(self,tile):
        interupt_stack = []
        next_player = (self.current_player + 1) % 4

        while next_player != self.current_player:
            # Count the same tiles already in the players hand
            tiles_in_hand = self.players[next_player].hand.count(tile)
            if tiles_in_hand == 2:
                interupt_stack.append([next_player,0]) # 0 for Pong
            elif tiles_in_hand == 3:
                interupt_stack.append([next_player,1]) # 1 for Kong
            # Increment to the next player
            next_player = (next_player + 1) % 4

        return interupt_stack
    
    def check_for_chow(self,tile):
        interupt_stack = []
        next_player = (self.current_player + 1) % 4
        # Create a temporary array contaning the deck with the takable tile
        hand_with_tile = self.players[next_player].hand + [tile]

        # Check for possible chows
        for chow in self.chows:
            if tile in chow:
                if all(t in hand_with_tile for t in chow):
                    interupt_stack.append([next_player,2,chow])

        return interupt_stack

    #
    # Postgame 
    #

    #
    # Utility
    #
    def sort_hands(self):
        for player in self.players:
            player.hand.sort()