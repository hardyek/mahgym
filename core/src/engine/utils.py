from typing import List

from .player import Player
from .scoring import *

def check_if_winner_exists(current_player: int, players: List[Player], takable: int) -> int:
    next_player = (current_player + 1) % 4
    while next_player != current_player:
        if check_for_mahjong(players[next_player], takable):
            return next_player
        
        next_player = (next_player + 1) % 4
    return -1

def check_current_is_winner(player: Player) -> bool:
    if check_for_mahjong(player, -1):
        return True
    else:
        return False
    
def check_for_mahjong(player: Player, tile: int) -> bool:
    if tile == -1:
        hand = player.hand
    else:
        hand = player.hand + [tile]
    if is_winning_hand(hand, player.exposed):
        return True
    else:
        return False
    
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
    
        next_player = (next_player + 1) % 4
    
    # Check for SOENG 
    next_player = (current_player + 1) % 4

    suit_start = (tile // 10) * 10
    sequences = [seq for seq in [[tile-2, tile-1, tile],[tile-1, tile, tile+1],[tile, tile+1, tile+2]] if all(suit_start <= t < suit_start + 10 for t in seq)] # what is readability

    for seq in sequences:
        if players[next_player].has_tiles([t for t in seq if t != tile]):
            interupts.append((next_player, 2, seq))
    
    return interupts