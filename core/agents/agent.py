from ..engine.player import Player

class Agent(Player):
    def __init__(self):
        super(Agent, self).__init__()
        self.score: int = 0
        
    def make_discard(self) -> int:
        return 0

    def make_pickup(self, interupt) -> int:
        return 0

    def make_promote(self) ->  int:
        return 0