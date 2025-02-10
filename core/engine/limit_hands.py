from typing import List
from collections import Counter

def check_big_four_winds(tiles: List[int]) -> bool:
    wind_counts = Counter(t for t in tiles if 31 <= t <= 34)
    return all(count >= 3 for count in wind_counts.values())

def check_big_three_dragons(tiles: List[int]) -> bool:
    dragon_counts = Counter(t for t in tiles if 41 <= t <= 43)
    return all(count >= 3 for count in dragon_counts.values())

def check_all_honors(tiles: List[int]) -> bool:
    return all(t >= 30 for t in tiles)

def check_all_terminals(tiles: List[int]) -> bool:
    return all(t in [1,9,11,19,21,29] for t in tiles)

def check_thirteen_orphans(tiles: List[int]) -> bool:
    required = [1,9,11,19,21,29,31,32,33,34,41,42,43]
    return all(t in tiles for t in required) and len(tiles) == 14

def check_nine_gates(tiles: List[int]) -> bool:
    if len(tiles) != 14:
        return False
    # All tiles must be in same suit
    suit = tiles[0] // 10
    if not all(t // 10 == suit for t in tiles):
        return False
    # Need 1,1,1,2,3,4,5,6,7,8,9,9,9 plus one extra
    base_tiles = [suit*10 + i for i in [1,1,1,2,3,4,5,6,7,8,9,9,9]]
    remaining = tiles.copy()
    for t in base_tiles:
        if t not in remaining:
            return False
        remaining.remove(t)
    return len(remaining) == 1 and remaining[0] // 10 == suit

def check_all_green(tiles: List[int]) -> bool:
    green_tiles = [22,23,24,26,28,42]  # 2,3,4,6,8 of bamboo and Green Dragon
    return all(t in green_tiles for t in tiles)

def check_four_concealed_pungs(hand: List[int], is_self_drawn: bool) -> bool:
    if not is_self_drawn:
        return False
    counts = Counter(hand)
    pung_count = sum(1 for count in counts.values() if count >= 3)
    pair_count = sum(1 for count in counts.values() if count == 2)
    return pung_count == 4 and pair_count == 1

def check_special_patterns(tiles: List[int], self_drawn: bool) -> bool:
    """
    Check if tiles form any of the special winning patterns under Hong Kong rules.
    
    Args:
        tiles (List[int]): List of tiles to check
        self_drawn (bool): Whether the winning tile was self-drawn
        
    Returns:
        bool: True if tiles form any special pattern, False otherwise
    """
    # Thirteen Orphans can be claimed from discard
    if check_thirteen_orphans(tiles):
        return True
        
    # Nine Gates must be claimed self-drawn
    if self_drawn and check_nine_gates(tiles):
        return True
        
    # Four Concealed Pungs must be self-drawn
    if self_drawn and check_four_concealed_pungs(tiles, True):
        return True
        
    # These patterns can be claimed from discard
    if check_big_four_winds(tiles):
        return True
        
    if check_big_three_dragons(tiles):
        return True
        
    if check_all_honors(tiles):
        return True
        
    if check_all_terminals(tiles):
        return True
        
    if check_all_green(tiles):
        return True
    
    return False