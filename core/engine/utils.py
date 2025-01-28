from typing import List

from .player import Player
from .scoring import is_valid_14

def check_for_valid_14(current_player: int, players: List[Player], takable: int) -> int:
    if takable == -1:
        if is_valid_14(players[current_player].hand, players[current_player].exposed):
            return current_player

    else:
        next_player = (current_player + 1) % 4
        while next_player != current_player:
            test_hand = players[next_player].hand + [takable]
            if is_valid_14(test_hand, players[next_player].exposed):
                return next_player
            next_player = (next_player + 1) % 4

    return -1

def build_interupt_queue(tile: int, current_player: int, players: List[Player]) -> List[tuple[int, int, List[int]]]:
    interupts = []
    # Check for PUNG or GONG
    next_player = (current_player + 1) % 4

    while next_player != current_player:
        tiles_in_hand = players[next_player].count_tile(tile)

        if tiles_in_hand == 2:
            interupts.append((next_player, 0, [tile] * 3)) # 0 for PUNG
        elif tiles_in_hand == 3:
            interupts.append((next_player, 1, [tile] * 4)) # 1 for GONG
        else:
            # Updgrading a PUNG to a GONG
            for meld in players[next_player].exposed:
                if meld[0] == tile and meld[1] == tile:
                    interupts.append((next_player, 1, [tile] * 4))

        next_player = (next_player + 1) % 4

    # Check for SOENG
    next_player = (current_player + 1) % 4

    suit_start = (tile // 10) * 10
    sequences = [seq for seq in [[tile-2, tile-1, tile],[tile-1, tile, tile+1],[tile, tile+1, tile+2]] if all(suit_start <= t < suit_start + 10 for t in seq)] # what is readability

    for seq in sequences:
        if players[next_player].has_tiles([t for t in seq if t != tile]):
            interupts.append((next_player, 2, seq))

    return interupts

def check_promote_pung(tile: int, player: Player) -> int:
    for i in range(len(player.exposed)):
        if tile == player.exposed[i][0] and tile == player.exposed[i][1]:
            return i
    return -1
