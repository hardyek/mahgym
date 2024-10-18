from src.renderer import MahjongRenderer
import pygame
from src.game import MahjongGame
from src.utils import array_to_shorthand, index_to_wind

renderer = MahjongRenderer()
game = MahjongGame()
game.initialise_game()

running = True
clock = pygame.time.Clock()

while running:
    renderer.render_game(game)
    running = renderer.handle_events()
    
    # Update game state here
    
    clock.tick(60)  # Limit to 60 frames per second

pygame.quit()