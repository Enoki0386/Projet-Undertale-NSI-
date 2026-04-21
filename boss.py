import pygame
import animation
from animation import animations

class Boss(animation.AnimateSprite):
    '''Cette classe est en construction, elle devrait créer le boss du jeu. Cependant ici, elle sert uniquement à déclencher une
    mécanique du jeu, qui est le mini-jeu. Ainsi il n'y a pas d'animations, de collisions encore.'''
    def __init__(self, x, y):
        '''Quelques caractéristiques de l'objet'''
        super().__init__('dragon_basic_state')
        self.rect = pygame.Rect(x + (96 - 56) // 2, y + (80 - 60) // 2, 56, 60)
        self.rect.x = x 
        self.rect.y = y
        self.health = 1000
        self.max_health = 1000