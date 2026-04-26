import pygame
import animation
from animation import animations

# ─────────────────────────────────────────────────────────────────────────────
#  Paramètres du boss — tuner ici pour équilibrer la difficulté
# ─────────────────────────────────────────────────────────────────────────────
Detect_range   = 400   # distance à laquelle le dragon commence à se déplacer
Minigame_range = 80    # distance pour déclencher le mini-jeu (ancienne valeur : 50)
BOSS_VELOCITY  = 1.2   # plus lent que le joueur pour rester rattrapable
MAP_PADDING    = 10

class Boss(animation.AnimateSprite):
    '''Cette classe est en construction, elle devrait créer le boss du jeu. Cependant ici, elle sert uniquement à déclencher une
    mécanique du jeu, qui est le mini-jeu. Ainsi il n'y a pas d'animations, de collisions encore.'''
    def __init__(self, x, y):
        '''Quelques caractéristiques de l'objet'''
        super().__init__('dragon_state')
        w, h = 74, 74
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.x = x 
        self.rect.y = y
        self.health = 1000
        self.max_health = 1000
    
    def update_animation_boss(self):
        '''Méthode destinée à animer le dragon'''
        self.animate()