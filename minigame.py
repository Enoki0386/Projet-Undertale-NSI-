import pygame
from random import randint

class Projectile(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = randint(100, 880)
        self.rect.y = 100
        self.speed = 3
    

    def move(self):

        self.rect.y += self.speed
    

    def draw_projectile(self, screen):
        
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))


class Minigame:

    def __init__(self):

        # définition des variables de l'écran de jeu
        self.width = 880 # 400
        self.height = 520 # 340
        self.x = 100 # 340
        self.y = 100 # 280

        # définition des variables pour notre curseur qui est un coeur
        self.image = pygame.image.load('objects/heart.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = (self.width // 2) - (self.rect.width // 2)
        self.rect.y = self.height + (100 - self.rect.height) - 10
        self.velocity = 5

        # gestion des projectiles
        self.projectiles = pygame.sprite.Group()
        self.spawn_time = 0

    
    def move_right(self):
        
        self.rect.x += self.velocity
    

    def move_left(self):
        
        self.rect.x -= self.velocity
    

    def move_back(self):
        
        self.rect.y -= self.velocity
    

    def move_front(self):
        
        self.rect.y += self.velocity
    

    def draw_mini_game(self, screen):

        # mini jeu
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2, border_radius=10)

        # curseur
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # projectiles
        for projectile in self.projectiles:
            projectile.draw_projectile(screen)
    

    def update_projectile(self):

        self.spawn_time += 1

        if self.spawn_time >= 60: 
            self.projectiles.add(Projectile())
            self.spawn_time = 0

        for projectile in self.projectiles:
            if projectile.rect.y < (620 - projectile.rect.height): # 15 = taille du projectile
                projectile.move()
            else:
                projectile.kill()