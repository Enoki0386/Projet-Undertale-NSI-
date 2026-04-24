import pygame
import animation
from animation import animations
# ─────────────────────────────────────────────────────────────────────────────
#  Paramètres de l'IA du chevalier — modifiables facilement ici
# ─────────────────────────────────────────────────────────────────────────────
Detect_range   = 200   # distance (px) à laquelle le knight détecte le joueur
Atq_range   = 55    # distance (px) pour déclencher l'attaque
Atq_dmg  = 5     # dégâts infligés au joueur par attaque
atq_cd = 90   # frames entre deux attaques (90f = 1.5 s à 60 fps)
 
PATROL_HALF    = 100   # amplitude de patrouille de chaque côté du point de spawn
MAP_PADDING    = 10    # marge (px) pour ne jamais sortir de la map
 
# ------------------------------------------------------------------
# Repertoire animations de marche
# ------------------------------------------------------------------
Walk_anim = {
    'right': 'WALK_right',
    'left' : 'WALK_left',
}
class Knight(animation.AnimateSprite):

    def __init__(self, x, y):
        super().__init__('WALK_right') # récupération du __init__ de la classe sprite de pygame

        # ── Stats ──
        self.health     = 25
        self.max_health = 25
        self.attack     = 10
        self.velocity   = 2.5
        self.direction  = 1 # 1 = droite, -1 = gauche
        # ── Hitbox ──
        # Petite hitbox centrée sur le bas du sprite (pied du personnage)
        w, h            = 56, 60
        self.rect       = pygame.Rect(x, y, w, h)

        # Masque pixel-perfect pour les collisions avec le joueur
        self.mask = pygame.mask.from_surface(self.image)

        # ── Patrouille ──
        self.spawn_x       = x
        self.patrol_right  = x + PATROL_HALF
        self.patrol_left   = max(MAP_PADDING, x - PATROL_HALF)
    
        # ── Direction ──
        # direction  : 'right' / 'left'  → pour l'animation
        # last_dir      : dernière direction horizontale connue (DEBUG)
        self.direction = 'right'
        self.last_dir     = 'right'   # garde la dernière direction horizontale
 
        # ── État ──
        self.state          = 'patrol'
        self.attack_timer   = 0    # compteur de cooldown entre les attaques
        self.attack_frame   = 0    # frame actuelle de l'animation d'attaque
        self.is_attacking   = False
 
        # ── Référence externe remplie par game01 ──
        # Permet au knight de savoir les limites de la map sans y avoir accès directement
        self.map_width  = 1600
        self.map_height = 1600

    # ─────────────────────────────────────────────────────────────────────────
    #  Knight principal
    # ─────────────────────────────────────────────────────────────────────────
 
    def update_ai(self, player) -> None:
        """
        Point d'entrée de l'IA. Calcule la distance au joueur, choisit l'état
        et appelle la méthode correspondante.
        Également responsable du cooldown d'attaque.
        """
        # Décrémenter le cooldown d'attaque
        if self.attack_timer > 0:
            self.attack_timer -= 1
 
        dist = self.dist_to(player)
 
        if dist < Atq_range:
            self.state = 'attack'
            self.do_attack(player)
        elif dist < Detect_range:
            self.state = 'chase'
            self.chase(player)
        else:
            self.state = 'patrol'
            self.patrol()
 
        # Clamp : le knight ne sort jamais de la map
        self.clamp_to_map()
 
        # Animation
        self.animate()
 
        # Mise à jour du masque après le mouvement (pour collisions pixel-perfect)
        self.mask = pygame.mask.from_surface(self.image)

    def update_animation_knight(self) -> None:
        """Gardé pour la compatibilité — l'animation est déjà appelée dans update_ai."""
        pass
    # ------------------------------------------------------------------
    # États du knight
    # ------------------------------------------------------------------
    def patrol(self):
        """
        Va et vient entre patrol_left et patrol_right.
        Animation uniquement horizontale (c'est tout ce qu'on a pour le knight).
        """
        self.rect.x += self.velocity * (1 if self.direction == 'right' else -1)
 
        if self.rect.x >= self.patrol_right:
            self.direction = 'left'
            self.last_dir     = 'left'
        elif self.rect.x <= self.patrol_left:
            self.direction = 'right'
            self.last_dir     = 'right'
 
        self.update_walk_anim()
    
    def chase(self, player) -> None:
        """
        Poursuit le joueur sur les deux axes (vrai déplacement 2D).
 
        Animation :
          · Horizontal → WALK_right ou WALK_left selon la position relative du joueur.
          · Vertical   → on garde la dernière direction horizontale connue (last_dir)
            pour éviter le bug "animation droite quand joueur est à gauche".
        """
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
 
        # Déplacement X
        if abs(dx) > 2:   # éviter les micro-oscillations
            step_x = self.velocity if dx > 0 else -self.velocity
            self.rect.x += step_x
            self.last_dir   = 'right' if dx > 0 else 'left'
 
        # Déplacement Y
        if abs(dy) > 2:
            step_y = self.velocity if dy > 0 else -self.velocity
            self.rect.y += step_y
 
        # L'animation se base sur last_dir (horizontale) même quand on monte/descend
        self.direction = self.last_dir
        self.update_walk_anim()
    
    def do_attack(self, player) -> None:
        """
        Joue l'animation d'attaque et inflige des dégâts au joueur.
        Le cooldown ATTACK_COOLDOWN évite de taper 60 fois/seconde.
        """
        # Se tourne vers le joueur avant d'attaquer
        if player.rect.centerx > self.rect.centerx:
            self.last_dir = 'right'
        else:
            self.last_dir = 'left'
        self.direction = self.last_dir
 
        self.set_animation('ATTACK_1')
        self.is_attacking = True
 
        if self.attack_timer == 0:
            player.damage(Atq_dmg)
            self.attack_timer = atq_cd   # recharge
    # ------------------------------------------------------------------
    # Animation et debug
    # ------------------------------------------------------------------

    def update_walk_anim(self):
        """Choisit WALK_right ou WALK_left selon last_dir."""
        key = 'WALK_right' if self.last_dir == 'right' else 'WALK_left'
        self.set_animation(key)
 
 
    def dist_to(self, player):
        """Distance entre le centre du knight et le joueur."""
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        return (dx ** 2 + dy ** 2) ** 0.5
 
 
    def clamp_to_map(self):
        """
        Empêche le knight de sortir de la map.
        C'est ici qu'on règle le problème du knight "poussé hors de la map"
        par le joueur : même si la collision avec le joueur le pousse, il ne
        franchira jamais les bords.
        """
        self.rect.left   = max(MAP_PADDING, self.rect.left)
        self.rect.right  = min(self.map_width  - MAP_PADDING, self.rect.right)
        self.rect.top    = max(MAP_PADDING, self.rect.top)
        self.rect.bottom = min(self.map_height - MAP_PADDING, self.rect.bottom)

    # ------------------------------------------------------------------
    # Vie et dégats subis
    # ------------------------------------------------------------------
    def health_bar(self, surface: pygame.Surface, cam_x: int, cam_y: int):
        bx = self.rect.centerx - self.max_health // 2 - cam_x
        by = self.rect.top - 10 - cam_y
 
        pygame.draw.rect(surface, (200, 0, 0),    (bx, by, self.max_health, 5))
        pygame.draw.rect(surface, (80, 210, 40),  (bx, by, max(0, self.health), 5))
        pygame.draw.rect(surface, (200, 200, 200),(bx, by, self.max_health, 5), 1)
 
    def damage(self, amount: int):
        self.health = max(0, self.health - amount)
        # Si mort : on déclenche l'animation DEATH avant le kill() dans game01
        if self.health == 0:
            self.set_animation('DEATH')
 
    def default_state(self):
        """Alias gardé pour la compatibilité — redirige vers patrol."""
        self.patrol()
        self.clamp_to_map()
        self.animate()
 
    def chase_player(self, player):
        """Alias gardé pour la compatibilité — redirige vers chase."""
        self.chase(player)
        self.clamp_to_map()
        self.animate()