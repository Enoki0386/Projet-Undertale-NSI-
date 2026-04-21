import pygame

class Item(pygame.sprite.Sprite):
    
    def __init__(self, name, x, y):
        
        super().__init__()
        self.name = name
        self.image = pygame.image.load(f'objects/{name}.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        