from player01 import Player01
from knight import Knight
import pygame
import csv


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
        self.all_monsters = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        
    

    def load_maps(self, map, x, y):
        
        self.all_monsters.empty()
        
        if map == 1:

            self.background = pygame.image.load('carte1/carte_undertale_background.png')
            self.path = pygame.image.load('carte1/carte_undertale_path.png')
            self.walls = pygame.image.load('carte1/carte_undertale_walls.png')
            self.load_wall_group('carte1/carte_undertale._walls.csv')
            self.spawn_monster(1070, 580)
            self.spawn_monster(27, 15)
            self.spawn_monster(565, 219)
            self.spawn_monster(23, 190)
        
        elif map == 2:

            self.background = pygame.image.load('carte2/carte_undertale_2_background.png')
            self.path = pygame.image.load('carte2/carte_undertale_2_path.png')
            self.walls = pygame.image.load('carte2/carte_undertale_2_walls.png')   
            self.load_wall_group('carte2/carte_undertale_2_walls.csv')
            self.spawn_monster(600, 600) 
            self.spawn_monster(789, 20)
            self.spawn_monster(124, 123)
            self.spawn_monster(987, 102)
            self.spawn_monster(223, 500)

        self.player.rect.x = x
        self.player.rect.y = y      

    
    def load_wall_group(self, filename):

        self.wall_group.empty()

        with open(filename) as f:
            reader = csv.reader(f)

            for row_index, row in enumerate(reader):
                for col_index, tile in enumerate(row):

                    if int(tile.strip()) != -1:
                        x = col_index * self.tile_size
                        y = row_index * self.tile_size
                        self.wall_group.add(Wall(x, y, self.tile_size))

    
    def spawn_monster(self, x, y):

        knight = Knight(x, y)
        self.all_monsters.add(knight)


    def update_player(self):

        self.player.update_animation_player()
    

    def update_monsters(self):

        for monster in self.all_monsters:
            monster.update_animation_knight()
    