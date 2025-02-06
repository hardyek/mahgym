from typing import List, Dict, Type

from main import Game

from ..agents import Agent

class Table:
    def __init__(self, agent_array: List[Type[Agent]], num_games: int):
        self.agents = agent_array
        self.num_games = num_games

        self.scores = [0] * 4
        self.current_game = 0
        self.game_records = []

    def play_games(self) -> Dict:
        while self.current_game < self.num_games:

            round_wind = 31 + (self.round_number // 4)

            game = Game(self.agents, round_wind)
            game._initialise_game()

            result = game._main_loop()

            self.game_records.append(game.data)

            if result['result'] == 'win':
                winner = result['winner']
                points = result['points']
                self.scores[winner] += points
                
                # Check if winner was dealer (wind 0)
                if game.players[winner].wind == 0:
                    # If dealer wins, keep same wind
                    pass
                else:
                    # If non-dealer wins, rotate winds
                    self._rotate_winds()
            else:  # Draw
                self._rotate_winds()
            
            self.current_game += 1

        return {
            'final_scores': self.scores,
            'games_played': self.current_game,
            'game_records': self.game_records
        }
    
    def _rotate_winds(self):
        # After each non-dealer win or draw, rotate player positions
        self.agents = self.agents[1:] + [self.agents[0]]
        
        # After a complete rotation (when first player returns to dealer),
        # change the round wind
        if self.current_game % 4 == 3:
            if self.round_wind == 31:    # North -> East
                self.round_wind = 32
            elif self.round_wind == 32:  # East -> South
                self.round_wind = 33
            elif self.round_wind == 33:  # South -> West
                self.round_wind = 34
            else:                        # West -> North
                self.round_wind = 31
        