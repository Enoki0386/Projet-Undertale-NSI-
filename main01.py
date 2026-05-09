import pygame
from game01 import Game01
from title import TitleScreen

if __name__ == '__main__':
    # Initialisation de pygame ici pour que TitleScreen puisse s'en servir
    pygame.init()
    screen = pygame.display.set_mode((1080, 720))   
    pygame.display.set_caption('Undertale')
 
    # Lance l'écran titre → attend le choix du joueur
    action = TitleScreen(screen).run() 
 
    if action == 'play':
        # On passe l'écran déjà créé à Game01 pour éviter de recréer la fenêtre
        game = Game01()
    game = Game01()