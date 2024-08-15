import pygame
from config import TILE_SIZE, WORLD_WIDTH, WORLD_HEIGHT

def load_image(path, size):
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)

class Player:
    def __init__(self, x, y, image_path):
        self.pos = [x, y]
        self.image = load_image(image_path, (TILE_SIZE, TILE_SIZE))

    def move(self, dx, dy):
        new_x = max(0, min(WORLD_WIDTH - 1, self.pos[0] + dx))
        new_y = max(0, min(WORLD_HEIGHT - 1, self.pos[1] + dy))
        self.pos = [new_x, new_y]

class Doctor:
    def __init__(self, x, y, image_path, name, speciality, prompt):
        self.pos = [x, y]
        self.image = load_image(image_path, (TILE_SIZE, TILE_SIZE))
        self.name = name
        self.speciality = speciality
        self.prompt = prompt
        self.needs_to_move = False
        self.pending_description = None

    def set_pending_move(self, description):
        self.needs_to_move = True
        self.pending_description = description