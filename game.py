import pygame
import sys
import time
import random
import os
from openai import OpenAI
from dotenv import load_dotenv
from typing_extensions import override
from openai import AssistantEventHandler

# Initialize pygame
pygame.init()

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

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Small World Game with Specialized Doctors")

# Load and scale images
def load_image(path, size):
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)

player_image = load_image('sprites/person.webp', (TILE_SIZE, TILE_SIZE))
tile_image = load_image('sprites/grass2.webp', (TILE_SIZE, TILE_SIZE))

# Player and NPC setup
player_pos = [5, 7]
doctors = [
    {"pos": [8, 7], "image": load_image('sprites/doctor_2.webp', (TILE_SIZE, TILE_SIZE)), "name": "Dr. Smith", "specialty": "General Medicine"},
    {"pos": [4, 3], "image": load_image('sprites/doctor_3.webp', (TILE_SIZE, TILE_SIZE)), "name": "Dr. Johnson", "specialty": "Emergency Medicine"},
    {"pos": [WORLD_WIDTH - 4, 3], "image": load_image('sprites/nurse.webp', (TILE_SIZE, TILE_SIZE)), "name": "Dr. Williams", "specialty": "General Practice"}
]

# Font setup
font = pygame.font.Font(None, 18)

# Dialogue setup
current_dialogue = None
user_input = ""
input_active = False
dialogue_start_time = 0
DIALOGUE_DURATION = 3000  # Duration to show dialogue in milliseconds

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)
thread = client.beta.threads.create()

class GameEventHandler(AssistantEventHandler):    
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)
      
    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)
      
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)
  
    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)

def call_ai_assistant(question):
    global current_dialogue
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question
    )
    
    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id="asst_SZP3IHrndmnRLtgSTIbbdGmO",
        instructions="Please address the user as Jane Doe. The user has a premium account.",
        event_handler=GameEventHandler(),
    ) as stream:
        stream.until_done()
    
    # Assume the AI assistant's response is stored in `assistant_response`
    # In the real implementation, you need to capture this response from the stream
    assistant_response = "Dr. AI: I have analyzed your input. Here is my suggestion..."
    current_dialogue = ("NPC", assistant_response)

def npc_response(input_text, doctor):
    call_ai_assistant(input_text)

def draw_speech_bubble(surface, text, pos, color, padding=10, border=2):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        if font.size(' '.join(current_line))[0] > TILE_SIZE * 4:
            lines.append(' '.join(current_line[:-1]))
            current_line = [word]
    lines.append(' '.join(current_line))
    
    max_width = max(font.size(line)[0] for line in lines)
    height = sum(font.size(line)[1] for line in lines)
    
    bubble_width = max_width + padding * 2
    bubble_height = height + padding * 2
    
    # Create bubble shape
    bubble = pygame.Surface((bubble_width, bubble_height + 10), pygame.SRCALPHA)
    pygame.draw.rect(bubble, color, (0, 0, bubble_width, bubble_height), border_radius=10)
    pygame.draw.polygon(bubble, color, [(bubble_width // 2 - 10, bubble_height),
                                        (bubble_width // 2 + 10, bubble_height),
                                        (bubble_width // 2, bubble_height + 10)])
    
    # Draw text
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, TEXT_COLOR)
        bubble.blit(text_surface, (padding, padding + i * font.get_height()))
    
    # Position the bubble above the character
    bubble_pos = (pos[0] * TILE_SIZE - bubble_width // 2 + TILE_SIZE // 2,
                  pos[1] * TILE_SIZE - bubble_height - 15)
    
    surface.blit(bubble, bubble_pos)

def handle_movement(key):
    if key in (pygame.K_LEFT, pygame.K_a):
        player_pos[0] = max(0, player_pos[0] - 1)
    elif key in (pygame.K_RIGHT, pygame.K_d):
        player_pos[0] = min(WORLD_WIDTH - 1, player_pos[0] + 1)
    elif key in (pygame.K_UP, pygame.K_w):
        player_pos[1] = max(0, player_pos[1] - 1)
    elif key in (pygame.K_DOWN, pygame.K_s):
        player_pos[1] = min(WORLD_HEIGHT - 1, player_pos[1] + 1)

def handle_events():
    global running, input_active, user_input, current_dialogue, dialogue_start_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if input_active or current_dialogue:
                    input_active = False
                    current_dialogue = None
                    user_input = ""
                else:
                    running = False
            elif not input_active:
                handle_movement(event.key)
            elif event.key == pygame.K_BACKSPACE and input_active:
                user_input = user_input[:-1]
            elif input_active and event.unicode.isprintable():
                user_input += event.unicode
            elif input_active and event.key == pygame.K_RETURN and user_input:
                current_dialogue = ("User", user_input)
                dialogue_start_time = pygame.time.get_ticks()
                npc_response(user_input, random.choice(doctors))
                user_input = ""
                input_active = False

def check_proximity():
    global input_active, current_dialogue, dialogue_start_time
    for doctor in doctors:
        if abs(player_pos[0] - doctor["pos"][0]) <= 1 and abs(player_pos[1] - doctor["pos"][1]) <= 1:
            if current_dialogue and current_dialogue[0] == "User":
                npc_reply = npc_response(current_dialogue[1], doctor)
                current_dialogue = ("NPC", npc_reply)
                dialogue_start_time = pygame.time.get_ticks()
            elif not input_active and not current_dialogue:
                input_active = True
            return
    input_active = False

def draw_game():
    global current_dialogue
    screen.fill(BACKGROUND_COLOR)
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            screen.blit(tile_image, (x * TILE_SIZE, y * TILE_SIZE))
    screen.blit(player_image, (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE))
    for doctor in doctors:
        screen.blit(doctor["image"], (doctor["pos"][0] * TILE_SIZE, doctor["pos"][1] * TILE_SIZE))

    if current_dialogue:
        speaker, message = current_dialogue
        if speaker == "User":
            draw_speech_bubble(screen, message, player_pos, USER_BUBBLE_COLOR)
        else:
            for doctor in doctors:
                if doctor["name"] in message:
                    draw_speech_bubble(screen, message, doctor["pos"], NPC_BUBBLE_COLOR)
                    break
        
        # Clear dialogue after duration
        if pygame.time.get_ticks() - dialogue_start_time > DIALOGUE_DURATION:
            current_dialogue = None

    if input_active:
        draw_speech_bubble(screen, user_input + "▋", player_pos, USER_BUBBLE_COLOR)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    handle_events()
    check_proximity()
    draw_game()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
