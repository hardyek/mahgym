"""
Human agent class
"""
from ._agent import Agent

class Human(Agent):
    def __init__(self, seat: int):
        super().__init__(seat)

    def make_discard(self, game) -> int:
        obs = self._create_observation(game)
        action = int(input("Enter discard action: "))
        return action

    def make_pickup(self, interupt, game) -> int:
        obs = self._create_observation(game)
        action = int(input("Enter pickup action: "))
        return action

    def make_promote(self, game) ->  int:
        obs = self._create_observation(game)
        action = int(input("Enter promote action: "))
        return action