"""
Template class for any Agent implementation
"""
from ._agent import Agent

class Template(Agent):
    def __init__(self, seat: int):
        super().__init__(seat)

    """
    obs object is a dataclass with the following fields:

    class GameObservation
    hand: List[int]
    round_wind: int
    seat: int
    current_player: int
    takable: Optional[int]
    deck_length: int
    discard_pile: List[int]
    other_players: List[PlayerObservation]
    last_gong_made: bool
    last_gong_player: int

    class PlayerObservation
    wind: int
    num_tiles: int
    exposed: List[List[int]]
    specials: List[int]
    is_dealer: bool
    """
    
    """
    Following three functions are how agent behaviour is defined.
    """

    def make_discard(self, game) -> int:
        obs = self._create_observation(game)
        return 0

    def make_pickup(self, interupt, game) -> int:
        obs = self._create_observation(game)
        return 0

    def make_promote(self, game) ->  int:
        obs = self._create_observation(game)
        return 0