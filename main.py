import random
import math
from spritesheet import Spritesheet

from pygame.locals import *
import sys
import os
import pygame
import time

WIDTH = 720 # 15 wide
HEIGHT = 480 # 11 tall

pygame.init()

font = pygame.font.Font('freesansbold.ttf', 14)

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

TYPES = ['Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dark', 'Dragon', 'Steel', 'Fairy', None]
CHART = {0: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0, 1, 1, 0.5, 1, 1], 
         1: [1, 0.5, 0.5, 2, 1, 2, 1, 1, 1, 1, 1, 2, 0.5, 1, 0.5, 1, 2, 1, 1],
         2: [1, 2, 0.5, 0.5, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 0.5, 1, 1, 1, 1],
         3: [1, 0.5, 2, 0.5, 1, 1, 1, 0.5, 2, 0.5, 1, 0.5, 2, 1, 0.5, 1, 0.5, 1, 1],
         4: [1, 1, 2, 0.5, 0.5, 1, 1, 1, 0, 2, 1, 1, 1, 1, 0.5, 1, 1, 1, 1],
         5: [1, 0.5, 0.5, 2, 1, 0.5, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 0.5, 1, 1],
         6: [2, 1, 1, 1, 1, 2, 1, 0.5, 1, 0.5, 0.5, 0.5, 2, 0, 1, 2, 2, 0.5, 1],
         7: [1, 1, 1, 2, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 0, 2, 1],
         8: [1, 2, 1, 0.5, 2, 1, 1, 2, 1, 0, 1, 0.5, 2, 1, 1, 1, 2, 1, 1],
         9: [1, 1, 1, 2, 0.5, 1, 2, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 0.5, 1, 1],
         10: [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 0, 0.5, 1, 1],
         11: [1, 0.5, 1, 2, 1, 1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 0.5, 1, 2, 0.5, 0.5, 1],
         12: [1, 2, 1, 1, 1, 2, 0.5, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 0.5, 1, 1],
         13: [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 1, 1, 1],
         14: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0.5, 0, 1],
         15: [1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 1, 0.5, 1],
         16: [1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0.5, 2, 1],
         17: [1, 0.5, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 1, 1, 1, 2, 2, 0.5, 1, 1]
}

class Pokemon():
    def __init__(self, name, move_nums, pokemon_no, level):
        self.level = level
        self.moves_files = move_nums
        self.get_moves()
        self.no = pokemon_no
        self.name = name
        f = open(f"data/mons/{pokemon_no}.txt")
        self.species = f.readline()
        self.types = [f.readline().strip('\n'), f.readline().strip('\n')]
        self.ivs = [31, 31, 31, 31, 31, 31]
        self.base = [int(f.readline()), int(f.readline()), int(f.readline()), int(f.readline()), int(f.readline()), int(f.readline())]
        f.close()
        self.calc_stats()
        self.hp = self.stats[0]
    def calc_stats(self):
        self.stats = []
        self.stats.append(math.floor((self.base[0] * 2 + self.ivs[0]) * self.level / 100) + self.level + 10)
        for i in range(1, 6):
            self.stats.append(math.floor((self.base[i] * 2 + self.ivs[i]) * self.level / 100) + 5)
        print(self.stats)
    def get_moves(self):
        self.moves = [[] for i in range(4)]
        for i, num in enumerate(self.moves_files):
            f = open(f"data/moves/{num}.txt")
            for j in f.readlines():
                self.moves[i].append(j.strip('\n'))
            f.close()
        print(self.moves)
    def calc_damage(self, target, move):
        if self.moves[move][2] == "Physical":
            a = self.stats[2]
            d = target.stats[3]
        if self.moves[move][2] == "Special":
            a = self.stats[4]
            d = target.stats[5]
        stab = 1
        if self.moves[move][1] in self.types:
            stab = 1.5
        effectiveness = target.type_effectiveness(self.moves[move][1])
        print(f"{self.name} used {self.moves[move][0]}")
        if effectiveness < 1:
            print("It's not very effective")
        elif effectiveness > 1:
            print("It's super effective")
        damage = round(((2 * self.level / 5 + 2) * int(self.moves[move][4]) * a / d / 50 + 2) * stab * effectiveness * (random.random() * 0.15 + 0.85))
        return damage
    def type_effectiveness(self, move_type):
        move_type = TYPES.index(move_type)
        effectiveness = CHART[move_type][TYPES.index(self.types[0])] * CHART[move_type][TYPES.index(self.types[1])]
        return effectiveness
        
        

