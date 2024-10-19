import pygame
from typing import List, Dict
from src.player import Player
from src.game import MahjongGame
from src.utils import array_to_shorthand

class MahjongRenderer:
    def __init__(self, screen_width: int = 1400, screen_height: int = 600):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Mahgym")
        
        self.tile_width = 50 * 1.3
        self.tile_height = 61 * 1.3
        self.padding = 2

        self.tile_images: Dict[int, pygame.Surface] = self.load_tile_images()
        self.font = pygame.font.SysFont ("Helvetica", 24)

        self.colors = {
            'background': (255,255,255),
            'box': (255,255,255),
            'text': (0,0,0),
            'unexposed_tile' : (0,0,255), # Blue
            'exposed_meld': (255, 0, 0),  # Red
            'current_player': (214, 67, 214),  # Pink
            'current_player_background': (240, 240, 240),
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
            player_y = i * (self.tile_height + self.padding)
            player_color_background = self.colors['current_player_background'] if i == current_player else self.colors['background']
            player_color_text = self.colors['current_player'] if i == current_player else self.colors['text']
            pygame.draw.rect(self.screen, player_color_background, (0, player_y, self.tile_width, self.tile_height))
            self.screen.blit(self.font.render(f"P{i}", True, (player_color_text)), (10, player_y + 10))
            
            self.render_hand(player.hand, self.tile_width, player_y, player.exposed)
            self.render_specials(player.specials, player_y)

    def render_hand(self, hand: List[int], x: int, y: int, exposed_melds: List[List[int]]):
        exposed_tiles = [tile for meld in exposed_melds for tile in meld]
        for i, tile in enumerate(hand):
            tile_x = x + i * self.tile_width
            exposed_tile_x = tile_x + self.tile_width
            pygame.draw.rect(self.screen, self.colors['unexposed_tile'], (tile_x, y, self.tile_width, self.tile_height))
            self.screen.blit(self.tile_images[tile], (tile_x, y))
        for i, tile in enumerate(exposed_tiles):
            tile_x = exposed_tile_x + i * self.tile_width
            pygame.draw.rect(self.screen, self.colors['exposed_meld'], (tile_x, y, self.tile_width, self.tile_height))
            self.screen.blit(self.tile_images[tile], (tile_x, y))
        

    def render_specials(self, specials: List[Player], y: int):
        specials_x = 16 * self.tile_width  # Start right after the deck
        for i, tile in enumerate(specials):
            tile_x = specials_x + i * self.tile_width
            pygame.draw.rect(self.screen, self.colors["box"], (tile_x, y, self.tile_width, self.tile_height))
            self.screen.blit(self.tile_images[tile], (tile_x, y))

    def render_deck(self, deck: List[int]):
        deck_y = 4.5 * (self.tile_height + self.padding)
        self.screen.blit(self.font.render("Deck", True, (self.colors["text"])), (10, deck_y - 30))
        for i, tile in enumerate(deck[:15]):  # Show next 10 tiles
            tile_x = i * self.tile_width
            pygame.draw.rect(self.screen, self.colors['box'], (tile_x, deck_y, self.tile_width, self.tile_height))
            self.screen.blit(self.tile_images[tile], (tile_x, deck_y))

    def render_discard_pile(self, pile: List[int], takable: int):
        pile_y = 6 * (self.tile_height + self.padding)
        self.screen.blit(self.font.render("Pile", True, (self.colors["text"])), (10, pile_y - 30))
        for i, tile in enumerate(reversed(pile[-15:])):  # Show last 10 tiles in reverse order
            tile_x = i * self.tile_width
            box_color = self.colors['takable'] if i == 0 and tile == takable else self.colors['box']
            pygame.draw.rect(self.screen, box_color, (tile_x, pile_y, self.tile_width, self.tile_height))
            self.screen.blit(self.tile_images[tile], (tile_x, pile_y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True