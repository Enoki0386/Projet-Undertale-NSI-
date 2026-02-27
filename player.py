import pygame
from projectile import Projectile # import de la classe Projectile du fichier projectile.py


class Player(pygame.sprite.Sprite): # héritage de la classe sprite de pygame (expliqué dans projectile.py)

    def __init__(self):
        super().__init__() # récupération du __init__ de la classe sprite de pygame
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 1
        # les variables ci-dessus ne sont pas encore utilisées

        self.all_projectiles = pygame.sprite.Group() # sachant que les projectiles sont nombreux, ils sont stockés dans une superclasse
        self.sprite_sheet = pygame.image.load('assets/sprites/generic_char_v0.2/png/blue/char_blue_2.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect() # rectangle du joueur (hitbox)

        self.rect.x = 430 
        self.rect.y = 540
        # position de la hitbox du joueur ci-dessus
    
    def get_image(self, x, y):
        image = pygame.Surface([60, 60])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 60, 60))
        return image
    
    def launch_projectile(self):
        # Projectile est une sous-classe de Player, lui même sous-classe de Game

        self.all_projectiles.add(Projectile()) # ajout de l'objet Projectile au sein de la superclasse
    
    def move_right(self):
        self.rect.x += self.velocity # déplacement de la coordonnée x de la hitbox
    
    def move_left(self):
        self.rect.x -= self.velocity # déplacement de la coordonnée x de la hitbox
    
    def move_back(self):
        self.rect.y += self.velocity # déplacement de la coordonnée y de la hitbox
    
    def move_front(self):
        self.rect.y -= self.velocity # déplacement de la coordonnée y de la hitbox