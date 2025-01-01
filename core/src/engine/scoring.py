from typing import List, Dict, Set, Tuple
from collections import Counter

special_hands = {
    'small_dragons': {'dragons': 2, 'score': 5},  # 2 dragon pungs + pair
    'big_dragons': {'dragons': 3, 'score': 8},    # All 3 dragon pungs
    'small_winds': {'winds': 3, 'score': 6},      # 3 wind pungs
    'big_winds': {'winds': 4, 'score': 10},       # All 4 wind pungs
    'all_honors': {'score': 10},
    'all_terminals': {'score': 10}, 
    'thirteen_orphans': {'tiles': {1,9,11,19,21,29,31,32,33,34,41,42,43}, 'score': 13},
    'all_pungs': {'score': 3},
    'clean_suit': {'score': 7},
    'all_green': {'score': 8},  # Only green tiles
    'nine_gates': {'score': 11},  # 1112345678999 in one suit
    'mixed_suit': {'score': 3}  # One suit + honors
}

def is_winning_hand(hand: List[int], exposed: List[List[int]]) -> bool:
    sorted_hand = sorted(hand)

    if len(exposed) == 0 and set(hand) == special_hands['thirteen_orphans']['tiles']:
        return True
    
    for tile in set(sorted_hand):
        if sorted_hand.count(tile) >= 2:
            remaining = sorted_hand[:]
            remaining.remove(tile)
            remaining.remove(tile)
            if can_form_four_sets(remaining, exposed):
                return True
    return False

def can_form_four_sets(hand: List[int], exposed: List[List[int]]) -> bool:
    sets_needed = 4 - len(exposed)
    if sets_needed == 0:
        return len(hand) == 0
        
    hand = sorted(hand)
    if len(hand) < 3:
        return False
        
    # Try PUNG
    if hand[0] == hand[1] == hand[2]:
        if can_form_four_sets(hand[3:], exposed + [[hand[0]]*3]):
            return True
            
    # Try SOENG
    if hand[0] + 1 in hand and hand[0] + 2 in hand:
        new_hand = hand[:]
        for i in range(3):
            new_hand.remove(hand[0] + i)
        if can_form_four_sets(new_hand, exposed + [[hand[0], hand[0]+1, hand[0]+2]]):
            return True
            
    return False

def score(tiles: List[int,List[int]], own_wind: int = None, round_wind: int = None, last_tile: bool = False) -> int:
    def flatten(tiles, flattened=None, all_concealed=True) -> Tuple[List[int], bool]:
        if flattened is None:
            flattened = []
        for item in tiles:
            if isinstance(item, int):
                flattened.append(item)
            else:
                flatten(item, flattened, False)
        return flattened, all_concealed
    hand, all_concealed = flatten(tiles)

    score = 0

    if set(hand) == special_hands['thirteen_orphans']['tiles']:
       return special_hands['thirteen_orphans']['score']

    dragons = [t for t in range(41,44) if hand.count(t) >= 3]
    dragon_pairs = [t for t in range(41,44) if hand.count(t) == 2]
    winds = [t for t in range(31,35) if hand.count(t) >= 3]
    wind_pairs = [t for t in range(31,35) if hand.count(t) == 2]
    suits = {t//10 for t in hand if t < 31}

    score += len(dragons) * 2 
    score += len(winds) * 2
    score += len(dragon_pairs)
    score += sum(1 for t in wind_pairs if t == own_wind or t == round_wind)

    score += sum(1 for t in hand if t < 31 and t%10 in (1,9) and hand.count(t) >= 3)


     # Special hands
    if len(dragons) == 3:
        score += special_hands['big_dragons']['score']
    elif len(dragons) == 2 and dragon_pairs:
        score += special_hands['small_dragons']['score']

    if len(winds) == 4:
        score += special_hands['big_winds']['score']
    elif len(winds) == 3:
        score += special_hands['small_winds']['score']
    
    if all(t >= 31 for t in hand):
        score += special_hands['all_honors']['score']

    if all(t%10 in (1,9) for t in hand if t < 31):
        score += special_hands['all_terminals']['score']

    if len(suits) == 1:
        score += special_hands['clean_suit']['score']
    elif len(suits) == 1 and any(t >= 31 for t in hand):
        score += special_hands['mixed_suit']['score']

    if all(t in [22,23,24,26,28,42] for t in hand):
        score += special_hands['all_green']['score']

    if all(any(hand.count(t) >= n for t in hand) for n in [3,3,3,3,2]):
        score += special_hands['all_pungs']['score']

    if all_concealed:
        score += 1
    
    if last_tile:
        score += 1

    return min(score, 13)

    

