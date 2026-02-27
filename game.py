import pygame
from player import Player # import de la classe Player du fichier player.py


class Game:

    def __init__(self):
        # Player est une sous-classe de Game
        
        self.player = Player() # création du joueur 
        self.pressed = {} # dictionnaire assignant une touche à son état