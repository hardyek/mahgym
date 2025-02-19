from ..engine.player import Player

from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class PlayerObservation:
    wind: int
    num_tiles: int
    exposed: List[List[int]]
    specials: List[int]
    is_dealer: bool

@dataclass
class GameObservation:
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

class Agent(Player):
    def __init__(self, seat: int):
        super().__init__(seat)

    def _create_observation(self, game_state) -> GameObservation:
        other_players = []
        for i in range(1, 4):
            i = (self.seat + i) % 4
            player = game_state.players[i]
            other_players.append(PlayerObservation(
                wind=player.wind,
                num_tiles=len(player.hand),
                exposed_melds=player.exposed,
                specials=player.specials,
                is_dealer=player.wind == 0
            ))
        
        return GameObservation(
            hand=self.hand.copy(),
            round_wind=game_state.round_wind,
            player_seat=self.seat,
            current_player=game_state.current_player,
            takable_tile=game_state.takable if game_state.takable != -1 else None,
            deck_size=len(game_state.deck),
            discard_pile=game_state.pile.copy(),
            other_players=other_players,
            last_gong_made=game_state.last_gong_made,
            last_gong_player=game_state.last_gong_player
        )
    
    # FOR TYPING / DEBUGGING IN engine

    def make_discard(self, game) -> int:
        obs = self._create_observation(game)
        return 0

    def make_pickup(self, interupt, game) -> int:
        obs = self._create_observation(game)
        return 0

    def make_promote(self, game) ->  int:
        obs = self._create_observation(game)
        return 0