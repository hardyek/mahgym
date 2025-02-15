from typing import List, Dict

class Player:
    def __init__(self, seat: int):
        self.seat: int = seat
        self.wind: int = 0
        self.hand: List[int] = []
        self.exposed: List[List[int]] = []
        self.specials: List[int] = []
        self._hand_counts: Dict[int, int] = {}

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
