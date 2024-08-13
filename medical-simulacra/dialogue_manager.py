import time
from ai_integration import call_ai_assistant

class DialogueManager:
    def __init__(self):
        self.current_dialogue = None
        self.dialogue_start_time = 0
        self.dialogue_duration = 10000  # 10 seconds, increased for readability

    def start_dialogue(self, speaker, message):
        self.current_dialogue = (speaker, message)
        self.dialogue_start_time = time.time() * 1000  # Convert to milliseconds

    def update_dialogue(self):
        if self.current_dialogue and time.time() * 1000 - self.dialogue_start_time > self.dialogue_duration:
            self.current_dialogue = None

    def get_ai_response(self, user_input):
        ai_response = call_ai_assistant(user_input)
        print(f"AI Response: {ai_response}")  # Debug print
        self.start_dialogue("NPC", f"Dr. AI: {ai_response}")

    def get_current_dialogue(self):
        return self.current_dialogue