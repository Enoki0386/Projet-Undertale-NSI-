import pygame
import animation
from animation import animations


class Knight(animation.AnimateSprite):

    def __init__(self, x, y):

        super().__init__('WALK_right') # récupération du __init__ de la classe sprite de pygame
        self.health = 25
        self.max_health = 25
        self.attack = 10
        self.velocity = 2.5

        self.direction = 1

        self.rect = pygame.Rect(x + (96 - 56) // 2, y + (80 - 60) // 2, 56, 60) # rectangle du joueur (hitbox)
        self.rect.x = x # position de la hitbox du joueur
        self.rect.y = y

        self.patrol_right = self.rect.x + 100
        self.patrol_left = self.rect.x - 100 # attention limite

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
    

    def health_bar(self, surface, camera_x, camera_y):

        bar_color_health = (111, 210, 46)
        bar_color = (255, 0, 0)

        bar_x = self.rect.x - camera_x + self.max_health + 10
        bar_y = self.rect.y - camera_y

        bar_position_health = [bar_x, bar_y, self.health, 5]
        bar_position = [bar_x, bar_y, self.max_health, 5]

        pygame.draw.rect(surface, bar_color, bar_position)
        pygame.draw.rect(surface, bar_color_health, bar_position_health)
    

    def damage(self, amount):

        self.health -= amount

        if self.health <= 0:
            self.health = 0


    def chase_player(self, player):

        if player.rect.x > self.rect.x:
            self.rect.x += self.velocity
            self.images = animations.get('WALK_right')

        elif player.rect.x < self.rect.x:
            self.rect.x -= self.velocity
            self.images = animations.get('WALK_left')
        
        if player.rect.y > self.rect.y:
            self.rect.y += self.velocity
            
        elif player.rect.y < self.rect.y:
            self.rect.y -= self.velocity