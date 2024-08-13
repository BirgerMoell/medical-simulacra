import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, PLAYER_IMAGE_PATH, TILE_IMAGE_PATH, DOCTOR_IMAGES, FONT_SIZE
from game_objects import Player, Doctor
from rendering import load_image, draw_game
from dialogue_manager import DialogueManager
from event_handler import EventHandler

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Small World Game with Specialized Doctors")

    # Initialize font after pygame is initialized
    font = pygame.font.Font(None, FONT_SIZE)

    tile_image = load_image(TILE_IMAGE_PATH, (TILE_SIZE, TILE_SIZE))
    player = Player(5, 7, PLAYER_IMAGE_PATH)
    doctors = [
        Doctor(8, 7, DOCTOR_IMAGES[0], "Dr. Smith", "General Medicine"),
        Doctor(12, 10, DOCTOR_IMAGES[1], "Dr. Johnson", "Emergency Medicine"),
        Doctor(16, 5, DOCTOR_IMAGES[2], "Dr. Williams", "Licensed clinical psychologist")
    ]

    dialogue_manager = DialogueManager()
    event_handler = EventHandler(player, dialogue_manager)

    clock = pygame.time.Clock()
    running = True

    while running:
        running = event_handler.handle_events()
        event_handler.check_proximity(doctors)

        # Removed the call to dialogue_manager.update_dialogue()

        draw_game(screen, tile_image, player, doctors, 
                  dialogue_manager, 
                  event_handler.is_input_active(), 
                  event_handler.get_user_input(),
                  font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()