import pygame
import os
# ------------------------------------------------------------------
# Chargement des animations
# ------------------------------------------------------------------
def load_animation_images(animation):
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
    sheet_width  = sprite_sheet.get_width()
    num_frames   = sheet_width // 96  # calcul automatique du nombre de frames
    frame_w = sprite_sheet.get_width() // num_frames
    frame_h = sprite_sheet.get_height() 

    for i in range(num_frames):
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
    # --- Joueur : déplacement ---
    'run_right'     : load_animation_images('run_right'),
    'run_left'      : load_animation_images('run_left'),
    'run_up'        : load_animation_images('run_up'),
    'run_down'      : load_animation_images('run_down'),
 
    # --- Joueur : idle (immobile) ---
    'idle_right'    : load_animation_images('idle_right'),
    'idle_left'     : load_animation_images('idle_left'),
    'idle_up'       : load_animation_images('idle_up'),
    'idle_down'     : load_animation_images('idle_down'),
 
    # --- Joueur : attaque directionnelle ---
    'attack1_right' : load_animation_images('attack1_right'),
    'attack1_left'  : load_animation_images('attack1_left'),
    'attack1_down'  : load_animation_images('attack1_down'),
    'attack1_up'    : load_animation_images('attack1_up'),
 
    # --- Knight : déplacement ---
    'WALK_right'    : load_animation_images('WALK_right'),
    'WALK_left'     : load_animation_images('WALK_left'),
 
    # --- Knight : idle & mort ---
    'IDLE'          : load_animation_images('IDLE'),
    'idle_r_knight' : load_animation_images('idle_right'),   # alias pour le knight
    'idle_l_knight' : load_animation_images('idle_left'),
    'DEATH'         : load_animation_images('DEATH'),
 
    # --- Knight : attaque ---
    'ATTACK 1'      : load_animation_images('ATTACK 1'),
 
    # --- Boss : dragon ---
    'dragon_state'   : load_animation_images('dragon_basic_state'),
    'dragon_walk'    : load_animation_images('dragon_walking'),
    'dragon_fight'   : load_animation_images('dragon_fighting'),
    'dragon_final'   : load_animation_images('dragon_final_state'),
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
