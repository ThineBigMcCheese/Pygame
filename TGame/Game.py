import pygame
import sys
import os

print("Python is currently looking here:", os.getcwd())

pygame.init()
pygame.font.init()
my_font = pygame.font.Font("TGame/upheavtt.ttf", 32)

WIDTH, HEIGHT = 1600, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Saac")

# 3. Define Color Palettes (RGB Format)
BG_COLOR = (0, 0, 0)       # Dark slate blue
TEXT_COLOR = (230, 235, 240)   # Off-white
ACCENT_COLOR = (242, 174, 46)  # Warm gold
HOVER_COLOR = (194, 63, 56)    # Deep red

# 4. Set Up Fonts
# Pygame uses system fonts or loaded TTF files
FONT_TITLE = pygame.font.SysFont("upheaval", 36, bold=True)
FONT_BODY = pygame.font.SysFont("upheaval", 22)

# 5. Define Game State and Narrative Data
# The story graph uses unique keys to link scenes and decisions
story_scenes = {
    "start": {
        "text": "You wake up in a damp stone cell. A heavy iron door is locked before you, but you notice a loose brick near the floor. What do you do?",
        "choices": [
            {"text": "1. Inspect the loose brick", "next_scene": "brick"},
            {"text": "2. Call out for help", "next_scene": "call_help"}
        ]
    },
    "brick": {
        "text": "Behind the brick, you discover a rusted iron key! It perfectly fits into the door lock. You turn it and step into a dark corridor.",
        "choices": [
            {"text": "1. Move quietly down the left hall", "next_scene": "win"},
            {"text": "2. Charge blindly down the right hall", "next_scene": "lose_trap"}
        ]
    },
    "call_help": {
        "text": "Your echoes wake a sleeping goblin guard nearby. He opens the cell door with his sword drawn. You have no weapon to defend yourself.",
        "choices": [
            {"text": "1. Attempt to run past him", "next_scene": "lose_guard"},
            {"text": "2. Try to negotiate", "next_scene": "lose_guard"}
        ]
    },
    "win": {
        "text": "You successfully navigate the corridors and find a hidden exit leading to the outer forest. You are free! Game Won.",
        "choices": [{"text": "Press ENTER to play again.", "next_scene": "start"}]
    },
    "lose_trap": {
        "text": "You trip over a hidden wire, triggering a pitfall trap. You fall into the darkness. Game Over.",
        "choices": [{"text": "Press ENTER to try again.", "next_scene": "start"}]
    },
    "lose_guard": {
        "text": "The guard swiftly overpowers you. You are tossed deeper into the dungeons, never to escape. Game Over.",
        "choices": [{"text": "Press ENTER to try again.", "next_scene": "start"}]
    }
}

# Global State Tracker
current_scene_key = "start"

def wrap_text(text, font, max_width):
    """Splits a long string into multiple lines based on maximum pixel width."""
    words = text.split(' ')
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        # Measure line width in pixels
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines

def render_game():
    """Clears the screen and draws text structures for the current scene."""
    SCREEN.fill(BG_COLOR)
    scene = story_scenes[current_scene_key]
    
    # Render and Wrap Main Story Block
    wrapped_story = wrap_text(scene["text"], FONT_BODY, WIDTH - 100)
    current_y = 80
    
    for line in wrapped_story:
        text_surface = FONT_BODY.render(line.strip(), True, TEXT_COLOR)
        SCREEN.blit(text_surface, (50, current_y))
        current_y += 35
        
    # Render Choice Options Interactively
    current_y += 50
    mouse_pos = pygame.mouse.get_pos()
    
    for i, choice in enumerate(scene["choices"]):
        # Create a bounding box rectangle for mouse collision checks
        choice_surface = FONT_BODY.render(choice["text"], True, ACCENT_COLOR)
        choice_rect = choice_surface.get_rect(topleft=(50, current_y))
        
        # Highlight text if the user hovers over it
        if choice_rect.collidepoint(mouse_pos):
            choice_surface = FONT_BODY.render(choice["text"], True, HOVER_COLOR)
            
        SCREEN.blit(choice_surface, (50, current_y))
        current_y += 45

    pygame.display.flip()

def handle_choice_click(mouse_pos):
    """Processes mouse clicks on decision text branches."""
    global current_scene_key
    scene = story_scenes[current_scene_key]
    
    # Recalculate positions matching the renderer to detect specific clicks
    # Start checking exactly where the choices begin on screen
    wrapped_story = wrap_text(scene["text"], FONT_BODY, WIDTH - 100)
    current_y = 80 + (len(wrapped_story) * 35) + 50
    
    for choice in scene["choices"]:
        choice_surface = FONT_BODY.render(choice["text"], True, ACCENT_COLOR)
        choice_rect = choice_surface.get_rect(topleft=(50, current_y))
        
        if choice_rect.collidepoint(mouse_pos):
            current_scene_key = choice["next_scene"]
            break
        current_y += 45

# 6. Primary Interactive Game Loop
clock = pygame.time.Clock()

while True:
    render_game()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse click
                handle_choice_click(event.pos)
                
        elif event.type == pygame.KEYDOWN:
            # Shortcut mapping: Keys '1' or '2' jump to choices instantly
            scene = story_scenes[current_scene_key]
            if event.key == pygame.K_1 and len(scene["choices"]) >= 1:
                current_scene_key = scene["choices"][0]["next_scene"]
            elif event.key == pygame.K_2 and len(scene["choices"]) >= 2:
                current_scene_key = scene["choices"][1]["next_scene"]
            elif event.key == pygame.K_RETURN and current_scene_key in ["win", "lose_trap", "lose_guard"]:
                current_scene_key = "start"

    # Caps frame rendering rate to 30 frames per second
    clock.tick(30)