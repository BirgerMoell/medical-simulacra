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
        Doctor(4, 3, DOCTOR_IMAGES[1], "Dr. Johnson", "Emergency Medicine"),
        Doctor(SCREEN_WIDTH // TILE_SIZE - 4, 3, DOCTOR_IMAGES[2], "Dr. Williams", "General Practice")
    ]

    dialogue_manager = DialogueManager()
    event_handler = EventHandler(player, dialogue_manager)

    clock = pygame.time.Clock()
    running = True

    while running:
        running = event_handler.handle_events()
        event_handler.check_proximity(doctors)
        dialogue_manager.update_dialogue()

        current_dialogue = dialogue_manager.get_current_dialogue()
        if current_dialogue:
            print(f"Current dialogue: {current_dialogue}")  # Debug print

        draw_game(screen, tile_image, player, doctors, 
                  current_dialogue, 
                  event_handler.is_input_active(), 
                  event_handler.get_user_input(),
                  font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()