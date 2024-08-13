import pygame
from dialogue_manager import DialogueManager

class EventHandler:
    def __init__(self, player, dialogue_manager):
        self.player = player
        self.dialogue_manager = dialogue_manager
        self.user_input = ""
        self.input_active = False
        self.conversation_doctor = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.input_active or self.dialogue_manager.get_current_dialogue():
                        self.end_conversation()
                    else:
                        return False
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    self.handle_movement(event.key)
                elif self.input_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    elif event.key == pygame.K_RETURN and self.user_input:
                        self.dialogue_manager.start_dialogue("User", self.user_input)
                        self.dialogue_manager.get_ai_response(self.user_input)
                        self.user_input = ""
                    elif event.unicode.isprintable():
                        self.user_input += event.unicode
        return True

    def handle_movement(self, key):
        old_pos = self.player.pos.copy()
        if key == pygame.K_LEFT:
            self.player.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.player.move(1, 0)
        elif key == pygame.K_UP:
            self.player.move(0, -1)
        elif key == pygame.K_DOWN:
            self.player.move(0, 1)
        
        if self.conversation_doctor:
            distance = ((self.player.pos[0] - self.conversation_doctor.pos[0])**2 + 
                        (self.player.pos[1] - self.conversation_doctor.pos[1])**2)**0.5
            if distance > 2:  # End conversation if player is more than 2 tiles away
                self.end_conversation()

    def check_proximity(self, doctors):
        for doctor in doctors:
            distance = ((self.player.pos[0] - doctor.pos[0])**2 + 
                        (self.player.pos[1] - doctor.pos[1])**2)**0.5
            if distance <= 1:
                if not self.input_active and not self.dialogue_manager.get_current_dialogue():
                    self.start_conversation(doctor)
                return
        if self.input_active:
            self.end_conversation()

    def start_conversation(self, doctor):
        self.input_active = True
        self.conversation_doctor = doctor
        self.dialogue_manager.start_conversation_with(doctor)
        print(f"Started conversation with {doctor.name}")  # Debug print

    def end_conversation(self):
        self.input_active = False
        self.dialogue_manager.clear_current_doctor()
        self.user_input = ""
        self.conversation_doctor = None
        print("Ended conversation")  # Debug print

    def get_user_input(self):
        return self.user_input

    def is_input_active(self):
        return self.input_active

    def get_conversation_doctor(self):
        return self.conversation_doctor