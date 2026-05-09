import pygame
from tutoriel import Tutoriel
from animation import AnimateSprite


class Cinematique:
    def __init__(self, anim_key, dialogue):

        # définition des variables de l'écran de jeu
        self.width = 880 
        self.height = 340 
        self.x = 100 
        self.y = 280 # 270

        # définition des variables du boss
        self.sprite = AnimateSprite(anim_key)
        self.rect = pygame.Rect(self.x + 20, self.y + self.height // 2 - 40, 100, 100)
        self.anim_timer = 0

        # dialogue du boss
        self.dialogue = Tutoriel(dialogue)

        # gestion
        self.finished = False

    
    def update(self):
        
        self.dialogue.update()

        # animation du sprite
        self.anim_timer += 1
        if self.anim_timer >= 8:
            self.sprite.animate()
            self.anim_timer = 0
        
        if self.dialogue.finished:
            self.finished = True


    def draw_cinematique(self, screen, width, height):

        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2, border_radius=10)
        screen.blit(self.sprite.image, (self.x + 20, self.y + self.height // 2 - 40))

        self.dialogue.draw_dialogue(screen, width, height)