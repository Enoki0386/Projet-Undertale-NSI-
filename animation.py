import pygame
import os
# ------------------------------------------------------------------
# Chargement des animations
# ------------------------------------------------------------------
def load_animation_images(animation, num_frame):
    """
    Découpe un sprite sheet en liste de frames pygame.Surface.
 
    Le nombre de frames est calculé automatiquement (largeur / FRAME_W),
    donc ça s'adapte à n'importe quel sprite sheet sans changer le code.
 
    Si le fichier est introuvable, on retourne [] et on affiche un warning
    au lieu de planter tout le jeu — pratique pendant le développement.
    """
    path = f'Sprites/{animation}.png'
 
    if not os.path.exists(path):
        print(f'[animation] ⚠  sprite introuvable : {path}')
        return []
    
    images = []
    sprite_sheet = pygame.image.load(f'Sprites/{animation}.png')
    frame_w = sprite_sheet.get_width() // num_frame
    frame_h = sprite_sheet.get_height() 

    for i in range(num_frame):
        x = i * frame_w        # on commence à 0, chaque frame fait FRAME_WIDTH pixels
        image = pygame.Surface([frame_w, frame_h])
        image.blit(sprite_sheet, (0, 0), (x, 0, frame_w, frame_h))
        image.set_colorkey([0, 0, 0])
        images.append(image)

    return images
# ------------------------------------------------------------------
# Repertoire global :
#    · Joueur  → minuscule 
#    · Knight  → MAJUSCULE
#    · Boss    → dragon_*
# ------------------------------------------------------------------
 
animations = {
    # --- Joueur : déplacement ---                              num_frame = 8 pour le joueur 
    'run_right'     : load_animation_images('run_right', 8),
    'run_left'      : load_animation_images('run_left', 8),
    'run_up'        : load_animation_images('run_up', 8),
    'run_down'      : load_animation_images('run_down', 8),
 
    # --- Joueur : idle (immobile) ---
    'idle_right'    : load_animation_images('idle_right', 8),
    'idle_left'     : load_animation_images('idle_left', 8),
    'idle_up'       : load_animation_images('idle_up', 8),
    'idle_down'     : load_animation_images('idle_down', 8),
 
    # --- Joueur : attaque directionnelle ---
    'attack1_right' : load_animation_images('attack1_right', 8),
    'attack1_left'  : load_animation_images('attack1_left', 8),
    'attack1_down'  : load_animation_images('attack1_down', 8),
    'attack1_up'    : load_animation_images('attack1_up', 8),
 
    # --- Knight : déplacement ---                             num_frame = 8 en marche
    'WALK_right'    : load_animation_images('WALK_right', 8),
    'WALK_left'     : load_animation_images('WALK_left', 8),
 
    # --- Knight : idle & mort ---                             num frame = 7 en idle
    'IDLE'          : load_animation_images('IDLE', 7),        
    'idle_r_knight' : load_animation_images('idle_right', 7),   # alias pour le knight
    'idle_l_knight' : load_animation_images('idle_left', 7),
    'DEATH'         : load_animation_images('DEATH', 12),          # num_frame = 12 en mort 
 
    # --- Knight : attaque ---                                 num_frame = 6 en attaque
    'ATTACK 1'      : load_animation_images('ATTACK 1', 6),
 
    # --- Boss : dragon ---
    'dragon_state'   : load_animation_images('dragon_basic_state', 4), # 4 frames
    'dragon_walk'    : load_animation_images('dragon_walking', 8), # 8 frames
    'dragon_fight'   : load_animation_images('dragon_fighting', 16), # 16 frames
    'dragon_final'   : load_animation_images('dragon_final_state', 5), # 5 frames 

    # --- Npc : 1 ---
    'npc1_left'     : load_animation_images('npc1_left', 8),
    'npc1_front'     : load_animation_images('npc1_front', 8),
    'npc1_back'     : load_animation_images('npc1_back', 8),

    # --- Npc : 2 ---
    'npc2_left'     : load_animation_images('npc2_left', 8),
    'npc2_front'     : load_animation_images('npc2_front', 8),
    'npc2_back'     : load_animation_images('npc2_back', 8),

    # --- Npc : 3 ---
    'npc3_left'     : load_animation_images('npc3_left', 8),
    'npc3_front'     : load_animation_images('npc3_front', 8),
    'npc3_back'     : load_animation_images('npc3_back', 8)
}

# ------------------------------------------------------------------
# Animé les animation ? (by Matis)
# ------------------------------------------------------------------
class AnimateSprite(pygame.sprite.Sprite):
    '''Création de la classe AnimateSprite permettant d'animer des sprites, ainsi elle hérite de la classe pygame sprite.Sprite, récupérant ses caractéristiques'''
    def __init__(self, animation):
        '''Création de l'objet AnimateSprite
           PS: Pour gérer les animations, dans le dossier du projet, il ya un sous dossier nommé 'Sprites', il contient des sprite sheet, donc des images au
           format .png, chaque image contient les positions successives du personnage, mes méthodes vont donc découper ces sprites sheets afin d'y créer une
           une animation '''
        super().__init__()
 
        self.current_image = 0
        self.images        = animations.get(animation,[])
 
        # Image initiale = première frame, ou surface vide si animation absente
        self.image = self.images[0].copy() if self.images else pygame.Surface([96, 80])
        self.image.set_colorkey((0, 0, 0))

    def set_animation(self, key):
        '''Change l'animation seulement si elle est différente de l'actuelle.
        Remet current_image à 0 pour éviter les freezes sur une mauvaise frame.'''
        #Débuged !!
        anim = animations.get(key)
        if anim is not None and self.images is not anim:
            self.images        = anim
            self.current_image = 0

    def animate(self):
        if not self.images:  # sécurité si la liste est None ou vide
            return
        '''Cette méthode permet de faire défiler les positions pour réaliser une animation'''

        self.current_image = (self.current_image + 1) % len(self.images)
        self.image         = self.images[self.current_image]
        self.image.set_colorkey([0, 0, 0])