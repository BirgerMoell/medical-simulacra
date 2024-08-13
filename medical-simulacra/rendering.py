import pygame
from config import TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT, TEXT_COLOR, BUBBLE_OUTLINE_COLOR, USER_BUBBLE_COLOR, NPC_BUBBLE_COLOR

def load_image(path, size):
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)

def draw_speech_bubble(surface, text, pos, color, font, padding=10, border=2):
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
    
    bubble = pygame.Surface((bubble_width, bubble_height + 10), pygame.SRCALPHA)
    
    # Draw outline
    pygame.draw.rect(bubble, BUBBLE_OUTLINE_COLOR, (0, 0, bubble_width, bubble_height), border_radius=10)
    pygame.draw.rect(bubble, color, (border, border, bubble_width - 2*border, bubble_height - 2*border), border_radius=10)
    
    # Draw the speech bubble tail
    pygame.draw.polygon(bubble, BUBBLE_OUTLINE_COLOR, [
        (bubble_width // 2 - 10, bubble_height),
        (bubble_width // 2 + 10, bubble_height),
        (bubble_width // 2, bubble_height + 10)
    ])
    pygame.draw.polygon(bubble, color, [
        (bubble_width // 2 - 10 + border, bubble_height - border),
        (bubble_width // 2 + 10 - border, bubble_height - border),
        (bubble_width // 2, bubble_height + 10 - border)
    ])
    
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, TEXT_COLOR)
        bubble.blit(text_surface, (padding, padding + i * font.get_height()))
    
    bubble_pos = (pos[0] * TILE_SIZE - bubble_width // 2 + TILE_SIZE // 2,
                  pos[1] * TILE_SIZE - bubble_height - 15)
    
    surface.blit(bubble, bubble_pos)

def draw_game(screen, tile_image, player, doctors, current_dialogue, input_active, user_input, font):
    screen.fill((144, 201, 120))
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            screen.blit(tile_image, (x * TILE_SIZE, y * TILE_SIZE))
    
    screen.blit(player.image, (player.pos[0] * TILE_SIZE, player.pos[1] * TILE_SIZE))
    
    for doctor in doctors:
        screen.blit(doctor.image, (doctor.pos[0] * TILE_SIZE, doctor.pos[1] * TILE_SIZE))

    if current_dialogue:
        speaker, message = current_dialogue
        print(f"Drawing dialogue: {speaker} - {message}")  # Debug print
        if speaker == "User":
            draw_speech_bubble(screen, message, player.pos, USER_BUBBLE_COLOR, font)
        else:
            nearest_doctor = min(doctors, key=lambda d: ((d.pos[0] - player.pos[0])**2 + (d.pos[1] - player.pos[1])**2))
            draw_speech_bubble(screen, message, nearest_doctor.pos, NPC_BUBBLE_COLOR, font)

    if input_active:
        draw_speech_bubble(screen, user_input + "▋", player.pos, USER_BUBBLE_COLOR, font)