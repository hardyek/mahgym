class Agent:
    def __init__(self, seat: int):
        self._seat = seat

    def make_discard(self) -> int:
        return 0

    def make_pickup(self, interupt) -> int:
        return 0

    def make_promote(self) ->  int:
        return 0