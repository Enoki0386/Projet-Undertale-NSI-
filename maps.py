from player01 import Player01
from knight import Knight
import pygame

class Map:

    def __init__(self):

        self.width = 1600
        self.height = 1600

        self.player = Player01()
        self.knight = Knight()
    

    def load_maps(self, map, x, y):
        
        if map == 1:

            self.background = pygame.image.load('carte1/carte_undertale_background.png')
            self.path = pygame.image.load('carte1/carte_undertale_path.png')
            self.walls = pygame.image.load('carte1/carte_undertale_walls.png')
        
        elif map == 2:

            self.background = pygame.image.load('carte2/carte_undertale_2_background.png')
            self.path = pygame.image.load('carte2/carte_undertale_2_path.png')
            self.walls = pygame.image.load('carte2/carte_undertale_2_walls.png')    

        self.player.rect.x = x
        self.player.rect.y = y        


    def update_player(self):

        self.player.update_animation_player()
    

    def update_knight(self):

        self.knight.update_animation_knight()