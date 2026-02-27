import pygame # import du module


class Projectile(pygame.sprite.Sprite): # création de la classe projectile qui hérite de la classe 'pygame.sprite.Sprite', qui
    # représente un sprite au sein de pygame

    def __init__(self):
        super().__init__() # récupération du __init__ de la classe sprite de pygame
        self.velocity = 5 # vitesse de 5 (pas encore utilisée dans le code)
        self.image = pygame.image.load('assets/sprites/pngimg.com - stone_PNG13546.png') # image de l'objet
        self.rect = self.image.get_rect() # création d'un rectangle représentant l'image pour une représentation dans le code de l'objet