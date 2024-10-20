to_shorthand = {
    1 : "n1",
    2 : "n2",
    3 : "n3",
    4 : "n4",
    5 : "n5",
    6 : "n6",
    7 : "n7",
    8 : "n8",
    9 : "n9",

    10 : "b1",
    11 : "b2",
    12 : "b3",
    13 : "b4",
    14 : "b5",
    15 : "b6",
    16 : "b7",
    17 : "b8",
    18 : "b9",

    19 : "c1",
    20 : "c2",
    21 : "c3",
    22 : "c4",
    23 : "c5",
    24 : "c6",
    25 : "c7",
    26 : "c8",
    27 : "c9",

    28 : "wn",
    29 : "we",
    30 : "ws",
    31 : "ww",

    32 : "dw",
    33 : "dg",
    34 : "dr",

    35 : "f1e",
    36 : "f2s",
    37 : "f3w",
    38 : "f4n",
    39 : "s1e",
    40 : "s2s",
    41 : "s3w",
    42 : "s4n"
}

index_to_wind = {
    0 : "East",
    1 : "South",
    2 : "West",
    3 : "North"
}

def array_to_shorthand(array):
    array_shorthand = []
    for tile in array:
        array_shorthand.append(to_shorthand[tile])
    return array_shorthand