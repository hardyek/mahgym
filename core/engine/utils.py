from typing import List, Tuple

from collections import Counter

from .player import Player

def can_form_four_melds(hand: List[int], exposed: List[List[int]]) -> bool:
    """

    Checks if the list of tiles in hand and exposed melds together make 4 valid melds.

    Args:
        hand (List[int]): The players hand.
        exposed (List[List[int]]): The list of pre-exposed melds of the player.

    Returns:
        bool: Y/N
    """
    sets_needed = 4 - len(exposed)
    if sets_needed == 0:
        return len(hand) == 0

    hand = sorted(hand)
    if len(hand) < 3:
        return False

    # Try PUNG
    if hand[0] == hand[1] == hand[2]:
        if can_form_four_melds(hand[3:], exposed + [[hand[0]]*3]):
            return True

    # Try SOENG
    if hand[0] + 1 in hand and hand[0] + 2 in hand:
        new_hand = hand[:]
        for i in range(3):
            new_hand.remove(hand[0] + i)
        if can_form_four_melds(new_hand, exposed + [[hand[0], hand[0]+1, hand[0]+2]]):
            return True

    return False

def check_thirteen_orphans(tiles: List[int]) -> bool:
    terminals = [1, 9, 11, 19, 21, 29]  # 1s and 9s of each suit
    honors = [31, 32, 33, 34, 41, 42, 43]  # Winds and dragons
    required = terminals + honors
    
    # Must have all required tiles plus one duplicate
    return all(t in tiles for t in required) and len(tiles) == 14

def check_seven_pairs(tiles: List[int]) -> bool:
    if len(tiles) != 14:
        return False
    counts = Counter(tiles)
    return all(count == 2 for count in counts.values()) and len(counts) == 7

def check_pure_terminals(tiles: List[int]) -> bool:
    valid_tiles = {1, 9, 11, 19, 21, 29}
    return all(tile in valid_tiles for tile in tiles) and len(tiles) == 14

def check_pure_terminals_and_honors(tiles: List[int]) -> bool:
    valid_tiles = {1, 9, 11, 19, 21, 29}  # Terminals
    valid_tiles.update(range(31, 35))  # Winds
    valid_tiles.update(range(41, 44))  # Dragons
    return all(tile in valid_tiles for tile in tiles) and len(tiles) == 14

def check_special_patterns(tiles: List[int], self_drawn) -> bool:
    """

    Do the input tiles make up one of the specified special winning hands.

    Args:
        tiles (List[int]): 14 Tiles that might make up a special winning hand

    Returns:
        bool
    """
    if check_thirteen_orphans(tiles):
        return True
    if check_seven_pairs(tiles) and self_drawn:
        return True
    if check_pure_terminals(tiles):
        return True
    if check_pure_terminals_and_honors(tiles):
        return True
    return False

def is_valid_14(hand: List[int], exposed: List[List[int]]) -> bool:
    """

    Does the player have a valid set of 14 tiles (forming 4 valid melds) to declare mahjong,

    Note that it may not be 14 due to gongs but it is effectively 14.

    Args:
        hand (List[int]): The players hand.
        exposed (List[List[int]]): The list of pre-exposed melds of the player.

    Returns:
        bool: Y/N
    """
    sorted_hand = sorted(hand)
                                           # thirteen orphans tiles set
    if len(exposed) == 0 and set(hand) ==  {1,9,11,19,21,29,31,32,33,34,41,42,43}:
        return True

    for tile in set(sorted_hand):
        if sorted_hand.count(tile) >= 2:
            remaining = sorted_hand[:]
            remaining.remove(tile)
            remaining.remove(tile)
            if can_form_four_melds(remaining, exposed):
                return True
    return False

def check_for_valid_14(current_player: int, players: List[Player], takable: int) -> int:
    """

    Checks if any players can for a form a valid set of 14 tiles (see is_valid_14) by picking up the takable tile.

    Args:
        current_player (int): Index of the current player.
        players (List[Player]): List of players.
        takable (int): Tile that is available to be picked up.

    Returns:
        int: The player who can declare mahjong or -1 if not.
    """
    
    if takable == -1:
        if is_valid_14(players[current_player].hand, players[current_player].exposed) or check_special_patterns(players[current_player].hand, True):
            return current_player

    else:
        next_player = (current_player + 1) % 4
        while next_player != current_player:
            test_hand = players[next_player].hand + [takable]
            # In Hong Kong rules, special patterns can be completed by picking up tiles
            if is_valid_14(test_hand, players[next_player].exposed) or check_special_patterns(test_hand, False):
                return next_player
            next_player = (next_player + 1) % 4

    return -1

def build_interupt_queue(tile: int, current_player: int, players: List[Player]) -> List[tuple[int, int, List[int]]]:
    """

    Builds the list of interupts to gameflow that will be possible given the recently discarded tile.

    Args:
        tile (int): Tile that has just been discarded.
        current_player (int): Index of the current player.
        players (List[Player]): List of players.

    Returns:
        List[tuple[int, int, List[int]]]: Interupts formatted as follows in a list (queue based on interupt priority):

        (PLAYER_INDEX, INTERUPT_TYPE, [TILE1, TILE2, TILE3, TILE4(FOR GONG ONLY)])

        INTERUPT_TYPES are as follows 0: PUNG, 1: GONG, 2: SOENG
    """
    interrupts = []
    # Check for PUNG or GONG
    next_player = (current_player + 1) % 4

    while next_player != current_player:
        tiles_in_hand = players[next_player].count_tile(tile)

        if tiles_in_hand == 2:
            interrupts.append((next_player, 0, [tile] * 3)) # 0 for PUNG
        elif tiles_in_hand == 3:
            interrupts.append((next_player, 1, [tile] * 4)) # 1 for GONG
        else:
            # Updgrading a PUNG to a GONG
            for meld in players[next_player].exposed:
                if meld[0] == tile and meld[1] == tile:
                    interrupts.append((next_player, 1, [tile] * 4))

        next_player = (next_player + 1) % 4

    # Check for SOENG
    next_player = (current_player + 1) % 4

    suit_start = (tile // 10) * 10
    sequences = [seq for seq in [[tile-2, tile-1, tile],[tile-1, tile, tile+1],[tile, tile+1, tile+2]] if all(suit_start <= t < suit_start + 10 for t in seq)] # what is readability

    for seq in sequences:
        if players[next_player].has_tiles([t for t in seq if t != tile]):
            interrupts.append((next_player, 2, seq))

    return interrupts

def check_promote_pung(tile: int, player: Player) -> int:
    """
    
    Checks for the condition when a player draws a tile which they have an already exposed pung of at which point they can chose whether to keep the tile in their hand or to use it to "promote" their pung to a gong and draw again.

    Args:
        tile (int): Tile in question.
        player (Player): Player who might be able to make the promotion.

    Returns:
        int: The index of the pung that can be promoted in the players list of exposed melds.
    """
    for i in range(len(player.exposed)):
        if tile == player.exposed[i][0] and tile == player.exposed[i][1]:
            return i
    return -1
