import pygame
import animation
from animation import animations

class NPC(animation.AnimateSprite): # 'animation.AnimateSprite' est sensé être dans les parenthèses pour l'animation. Ainsi pour engendrer les boites de dialogues
    def __init__(self, x, y, filename, sprite, name):    # j'ai choisi de garder temporairement la classe Sprite. Lorsque l'animation sera requise oubliez pas de mettre l'animation dans le super
        super().__init__(sprite)

        # rectangle du joueur
        w, h = 32, 50
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y 

        # nom du npc
        self.name = name

        # couleur des dialogues
        self.WHITE = (255, 255, 255) # -> texte
        self.BLACK = (0, 0, 0) # -> fond

        # police
        self.font = pygame.font.Font('assets/PixelOperator8-Bold.ttf', 24)

        # dialogue + fonctionnement
        self.dialogues = self.load_dialogue(filename)
        self.dialogue_index = 0
        self.finished = False

        # Attention : le fichier texte contenant le dialogue doit avoir des lignes de la même longueur
        # que la 1ère ligne que j'ai mise dans npc_1 (dialogue) pour que tout s'affiche sans déborder de la boite
    

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

        pygame.draw.rect(screen, self.BLACK, (box_x, box_y, box_w, box_h), border_radius=10)
        pygame.draw.rect(screen, self.WHITE, (box_x, box_y, box_w, box_h), 2, border_radius=10)

        # texte
        if self.dialogue_index < len(self.dialogues):
            text = self.dialogues[self.dialogue_index].strip()  # .strip() enlève le \n
            text_surface = self.font.render(text, True, self.WHITE)
            screen.blit(text_surface, (box_x + 20, box_y + 40))

    def update_animation_npc(self):
        '''Méthode visant à animer le npc'''
        pass