import pygame

class AnimateSprite(pygame.sprite.Sprite):
    '''Création de la classe AnimateSprite permettant d'animer des sprites, ainsi elle hérite de la classe pygame sprite.Sprite, récupérant ses caractéristiques'''
    def __init__(self, animation):
        '''Création de l'objet AnimateSprite
           PS: Pour gérer les animations, dans le dossier du projet, il ya un sous dossier nommé 'Sprites', il contient des sprite sheet, donc des images au
           format .png, chaque image contient les positions successives du personnage, mes méthodes vont donc découper ces sprites sheets afin d'y créer une
           une animation '''
        super().__init__() # récupération du init de la classe sprite.Sprite de pygame
        self.sprite_sheet = pygame.image.load(f'Sprites/{animation}.png') # récupération du sprite sheet spécifié avec une entrée, défini par la classe Player01 (player01.py) ou Knight (knight.py)
        self.image = self.get_image(0, 0) # position du personnage par defaut, c'est la première position du sprite sheet, récupéré par la méthode get_image()
        self.image.set_colorkey([0, 0, 0]) # pour avoir un fond transparent

        self.current_image = 0 # compteur de frame jouées
        self.images = animations.get(animation) # self.images contient une liste des positions découpées du sprite sheet grâce à la fonction load_animation_images, stocké dans le dictionnaire animations
    

    def animate(self):
        '''Cette méthode permet de faire défiler les positions pour réaliser une animation'''
        self.current_image += 1 # à l'appel de la méthode, une frame est défilée

        if self.current_image >= len(self.images): # si le nombre de frames défilées est supérieur au nombre de position dans la liste
            self.current_image = 0 # on revient à 0 car l'animation a été défilée
        
        self.image = self.images[self.current_image] # pour que les positions soit vraiment défilée, on prend la liste des position à l'index de l'image actuelle, cela est stocké dans self.image


    def get_image(self, x, y):
        '''Méthode permettant de récupérer une seule position du sprite sheet'''
        image = pygame.Surface([96, 80]) # on défini la surface de l'image voulu (correspond au pixels de notre sprite)
        image.blit(self.sprite_sheet, (0, 0), (x, y, 96, 80)) # on affiche le sprite sheet découpé sur une position

        return image # sauvegarde de cette première position


def load_animation_images(animation):
    '''Fonction (hors de la classe afin d'augmenter la rapidité du programme) permettant de découper le sprite sheet pour récupérer les positions qui sont stockées dans
       une liste, elle même valeur du dictionnaire animations assigné à la clé permettant de retrouver la liste'''
    images = [] 
    sprite_sheet = pygame.image.load(f'Sprites/{animation}.png') # load du sprite sheet
    x = 96 # largeur de la position (image) souhaitée

    for num in range(7): # le sprite sheet contient 7 positions de 96 pixels

        if x < 768: # si la largeur est conforme à la taille du sprite sheet
            image = pygame.Surface([96, 80]) # rectangle 
            image.blit(sprite_sheet, (0, 0), (x, 0, 96, 80)) # découpage
            image.set_colorkey([0, 0, 0]) # fond transparent
            images.append(image) # chaque position du sprite sheet est ajouté à la liste contenant l'animation
            x += 96 # on ajoute la largeur d'une position pour procéder au découpage de la position suivante
    
    return images


animations = {
    'run_right' : load_animation_images('run_right'),
    'run_left' : load_animation_images('run_left'),
    'run_up' : load_animation_images('run_up'),
    'run_down' : load_animation_images('run_down'),
    'attack1_right' : load_animation_images('attack1_right'),
    'attack1_left' : load_animation_images('attack1_left'),
    'attack1_down' : load_animation_images('attack1_down'),
    'attack1_up' : load_animation_images('attack1_up'),
    'WALK_right' : load_animation_images('WALK_right'),
    'WALK_left' : load_animation_images('WALK_left'),
    'DEATH' : load_animation_images('DEATH'),
    'dragon_state' : load_animation_images('dragon_basic_state')   
} # donc chaque liste de positions à sa clé dans ce dictionnaire