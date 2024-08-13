import pygame
from config import TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT, TEXT_COLOR, BUBBLE_OUTLINE_COLOR, USER_BUBBLE_COLOR, NPC_BUBBLE_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT

def load_image(path, size):
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    return lines

def draw_dialogue_panel(surface, dialogue_history, font, input_active, user_input, current_doctor):
    panel_width = SCREEN_WIDTH // 3
    panel_height = SCREEN_HEIGHT
    panel_rect = pygame.Rect(SCREEN_WIDTH - panel_width, 0, panel_width, panel_height)

    # Draw panel background
    pygame.draw.rect(surface, (240, 240, 245), panel_rect)
    pygame.draw.line(surface, (200, 200, 210), (panel_rect.left, 0), (panel_rect.left, SCREEN_HEIGHT), 2)

    # Draw doctor name
    doctor_name = f"Conversation with {current_doctor.name}" if current_doctor else "No active conversation"
    name_surface = font.render(doctor_name, True, (60, 60, 70))
    surface.blit(name_surface, (panel_rect.left + 20, panel_rect.top + 20))

    # Draw dialogue history
    history_rect = pygame.Rect(panel_rect.left + 10, panel_rect.top + 60, panel_rect.width - 20, panel_rect.height - 120)
    pygame.draw.rect(surface, (250, 250, 255), history_rect)
    pygame.draw.rect(surface, (220, 220, 230), history_rect, 1)

    y_offset = history_rect.top + 10
    for speaker, message in dialogue_history:
        is_user = speaker == "User"
        speaker_name = "You" if is_user else current_doctor.name if current_doctor else "Doctor"
        
        # Wrap the text
        wrapped_lines = wrap_text(f"{speaker_name}: {message}", font, history_rect.width - 20)
        
        for line in wrapped_lines:
            if is_user:
                text_surface = font.render(line, True, (50, 50, 60))
                bubble_rect = text_surface.get_rect(topleft=(history_rect.left + 10, y_offset))
                bubble_rect.inflate_ip(20, 10)
                pygame.draw.rect(surface, (220, 230, 255), bubble_rect, border_radius=10)
                pygame.draw.rect(surface, (200, 210, 255), bubble_rect, 1, border_radius=10)
            else:
                text_surface = font.render(line, True, (50, 50, 60))
                bubble_rect = text_surface.get_rect(topright=(history_rect.right - 10, y_offset))
                bubble_rect.inflate_ip(20, 10)
                pygame.draw.rect(surface, (230, 255, 230), bubble_rect, border_radius=10)
                pygame.draw.rect(surface, (210, 255, 210), bubble_rect, 1, border_radius=10)
            
            surface.blit(text_surface, text_surface.get_rect(center=bubble_rect.center))
            y_offset += bubble_rect.height + 5
        
        y_offset += 10  # Extra space between messages

    # Draw input area
    input_rect = pygame.Rect(panel_rect.left + 10, panel_rect.bottom - 50, panel_rect.width - 20, 40)
    pygame.draw.rect(surface, (255, 255, 255), input_rect)
    pygame.draw.rect(surface, (200, 200, 210), input_rect, 1)
    if input_active:
        text_surface = font.render(user_input + "▋", True, (50, 50, 60))
        surface.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

def draw_game(screen, tile_image, player, doctors, dialogue_manager, input_active, user_input, font):
    # Clear the screen
    screen.fill((144, 201, 120))

    # Draw the game world
    for x in range(WORLD_WIDTH):
        for y in range(WORLD_HEIGHT):
            screen.blit(tile_image, (x * TILE_SIZE, y * TILE_SIZE))

    # Draw the player and doctors
    screen.blit(player.image, (player.pos[0] * TILE_SIZE, player.pos[1] * TILE_SIZE))
    for doctor in doctors:
        screen.blit(doctor.image, (doctor.pos[0] * TILE_SIZE, doctor.pos[1] * TILE_SIZE))

    # Draw the dialogue panel
    if dialogue_manager.current_doctor:
        dialogue_history = dialogue_manager.get_dialogue_history()
        draw_dialogue_panel(screen, dialogue_history, font, input_active, user_input, dialogue_manager.current_doctor)
    else:
        draw_dialogue_panel(screen, [], font, input_active, user_input, None)