import pygame
from dialogue_manager import DialogueManager

class EventHandler:
    def __init__(self, player, dialogue_manager):
        self.player = player
        self.dialogue_manager = dialogue_manager
        self.user_input = ""
        self.input_active = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.input_active or self.dialogue_manager.get_current_dialogue():
                        # Exit conversation mode
                        self.input_active = False
                        self.dialogue_manager.current_dialogue = None
                        self.user_input = ""
                        print("Exited conversation mode")  # Debug print
                    else:
                        return False
                elif self.input_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    elif event.key == pygame.K_RETURN and self.user_input:
                        self.dialogue_manager.start_dialogue("User", self.user_input)
                        self.dialogue_manager.get_ai_response(self.user_input)
                        self.user_input = ""
                    elif event.unicode.isprintable():
                        self.user_input += event.unicode
                else:
                    self.handle_movement(event.key)
        return True

    def handle_movement(self, key):
        if key in (pygame.K_LEFT, pygame.K_a):
            self.player.move(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.player.move(1, 0)
        elif key in (pygame.K_UP, pygame.K_w):
            self.player.move(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.player.move(0, 1)

    def check_proximity(self, doctors):
        for doctor in doctors:
            if abs(self.player.pos[0] - doctor.pos[0]) <= 1 and abs(self.player.pos[1] - doctor.pos[1]) <= 1:
                if not self.input_active and not self.dialogue_manager.get_current_dialogue():
                    self.input_active = True
                    print("Entered conversation mode")  # Debug print
                return
        self.input_active = False

    def get_user_input(self):
        return self.user_input

    def is_input_active(self):
        return self.input_active