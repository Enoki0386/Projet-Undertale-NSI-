import pygame
import animation
from animation import animations

class NPC(pygame.sprite.Sprite): # 'animation.AnimateSprite' est sensé être dans les parenthèses pour l'animation. Ainsi pour engendrer les boites de dialogues
    def __init__(self, x, y):    # j'ai choisi de garder temporairement la classe Sprite. Lorsque l'animation sera requise oubliez pas de mettre l'animation dans le super
        super().__init__()

        # l'image est sensée être animée, cependant en guise de solution temporaire, elle sera une surface seulement
        self.image = pygame.Surface((50, 60))
        self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y 

        # couleur des dialogues
        self.WHITE = (255, 255, 255) # -> texte
        self.BROWN = (210, 105, 30) # -> fond

    
    def load_dialogue(filename, lines):
        '''Méthode destinée à extraire le dialogue d'un fichier texte'''
        with open(f'{filename}.txt', 'r') as f:
            lignes = f.readlines(lines)
    
        return lignes
    
    def load_text_boxes(filename, lines):
        '''Méthode destinée à créer des boites de dialogues'''
        lignes = self.load_dialogue(filename, lines)
        