from typing import List

class Player:
    def __init__(self, seat : int):
        self.seat = seat
        self.hand: List[int] = []
        self.exposed: List[int] = []
        self.flowers: List[int] = []
        self.wind: int = ""

    def recieve(self, tile: int):
        self.hand.append(tile)

    def discard(self, tile: int) -> int:
        self.hand.remove(tile)
        return tile
    
    def reveal_meld(self, meld: List[int]):
        for tile in meld:
            self.hand.remove(tile)
            self.exposed.append(tile)