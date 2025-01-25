from typing import List

from .player import Player

def draw(deck: List[int], player: Player) -> None:
    tile = deck.pop(0)
    while tile > 50 or player.count_tile(tile) == 3:
        if len(deck) == 0:
            return -1

        if tile > 50:
            player.add_special(tile)
        else:
            player.reveal_meld([tile] * 4)

        tile = deck.pop(-1)

    player.recieve_tile(tile)

def discard(action: int, player: Player) -> int:
    tile = player.discard_tile(action)
    return tile
