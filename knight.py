import pygame
import animation
from animation import animations


class Knight(animation.AnimateSprite):

    def __init__(self):

        super().__init__('WALK_right') # récupération du __init__ de la classe sprite de pygame
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 2.5

        self.direction = 1
        self.patrol_left = 1000
        self.patrol_right = 1200

        self.rect = pygame.Rect(1070 + (96 - 56) // 2, 580 + (80 - 60) // 2, 56, 60) # rectangle du joueur (hitbox)
        self.rect.x = 1070 # position de la hitbox du joueur
        self.rect.y = 580

        self.pressed = {}
    

    def update_animation_knight(self):

        self.animate()
    

    def default_state(self):

        self.rect.x += self.velocity * self.direction

        if self.rect.x > self.patrol_right:
            self.images = animations.get('WALK_left')
            self.direction = -1
        
        elif self.rect.x < self.patrol_left:
            self.images = animations.get('WALK_right')
            self.direction = 1