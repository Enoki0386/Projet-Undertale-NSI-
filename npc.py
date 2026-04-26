import pygame
import animation
from animation import animations

class NPC(pygame.sprite.Sprite): # 'animation.AnimateSprite' est sensé être dans les parenthèses pour l'animation. Ainsi pour engendrer les boites de dialogues
    def __init__(self, x, y, filename):    # j'ai choisi de garder temporairement la classe Sprite. Lorsque l'animation sera requise oubliez pas de mettre l'animation dans le super
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

        # dialogue + fonctionnement
        self.dialogues = self.load_dialogue(filename)
        self.dialogue_index = 0
        self.finished = False

        # Attention : le fichier texte contenant le dialogue doit avoir des lignes de la même longueur
        # que la 1ère ligne que j'ai mise pour que tout s'affiche sans déborder
    
    
    def load_dialogue(self, filename):
        '''Méthode destinée à extraire le dialogue d'un fichier texte'''
        with open(f'dialogues/{filename}.txt', 'r') as f:
            lignes = f.readlines()
    
        return lignes
    
    def next_dialogue(self):
        '''Méthode destinée à défiler le bon dialogue en fonction de la situation'''
        self.dialogue_index += 1

        if self.dialogue_index >= len(self.dialogues):
            self.finished = True
    
    def draw_dialogue(self, screen, screen_width, screen_height):
        '''Méthode destinée à afficher les boites de dialogues'''
        # les boites de dialogues sont en bas de l'écran
        box_x = 50
        box_y = screen_height - 150
        box_w = screen_width - 100
        box_h = 120

        pygame.draw.rect(screen, self.BROWN, (box_x, box_y, box_w, box_h), border_radius=10)
        pygame.draw.rect(screen, self.WHITE, (box_x, box_y, box_w, box_h), 2, border_radius=10)

        # texte
        if self.dialogue_index < len(self.dialogues):
            font = pygame.font.Font(None, 36)
            text = self.dialogues[self.dialogue_index].strip()  # .strip() enlève le \n
            text_surface = font.render(text, True, self.WHITE)
            screen.blit(text_surface, (box_x + 20, box_y + 40))