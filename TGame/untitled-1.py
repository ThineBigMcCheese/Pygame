import pygame
import random
import sys

# 1. Initialize Pygame
pygame.init()

# 2. Configuration Settings
TILE_SIZE = 32
MAP_WIDTH = 25   # Number of tiles horizontally
MAP_HEIGHT = 18  # Number of tiles vertically

SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE
screen = pygame.display.set_addr_size if hasattr(pygame.display, 'set_addr_size') else pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Random Map Generator")

# 3. Define Color Constants (Using colors as tile stand-ins)
WATER = (34, 100, 200)   # Blue
SAND = (230, 210, 160)    # Yellow-ish
GRASS = (46, 139, 87)    # Green
MOUNTAIN = (100, 100, 100) # Gray

# Define tile type mappings and spawn probabilities
TILE_TYPES = {
    0: WATER,
    1: SAND,
    2: GRASS,
    3: MOUNTAIN
}

def generate_random_map(width, height):
    """Generates a 2D grid filled with random tile ID integers."""
    # Using random.choices allows you to assign specific weights to each tile type
    tile_pool = [0, 1, 2, 3]
    spawn_weights = [0.15, 0.10, 0.60, 0.15] # 60% grass, 15% water, etc.
    
    game_map = []
    for row in range(height):
        row_data = random.choices(tile_pool, weights=spawn_weights, k=width)
        game_map.append(row_data)
    return game_map

def draw_map(surface, game_map):
    """Iterates through the 2D grid and draws rects representing tiles."""
    for row_idx, row in enumerate(game_map):
        for col_idx, tile_id in enumerate(row):
            # Calculate pixel positions
            x = col_idx * TILE_SIZE
            y = row_idx * TILE_SIZE
            
            # Fetch color corresponding to tile ID
            tile_color = TILE_TYPES.get(tile_id, GRASS)
            
            # Draw the tile surface
            tile_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface, tile_color, tile_rect)

# 4. Main Game Loop Setup
game_map = generate_random_map(MAP_WIDTH, MAP_HEIGHT)
clock = pygame.time.Clock()

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Press Spacebar to generate a completely new random map
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_map = generate_random_map(MAP_WIDTH, MAP_HEIGHT)
                
    # Rendering
    screen.fill((0, 0, 0))
    draw_map(screen, game_map)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()