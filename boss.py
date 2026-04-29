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
        self.attack = 10
    
    def update_animation_boss(self):
        '''Méthode destinée à animer le dragon'''
        self.animate()

    def damage(self, amount):
        self.health = max(0, self.health - amount)
    
    def main_health_bar(self, surface):
        '''Affiche une grande barre de vie en bas à gauche de l'écran'''
        pygame.draw.rect(surface, (200, 0, 0), (20, 60, self.max_health * 8, 40))
        pygame.draw.rect(surface, (80, 210, 40), (20, 60, max(0, self.health) * 8, 40))
        pygame.draw.rect(surface, (255, 255, 255), (20, 60, self.max_health * 8, 40), 1)


class Samurai(animation.AnimateSprite):
    '''Cette classe est en construction, elle devrait créer le boss du jeu. Cependant ici, elle sert uniquement à déclencher une
    mécanique du jeu, qui est le mini-jeu. Ainsi il n'y a pas d'animations, de collisions encore.'''
    def __init__(self, x, y):
        '''Quelques caractéristiques de l'objet'''
        super().__init__('samurai_idle')
        w, h =  96, 96
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.x = x 
        self.rect.y = y
        self.health = 1000
        self.max_health = 1000
        self.attack = 10
    
    def update_animation_boss(self):
        '''Méthode destinée à animer le dragon'''
        self.animate()

    def damage(self, amount):
        self.health = max(0, self.health - amount)

    def main_health_bar(self, surface):
        '''Affiche une grande barre de vie en bas à gauche de l'écran'''
        pygame.draw.rect(surface, (200, 0, 0), (20, 60, self.max_health * 8, 40))
        pygame.draw.rect(surface, (80, 210, 40), (20, 60, max(0, self.health) * 8, 40))
        pygame.draw.rect(surface, (255, 255, 255), (20, 60, self.max_health * 8, 40), 1)


class Ghost(animation.AnimateSprite):
    '''Cette classe est en construction, elle devrait créer le boss du jeu. Cependant ici, elle sert uniquement à déclencher une
    mécanique du jeu, qui est le mini-jeu. Ainsi il n'y a pas d'animations, de collisions encore.'''
    def __init__(self, x, y):
        '''Quelques caractéristiques de l'objet'''
        super().__init__('ghost_idle')
        w, h = 153, 170
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.x = x 
        self.rect.y = y
        self.health = 1000
        self.max_health = 1000
        self.attack = 10
    
    def update_animation_boss(self):
        '''Méthode destinée à animer le dragon'''
        self.animate()
    
    def damage(self, amount):
        self.health = max(0, self.health - amount)

    def main_health_bar(self, surface):
        '''Affiche une grande barre de vie en bas à gauche de l'écran'''
        pygame.draw.rect(surface, (200, 0, 0), (20, 60, self.max_health * 8, 40))
        pygame.draw.rect(surface, (80, 210, 40), (20, 60, max(0, self.health) * 8, 40))
        pygame.draw.rect(surface, (255, 255, 255), (20, 60, self.max_health * 8, 40), 1)