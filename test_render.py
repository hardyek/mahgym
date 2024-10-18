from src.renderer import MahjongRenderer
import pygame
from src.game import MahjongGame

renderer = MahjongRenderer()
game = MahjongGame()
game.initialise_game()

running = True
clock = pygame.time.Clock()

renderer.render_game(game)

while running:
    running = renderer.handle_events()
    
    # Update game state here
    game.play_turn()
    renderer.render_game(game)
    print(game.pile)
    
    clock.tick(15)  # Limit to 60 frames per second

pygame.quit()