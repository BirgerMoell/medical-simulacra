# Constants
TILE_SIZE = 60
WORLD_WIDTH, WORLD_HEIGHT = 20, 15
SCREEN_WIDTH, SCREEN_HEIGHT = WORLD_WIDTH * TILE_SIZE, WORLD_HEIGHT * TILE_SIZE

# Colors
BACKGROUND_COLOR = (144, 201, 120)
TEXT_COLOR = (0, 0, 0)
USER_BUBBLE_COLOR = (255, 255, 255)
NPC_BUBBLE_COLOR = (255, 255, 200)
BUBBLE_OUTLINE_COLOR = (0, 0, 0)

# Dialogue setup
DIALOGUE_DURATION = 3000  # Duration to show dialogue in milliseconds

# Font setup
FONT_SIZE = 18

# Image paths
PLAYER_IMAGE_PATH = 'sprites/person.webp'
TILE_IMAGE_PATH = 'sprites/grass2.webp'
DOCTOR_IMAGES = [
    'sprites/doctor_2.webp',
    'sprites/doctor_3.webp',
    'sprites/nurse.webp'
]