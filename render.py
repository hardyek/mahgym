from src.renderer import MahjongRenderer
import pygame
from src.game import MahjongGame

renderer = MahjongRenderer()
game = MahjongGame()
game.initialise_game()

clock = pygame.time.Clock()

renderer.render_game(game)

winner = game.game_loop_rendered(renderer,clock)

print(f"Player {winner} has won.")

pygame.quit()