import pygame
import json

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        f = open("data/sprites/main/tilesheet.json")
        self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((255,200,106))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))

        sprite = pygame.transform.scale(sprite, (sprite.get_size()[0] * 3, sprite.get_size()[1] * 3))
        return sprite
    
    def parse_sprites(self, name):
        sprite = self.data[name]['frame']
        x, y, w, h = sprite['x'], sprite['y'], sprite['w'], sprite['h']
        image = self.get_sprite(x, y, w, h)
        return image