from typing import List, Dict
from dataclasses import dataclass

@dataclass(slots = True) # For faster attribute access and memory saving
class Player:
    seat: int
    wind: int = 0
    score: int = 0
    hand: List[int] = None
    exposed: List[List[int]] = None 
    specials: List[int] = None
    _hand_counts: Dict[int, int] = None

    def __post_init__(self):
        self.hand = []
        self.exposed = []
        self.specials = []
        self._hand_counts = {} # Cache of tile counts for O(1) lookups

    def recieve_tile(self, tile: int) -> None:
        self.hand.append(tile)
        self._hand_counts[tile] = self._hand_counts.get(tile, 0) + 1 
    
    def discard_tile(self, index: int) -> int:
        tile = self.hand.pop(index)
        self._hand_counts[tile] -= 1
        if self._hand_counts[tile] == 0:
            del self._hand_counts[tile]
        return tile
    
    def reveal_meld(self, meld: List[int]) -> None:
        for tile in meld:
            self.hand.remove(tile)
            self._hand_counts[tile] -= 1
            if self._hand_counts[tile] == 0:
                del self._hand_counts[tile]
        self.exposed.append(meld)
    
    def add_special(self, tile: int) -> None:
        self.specials.append(tile)
    
    def count_tile(self, tile: int) -> int:
        return self._hand_counts.get(tile, 0)
    
    def has_tiles(self, tiles: List[int]) -> bool:
        return all(self.count_tile(t) >= tiles.count(t) for t in set(tiles))
