import pygame
import animation
from animation import animations
# ------------------------------------------------------------------
# Répertoire des animations
# ------------------------------------------------------------------
Run_anim = {
    'right': 'run_right',
    'left':  'run_left',
    'down':  'run_down',
    'up':    'run_up',
}
Atq_anim = {
    'right': 'attack1_right',
    'left':  'attack1_left',
    'down':  'attack1_down',
    'up':    'attack1_up',
}

Idle_anim = {
    'right': 'idle_right',
    'left':  'idle_left',
    'down':  'idle_down',
    'up':    'idle_up',
}
Diagonal = 0.707   # 1 / √2 (merci les maths)

class Player01(animation.AnimateSprite):
    '''Cette classe Player01 va créer le joueur et hérite de la classe AnimateSprite gérant l'animation des entités (animation.py)'''

    def __init__(self):
        '''définition de l'objet Joueur'''
        super().__init__('idle_right') # récupération du init de la classe AnimateSprite avec en entrée le nom de fichier qui va servir d'animation (par défaut)

        # définition des variables composant le joueur
        self.health         = 25
        self.max_health     = 25
        self.velocity       = 5             # vitesse de déplacement
        self.direction      = 'right'       # direction par defaut au lancement du jeu

        self.protection = 0                 # armure du joueur (initialement nulle)
        self.max_protection = 25            # avec un bouclier

        self.attacking      = False         # permet la gestion des attaques dans la classe Game01 du fichier game01.py
        self.just_attack    = False
        self.moving         = False         # True si une touche de déplacement est pressée (pour idle)
        self.anim_count     = 0             # nombre de frame jouée par la classe AnimateSPrite
        self.inventor       = False         # permet la gestion d'ouverture de l'inventaire

        w, h                = 30, 40        # largeur, hauteur du rectangle du joueur
        start_y      = 540
        start_x      = 430
        self.rect    = pygame.Rect(start_x + (96 - w) // 2, start_y + (80 - h) // 2, w, h)

        # Position flottante pour accumuler les fractions de déplacement
        self._fx: float = float(self.rect.x)
        self._fy: float = float(self.rect.y)
 
        self.pressed: dict = {}   # état des touches : {key: True/False}
    # ------------------------------------------------------------------
    # Update l'animation si elle change
    # ------------------------------------------------------------------
    '''def set_animation(self, key):
        anim = animations.get(key)
        if anim is not None and self.images is not anim:
            self.images = anim
            self.current_image = 0'''

    def update_animation_player(self):
        '''Cette méthode va appeler la méthode self.animate issu de la classe AnimateSprite afin de mettre à jours les images de l'animation'''
        self.animate()

    # ------------------------------------------------------------------
    # Déplacements
    # ------------------------------------------------------------------


    def move(self, dx: float, dy: float) -> None:
        """
        Déplace le joueur selon un vecteur (dx, dy) où chaque composante vaut
        -1, 0 ou 1 (déjà normalisé si diagonal → passer DIAGONAL_FACTOR depuis game01).
 
        Logique d'animation :
          · Horizontal (gauche/droite) prioritaire — plus lisible visuellement.
          · Vertical (haut/bas) seulement si on ne va pas latéralement.
        """
        self._fx += dx * self.velocity
        self._fy += dy * self.velocity
        self.rect.x = int(self._fx)
        self.rect.y = int(self._fy)
 
        # Mise à jour de la direction (horizontale prioritaire)
        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy > 0:
            self.direction = 'down'
        elif dy < 0:
            self.direction = 'up'
 
        self.set_animation(Run_anim[self.direction])

    
    def sync_float_pos(self) -> None:
        """
        Resynchronise la position flottante après une correction de collision.
        À appeler dans game01 APRÈS avoir modifié player.rect suite à un mur.
        Sans ça, la position flottante dériverait et annulerait la correction.
        """
        self._fx = float(self.rect.x)
        self._fy = float(self.rect.y)
        
    # ------------------------------------------------------------------
    # Attaque et idle
    # ------------------------------------------------------------------
    def attack(self):
        self.set_animation(Atq_anim[self.direction])
    
    def idle(self):
        self.set_animation(Idle_anim[self.direction])
    # ------------------------------------------------------------------
    # Vie et dégats recus
    # ------------------------------------------------------------------
    def health_bar(self, surface: pygame.Surface, cam_x: int, cam_y: int) -> None:
        """Affiche la barre de vie au-dessus du joueur, corrigée par la caméra."""
        bx = self.rect.x - cam_x + 10
        by = self.rect.y - cam_y - 12
 
        pygame.draw.rect(surface, (200, 0, 0),    (bx, by, self.max_health, 6))
        pygame.draw.rect(surface, (80, 210, 40),  (bx, by, max(0, self.health), 6))
        pygame.draw.rect(surface, (255, 255, 255),(bx, by, self.max_health, 6), 1)
    
    def main_health_bar(self, surface, screen_height):
        '''Affiche une grande barre de vie en bas à gauche de l'écran'''
        pygame.draw.rect(surface, (200, 0, 0), (20, screen_height - 60, self.max_health * 8, 40))
        pygame.draw.rect(surface, (80, 210, 40), (20, screen_height - 60, max(0, self.health) * 8, 40))
        pygame.draw.rect(surface, (255, 255, 255), (20, screen_height - 60, self.max_health * 8, 40), 1)
    
    def protection_bar(self, surface, screen_height):
        '''Affiche une barre mesurant le niveau d'armure du joueur (initialement nulle, s'augmente avec un bouclier)'''
        pygame.draw.rect(surface, (201, 229, 255), (20, screen_height - 60, self.max_protection * 8, 40))
        pygame.draw.rect(surface, (0, 139, 252), (20, screen_height - 60, max(0, self.protection) * 8, 40))
        pygame.draw.rect(surface, (255, 255, 255), (20, screen_height - 60, self.max_protection * 8, 40), 1)           
 
    def damage(self, amount: int) -> None:
        self.health = max(0, self.health - amount)