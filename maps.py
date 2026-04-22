from player01 import Player01
from knight import Knight
from item import Item
from minigame import Minigame
from boss import Boss
import pygame
import csv
from random import randint


class Wall(pygame.sprite.Sprite):
    
    def __init__(self, x, y, size):

        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((0, 0, 0))
        self.rect = pygame.Rect(x, y, size, size)
        self.mask = pygame.mask.from_surface(self.image)


class Map:

    def __init__(self):

        self.width = 1600
        self.height = 1600
        self.tile_size = 16

        self.player = Player01()
        self.boss = Boss(576, 892)
        self.minigame = Minigame()
        self.all_monsters = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.items_group = pygame.sprite.Group()
        self.items_choice = ['shield', 'heart', 'knife']
        

    def load_maps(self, map, x, y):
        
        self.all_monsters.empty()
        self.items_group.empty()
        
        if map == 1:

            self.background = pygame.image.load('carte1/carte_undertale_background.png')
            self.path = pygame.image.load('carte1/carte_undertale_path.png')
            self.walls = pygame.image.load('carte1/carte_undertale_walls.png')
            self.load_wall_group('carte1/carte_undertale._walls.csv')
        
        elif map == 2:

            self.background = pygame.image.load('carte2/carte_undertale_2_background.png')
            self.path = pygame.image.load('carte2/carte_undertale_2_path.png')
            self.walls = pygame.image.load('carte2/carte_undertale_2_walls.png')   
            self.load_wall_group('carte2/carte_undertale_2_walls.csv')
        
        self.monsters_spawner(map)
        self.items_spawner(map)

        self.player.rect.x = x
        self.player.rect.y = y      

    
    def load_wall_group(self, filename):

        self.wall_group.empty()

        with open(filename) as f:
            reader = csv.reader(f)
            row_index = 0

            for row in reader:
                col_index = 0

                for tile in row:
                    if int(tile.strip()) != -1:
                        x = col_index * self.tile_size
                        y = row_index * self.tile_size
                        self.wall_group.add(Wall(x, y, self.tile_size))
                    
                    col_index += 1
                
                row_index += 1

    
    def spawn_monster(self, x, y):

        knight = Knight(x, y)
        self.all_monsters.add(knight)


    def monsters_spawner(self, map):

        repeteur = 0

        while repeteur < 5:
            x = randint(0, 1600)
            y = randint(0, 1600)
            
            if map == 1:
                if 800 < x < 1400 and 200 < y < 1200:
                    self.spawn_monster(x, y)
                    repeteur += 1
                    continue
            
            elif map == 2:
                if 600 < x < 1500 and 200 < y < 1400:
                    self.spawn_monster(x, y)
                    repeteur += 1
                    continue
    

    def items_spawner(self, map):

        repeteur = 0

        while repeteur < 5:
            x = randint(0, 1600)
            y = randint(0, 1600)
            name = self.items_choice[randint(0, len(self.items_choice) - 1)]
            
            if map == 1:
                if 800 < x < 1400 and 200 < y < 1200:
                    self.spawn_item(name, x, y)
                    repeteur += 1
                    continue
            
            elif map == 2:
                if 600 < x < 1500 and 200 < y < 1400:
                    self.spawn_item(name, x, y)
                    repeteur += 1
                    continue

    
    def spawn_item(self, name, x, y):

        item = Item(name, x, y)
        self.items_group.add(item)
    

    def update_player(self):

        self.player.update_animation_player()
    

    def update_monsters(self):

        for monster in self.all_monsters:
            monster.update_animation_knight()