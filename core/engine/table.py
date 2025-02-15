from typing import List, Dict, Type

from scoring import ScoringInfo

from main import Game
from ..agents import Agent

class Table:
    def __init__(self, agent_array: List[Type[Agent]], num_games: int, base_points: int = 1):
        self.agents = agent_array
        self.num_games = num_games
        self.base_points = base_points  # Base points for scoring
        
        self.scores = [0] * 4
        self.chips = [0] * 4  # Track chips/money separately from points
        self.current_game = 0
        self.game_records = []

    def _calculate_payments(self, winner: int, points: int, scoring_info: ScoringInfo):
        if scoring_info.is_self_drawn:
            # In self-drawn wins, everyone pays
            base_payment = self.base_points * points
            dealer_payment = base_payment * 2
            
            for i in range(4):
                if i == winner:
                    continue
                    
                if scoring_info.is_dealer:
                    # If dealer wins self-drawn, others pay double
                    self.chips[i] -= dealer_payment
                    self.chips[winner] += dealer_payment
                else:
                    # If dealer loses to self-drawn, they pay double
                    if i == 0:  # dealer pays double
                        self.chips[i] -= dealer_payment
                        self.chips[winner] += dealer_payment
                    else:  # others pay normal
                        self.chips[i] -= base_payment
                        self.chips[winner] += base_payment
                        
        else:
            # In discard wins, only discarder pays
            base_payment = self.base_points * points
            discarder = scoring_info.discarder
            
            if scoring_info.is_dealer:
                # If dealer wins from discard, payment is doubled
                self.chips[discarder] -= base_payment * 2
                self.chips[winner] += base_payment * 2
            elif discarder == 0:
                # If dealer pays for discard, payment is doubled
                self.chips[discarder] -= base_payment * 2
                self.chips[winner] += base_payment * 2
            else:
                # Normal discard payment
                self.chips[discarder] -= base_payment
                self.chips[winner] += base_payment

    def play_games(self) -> Dict:
        while self.current_game < self.num_games:
            round_wind = 31 + (self.current_game // 4)

            game = Game(self.agents, round_wind)
            game._initialise_game()
            result = game._main_loop()
            
            self.game_records.append(game.data)
            
            if result['result'] == 'win':
                winner = result['winner']
                points = result['points']
                self.scores[winner] += points
                
                # Calculate chip payments
                self._calculate_payments(
                    winner=winner,
                    points=points,
                    is_self_drawn=result['scoring_info'].is_self_drawn,
                    is_dealer_win=game.players[winner].wind == 0
                )
                
                # Check if winner was dealer
                if game.players[winner].wind == 0:
                    pass  # Keep same positions
                else:
                    self.current_game += 1  # Only increment game count on non-dealer wins
            else:  # Draw
                self.current_game += 1
        
        return {
            'final_scores': self.scores,
            'games_played': self.current_game,
            'game_records': self.game_records,
            'final_chips': self.chips
        }   