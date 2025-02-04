from typing import List, Dict, Optional
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

def score(info: ScoringInfo):
    pass