import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, PLAYER_IMAGE_PATH, TILE_IMAGE_PATH, DOCTOR_IMAGES, FONT_SIZE
from game_objects import Player, Doctor
from rendering import load_image, draw_game
from dialogue_manager import DialogueManager
from event_handler import EventHandler
from ai_integration import call_ai_assistant
from doctor_actions import move_doctor_to_player

def main():
    pygame.init()
    pygame.mixer.init()  # Initialize the mixer for audio   
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Small World Game with Specialized Doctors")

    # Initialize font after pygame is initialized
    font = pygame.font.Font(None, FONT_SIZE)

    tile_image = load_image(TILE_IMAGE_PATH, (TILE_SIZE, TILE_SIZE))
    player = Player(10, 16, PLAYER_IMAGE_PATH)
    doctors = [
        Doctor(8, 7, DOCTOR_IMAGES[0], "Dr. Smith", "General Medicine", "You are an expert in general medicine. Give medical advice to patients. Be concise in your answers. If you are unsure, ask for more information. Always respond and roleplay your role as a medical doctor."),
        Doctor(12, 10, DOCTOR_IMAGES[1], "Dr. Johnson", "Emergency Medicine", "You are an expert in emergency medicine. Give medical advice to patients. Be concise in your answers. If you are unsure, ask for more information. Always respond and roleplay your role as a medical doctor."),
        Doctor(16, 5, DOCTOR_IMAGES[2], "Dr. Williams", "Licensed clinical psychologist", "You are an expert in clinical psycholoy. Give psychological advice to patients. Be concise in your answers. If you are unsure, ask for more information. Always respond and roleplay your role as a licensed clinical psychologist."),
        Doctor(12, 18, DOCTOR_IMAGES[3], "Dr. Triage", "Expert Triage Doctor", "You are an expert triage doctor. You role is to direct the patient to either Dr Smith, for general medicine, Dr Johnson, for emergency medicine, or Dr Williams, for clinical psychology. Be concise in your answers. If you are unsure, ask for more information. Always respond and roleplay your role as a triage doctor. Always recommmend the patient to talk to the right doctor.")
    ]

    dialogue_manager = DialogueManager(doctors)
    event_handler = EventHandler(player, dialogue_manager)

    clock = pygame.time.Clock()
    running = True

    # Load and play background music
    pygame.mixer.music.load('sound/chill_healing.mp3')  # Replace with your music file path
    pygame.mixer.music.play(-1)  # The -1 makes it loop indefinitely
 
    while running:
        running = event_handler.handle_events()

         # Check for doctor movements
        for doctor in doctors:
            if doctor.needs_to_move:
                move_doctor_to_player(player.pos, doctor.name, doctor.pending_description, doctors, dialogue_manager)
                doctor.needs_to_move = False
                doctor.pending_description = None

        event_handler.check_proximity(doctors)

        draw_game(screen, tile_image, player, doctors, 
                  dialogue_manager, 
                  event_handler.is_input_active(), 
                  event_handler.get_user_input(),
                  font)
        
        # If in a conversation, process AI responses
        if dialogue_manager.current_doctor and dialogue_manager.needs_ai_response:
            user_input = event_handler.get_user_input()
            if user_input != "":
                ai_response = call_ai_assistant(user_input, doctors, dialogue_manager.current_doctor.prompt)
                dialogue_manager.start_dialogue("NPC", ai_response)
                dialogue_manager.needs_ai_response = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()