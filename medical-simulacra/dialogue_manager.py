import time
from ai_integration import call_ai_assistant

class DialogueManager:
    def __init__(self):
        self.current_dialogue = None
        self.dialogue_history = {}  # Dictionary to store dialogue history for each doctor
        self.current_doctor = None

    def start_dialogue(self, speaker, message):
        self.current_dialogue = (speaker, message)
        if self.current_doctor:
            if self.current_doctor not in self.dialogue_history:
                self.dialogue_history[self.current_doctor] = []
            self.dialogue_history[self.current_doctor].append((speaker, message))

    def set_current_doctor(self, doctor):
        self.current_doctor = doctor

    def clear_current_doctor(self):
        self.current_doctor = None
        self.current_dialogue = None

    def get_ai_response(self, user_input):
        ai_response = call_ai_assistant(user_input)
        print(f"AI Response: {ai_response}")  # Debug print
        self.start_dialogue("NPC", f"Dr. AI: {ai_response}")

    def get_current_dialogue(self):
        return self.current_dialogue

    def get_dialogue_history(self):
        if self.current_doctor in self.dialogue_history:
            return self.dialogue_history[self.current_doctor]
        return []
    
    def start_conversation_with(self, doctor):
        self.set_current_doctor(doctor)
        greeting = f"Hello, I'm {doctor.name}, specializing in {doctor.specialty}. How can I assist you today?"
        self.start_dialogue("NPC", greeting)