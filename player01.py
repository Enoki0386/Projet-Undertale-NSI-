import pygame
import animation
from animation import animations

class Player01(animation.AnimateSprite):

    def __init__(self):

        super().__init__('run_right') # récupération du __init__ de la classe sprite de pygame
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 5

        self.rect = pygame.Rect(430 + (96 - 56) // 2, 540 + (80 - 60) // 2, 56, 60) # rectangle du joueur (hitbox)
        self.rect.x = 430 # position de la hitbox du joueur
        self.rect.y = 540

        self.pressed = {}
    

    def update_animation_player(self):

        self.animate()


    def move_right(self):

        self.images = animations.get('run_right')
        self.rect.x += self.velocity # déplacement de la coordonnée x de la hitbox
    

    def move_left(self):

        self.images = animations.get('run_left')
        self.rect.x -= self.velocity # déplacement de la coordonnée x de la hitbox
    

    def move_back(self):

        self.images = animations.get('run_down')
        self.rect.y += self.velocity # déplacement de la coordonnée y de la hitbox
    

    def move_front(self):

        self.images = animations.get('run_up')
        self.rect.y -= self.velocity # déplacement de la coordonnée y de la hitbox
    