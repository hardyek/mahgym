from typing import List

def is_winning_hand(hand: List[int], exposed: List[List[int]]) -> bool:
    sorted_hand = sorted(hand)
                                           # thirteen orphans tiles set
    if len(exposed) == 0 and set(hand) ==  {1,9,11,19,21,29,31,32,33,34,41,42,43}:
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
