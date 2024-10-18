import pygame
from typing import List, Dict
from src.player import Player
from src.game import MahjongGame
from src.utils import array_to_shorthand

class MahjongRenderer:
    def __init__(self, screen_width: int = 1024, screen_height: int = 768):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Mahgym")
        
        self.tile_width = 40
        self.tile_height = 60
        self.padding = 5
        self.box_size = max(self.tile_width, self.tile_height) + self.padding

        self.tile_images: Dict[int, pygame.Surface] = self.load_tile_images()
        self.font = pygame.font.Font(None, 36)

        self.colors = {
            'background': (255, 255, 255),  # White
            'box': (200, 200, 200),  # Light gray
            'exposed_meld': (230, 230, 250),  # Lavender
            'current_player': (255, 192, 203),  # Pink
            'takable': (144, 238, 144)  # Light green
        }

    def load_tile_images(self) -> Dict[int, pygame.Surface]:
        tile_images = {}
        tile_encodings = array_to_shorthand(range(1, 43))
        for i, encoding in enumerate(tile_encodings):
            image = pygame.image.load(f"tiles/{encoding}.png")
            tile_images[i + 1] = pygame.transform.scale(image, (self.tile_width, self.tile_height))
        return tile_images

    def render_game(self, game: MahjongGame):
        self.screen.fill(self.colors['background'])
        
        self.render_players(game.players, game.current_player)
        self.render_deck(game.deck)
        self.render_discard_pile(game.pile, game.takable)
        
        pygame.display.flip()

    def render_players(self, players: List[Player], current_player: int):
        for i, player in enumerate(players):
            player_y = i * (self.box_size + self.padding)
            player_color = self.colors['current_player'] if i == current_player else self.colors['background']
            pygame.draw.rect(self.screen, player_color, (0, player_y, 50, self.box_size))
            self.screen.blit(self.font.render(f"P{i}", True, (0, 0, 0)), (10, player_y + 10))
            
            self.render_hand(player.hand, 60, player_y, player.exposed_melds)

    def render_hand(self, hand: List[int], x: int, y: int, exposed_melds: List[List[int]]):
        exposed_tiles = [tile for meld in exposed_melds for tile in meld]
        for i, tile in enumerate(hand):
            tile_x = x + i * self.box_size
            box_color = self.colors['exposed_meld'] if tile in exposed_tiles else self.colors['box']
            pygame.draw.rect(self.screen, box_color, (tile_x, y, self.box_size, self.box_size))
            self.screen.blit(self.tile_images[tile], (tile_x + self.padding // 2, y + self.padding // 2))

    def render_deck(self, deck: List[int]):
        deck_y = 5 * (self.box_size + self.padding)
        self.screen.blit(self.font.render("Deck", True, (0, 0, 0)), (10, deck_y - 30))
        for i, tile in enumerate(deck[:10]):  # Show next 10 tiles
            tile_x = i * self.box_size
            pygame.draw.rect(self.screen, self.colors['box'], (tile_x, deck_y, self.box_size, self.box_size))

    def render_discard_pile(self, pile: List[int], takable: int):
        pile_y = 6 * (self.box_size + self.padding)
        self.screen.blit(self.font.render("Pile", True, (0, 0, 0)), (10, pile_y - 30))
        for i, tile in enumerate(reversed(pile[-10:])):  # Show last 10 tiles in reverse order
            tile_x = i * self.box_size
            box_color = self.colors['takable'] if i == 0 and tile == takable else self.colors['box']
            pygame.draw.rect(self.screen, box_color, (tile_x, pile_y, self.box_size, self.box_size))
            self.screen.blit(self.tile_images[tile], (tile_x + self.padding // 2, pile_y + self.padding // 2))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True