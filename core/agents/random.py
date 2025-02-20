"""
Random agent class
"""
from ._agent import Agent

import random

class Random(Agent):
    def __init__(self, seat: int):
        super().__init__(seat)

    def make_discard(self, game) -> int:
        obs = self._create_observation(game)
        hand_length = len(obs.hand)
        action = random.randint(0,hand_length-1)
        return action

    def make_pickup(self, interupt, game) -> int:
        obs = self._create_observation(game)
        action = random.randint(0,1)
        return action

    def make_promote(self, game) ->  int:
        obs = self._create_observation(game)
        action = random.randint(0,1)
        return action