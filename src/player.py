from typing import List

class Player:
    def __init__(self, seat : int):
        self.seat = seat
        self.hand: List[int] = []
        self.exposed: List[int] = []
        self.specials: List[int] = []
        self.wind: int = ""

    def recieve(self, tile: int):
        self.hand.append(tile)

    def discard(self, tile: int):
        self.hand.remove(tile)
    
    def reveal_meld(self, meld: List[int]):
        for tile in meld:
            self.hand.remove(tile)
            self.exposed.append(tile)