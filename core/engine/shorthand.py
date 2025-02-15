to_shorthand = {
    # Characters
    1: "n1", 2: "n2", 3: "n3", 4: "n4", 5: "n5", 6: "n6", 7: "n7", 8: "n8", 9: "n9",
    # Circles
    11: "c1", 12: "c2", 13: "c3", 14: "c4", 15: "c5", 16: "c6", 17: "c7", 18: "c8", 19: "c9",
    # Bamboo
    21: "b1", 22: "b2", 23: "b3", 24: "b4", 25: "b5", 26: "b6", 27: "b7", 28: "b8", 29: "b9",
    # Winds
    31: "w1", # North
    32: "w2",# East
    33: "w3", # South
    34: "w4", # West
    # Dragons
    41: "d1", # White
    42: "d2", # Green
    43: "d3", # Red
    # Specials
    # Flowers
    51: "f1",
    52: "f2",
    53: "f3",
    54: "f4",
    # Seasons
    61: "s1",
    62: "s2",
    63: "s3",
    64: "s4"
}

def meld_to_shorthand(meld):
    str = ""
    for tile in meld:
        str += to_shorthand[tile]
    return str
