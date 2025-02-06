from typing import List, Dict, Set, Tuple
from collections import Counter
from dataclasses import dataclass

@dataclass
class ScoringInfo:
    concealed_hand: List[int]
    exposed_melds: List[List[int]]
    specials: List[int]
    winning_tile: int
    is_self_drawn: bool
    is_last_tile: bool
    is_robbing_gong: bool
    is_last_gong: bool
    seat_wind: int
    round_wind: int
    declared_gongs: List[List[int]]  # List of gong tiles
    is_dealer: bool

def get_pairs_and_sets(tiles: List[int]) -> Tuple[List[List[int]], List[int]]:
    counts = Counter(tiles)
    pairs = []
    sets = []
    
    # Find pairs
    for tile, count in counts.items():
        if count >= 2:
            pairs.append([tile, tile])
            
    # Find pungs
    for tile, count in counts.items():
        if count >= 3:
            sets.append([tile] * 3)
            
    # Find soengs
    for suit in [0, 1, 2]:  # Characters, Circles, Bamboo
        base = suit * 10
        suited_tiles = [t for t in tiles if base <= t < base + 10]
        for i in range(1, 8):
            if (base + i in suited_tiles and 
                base + i + 1 in suited_tiles and 
                base + i + 2 in suited_tiles):
                sets.append([base + i, base + i + 1, base + i + 2])
                
    return sets, pairs


def score(info: ScoringInfo) -> int:
    points = 0 

    # Base points
    points += 1

    all_tiles = info.concealed_hand.copy()
    for meld in info.exposed_melds():
        all_tiles.extend(meld)

    # Dragon pungs
    dragon_counts = Counter(t for t in all_tiles if 41 <= t <= 43)
    for count in dragon_counts.values():
        if count >= 3:
            points += 1

    # Seat/round wind pungs
    if Counter(t for t in all_tiles if t == info.seat_wind + 30)[info.seat_wind + 30] >= 3:
        points += 1
    if Counter(t for t in all_tiles if t == info.round_wind)[info.round_wind] >= 3:
        points += 1

    # Clean hand
    suited_tiles = [(t//10, t%10) for t in all_tiles if t < 30]
    if suited_tiles:
        suits = {t[0] for t in suited_tiles}
        if len(suits) == 1:
            points += 3

    # All pongs
    concealed_sets, pairs = get_pairs_and_sets(info.concealed_hand)
    if all(len(meld) == 3 and len(set(meld)) == 1 for meld in (concealed_sets + info.exposed_melds)):
        points += 3

    # Additional points
    points += len(info.declared_gongs)  # Gongs
    points += len(info.specials)  # Flowers and seasons 

    # Special conditions
    if info.is_self_drawn: 
        points += 1
    if info.is_last_tile:
        points += 1
    if info.is_robbing_gong:
        points += 1
    if info.is_last_gong:
        points += 1
    if info.is_dealer:
        points += 1
        
    return points