def battle(mon1, mon2):
    while mon1.hp > 0 and mon2.hp > 0:
        move1 = int(input()) - 1
        move2 = int(input()) - 1
        if mon1.stats[5] > mon2.stats[5] or (mon1.stats[5] == mon2.stats[5] and random.randint(1, 2) == 1):
            mon2.hp -= mon1.calc_damage(mon2, move1)
            if mon2.hp <= 0:
                winner = "mon1"
            else:
                mon1.hp -= mon2.calc_damage(mon1, move2)
                if mon1.hp <= 0:
                    winner = "mon2"
        else:
            mon1.hp -= mon2.calc_damage(mon1, move2)
            if mon1.hp <= 0:
                winner = "mon2"
            else:
                mon2.hp -= mon1.calc_damage(mon2, move1)
                if mon2.hp <= 0:
                    winner = "mon1"
        print(f"Mon 1: {mon1.hp}")
        print(f"Mon 2: {mon2.hp}")
    print(winner)

# bulb1 = Pokemon('Bulby1', [1, 2], 1, 100)
# bulb2 = Pokemon('bulby2', [1, 2], 1, 100)
# battle(bulb1, bulb2)

bg_spritesheet = Spritesheet('data/sprites/main/Temp_tileset.png')

names = ["sea1", "sea2", "sea3", "sea4", "sea5", "sea6", "sea7", "sea8", "water_rock", "sign1", "sign2", "grass5", "bush1", "cut_tree", "strength_rock", "br_bush", "bush2", "flower", "water_rock2", "grass1", "grass2", "grass3", "grass4", "player", 'hor_fence1', 'hor_fence2', 'ver_fence1, ver_fence2', 'cor_fence1', 'tl_bush', 'hor_bush', 'tr_bush', 'bush4', 'ver_bush', 'bl_bush', 'playeru', 'playerl', 'playerr']

main_map = []

for i in range(40):
    main_map.append(["sea2" for j in range(1000)])
for i in range(920):
    main_map.append(["sea2" for j in range(40)] + ["grass" + str(random.randint(1, 5)) for j in range(920)] + ["sea2" for j in range(40)])
for i in range(40):
    main_map.append(["sea2" for j in range(1000)])

print(len(main_map))

sprites_dict = {}
for i in names:
    sprites_dict[i] = bg_spritesheet.parse_sprites(i)

def get_coords(x, y):
    return x * 48, y * 48

TIME_DIF = 0.1

class Background:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = -1
        self.dir = ""
    def sim(self, pressed_keys):
        if pressed_keys[K_RIGHT] and (main_map[self.y][self.x + 1][:3] != "sea"):
            if time.time() - self.timer >= TIME_DIF:
                self.x += 1
                self.timer = time.time()
                self.dir = "r"
        elif pressed_keys[K_LEFT] and (main_map[self.y][self.x - 1][:3] != "sea"):
            if time.time() - self.timer >= TIME_DIF:
                self.x -= 1
                self.timer = time.time()
                self.dir = "l"
        elif pressed_keys[K_DOWN] and (main_map[self.y + 1][self.x][:3] != "sea"):
            if time.time() - self.timer >= TIME_DIF:
                self.y += 1
                self.timer = time.time()
                self.dir = ""
        elif pressed_keys[K_UP] and (main_map[self.y - 1][self.x][:3] != "sea"):
            if time.time() - self.timer >= TIME_DIF:
                self.y -= 1
                self.timer = time.time()
                self.dir = "u"
        for i in range(self.y - 5, self.y + 6):
            for j in range(self.x - 7, self.x + 8):
                screen.blit(sprites_dict[main_map[i][j]], get_coords(j + 7 - self.x, i + 5 - self.y))
        screen.blit(sprites_dict["player" + self.dir], [get_coords(7, 5)[0], get_coords(7, 5)[1] - 9])

bg = Background(50, 50)

running = True
fps = 60

class Player():
    def __init__(self):
        self.team = []
    def catchPokemon(self, mon):
        self.team.append(mon)


while running == True:
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    pygame.display.set_caption("Pokemon")
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
    # screen.blit(sprites_dict['flower'], (0, 0))
    bg.sim(pygame.key.get_pressed())
    pygame.display.flip()
    fpsClock.tick(fps)
    continue