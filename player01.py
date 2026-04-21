import pygame
import animation
from animation import animations

class Player01(animation.AnimateSprite):
    '''Cette classe Player01 va créer le joueur et hérite de la classe AnimateSprite gérant l'animation des entités (animation.py)'''

    def __init__(self):
        '''définition de l'objet Joueur'''
        super().__init__('run_right') # récupération du init de la classe AnimateSprite avec en entrée le nom de fichier qui va servir d'animation (par défaut)

        # définition des variables composant le joueur
        self.health = 25
        self.max_health = 25
        self.attacking = False # permet la gestion des attaques dans la classe Game01 du fichier game01.py
        self.just_attack = False
        self.velocity = 5 # vitesse de déplacement
        self.anim_count = 0 # nombre de frame jouée par la classe AnimateSPrite
        self.direction = 'right' # direction par defaut au lancement du jeu
        self.inventor = False # permet la gestion d'ouverture de l'inventaire
        w, h = 30, 40 # largeur, hauteur du rectangle du joueur
        self.rect = pygame.Rect(430 + (96 - w) // 2, 540 + (80 - h) // 2, w, h) # rectangle du joueur, calculé afin d'être centré sur le joueur (avec la position, les proportions de l'image en pixel)
        self.rect.x = 430 + (96 - w) // 2 # position du rectangle en x
        self.rect.y = 540 + (80 - h) // 2 # position du rectangle en y
        self.pressed = {} # dictionnaire gérant les touches controllant le joueur (True = appuyé, False = relaché)
    

    def update_animation_player(self):
        '''Cette méthode va appeler la méthode self.animate issu de la classe AnimateSprite afin de mettre à jours les images de l'animation'''
        self.animate()


    def move_right(self):
        '''Méthode visant à déplacer le joueur vers la droite tout en actualisant l'animation
           PS: animations est un dictionnaire contenant des listes des positions successives des animations, les clés sont déjà définies'''
        self.images = animations.get('run_right') # on stocke l'image du déplacement dans self.images, variable de AnimateSprite
        self.rect.x += self.velocity # déplacement de la coordonnée x de la hitbox
        self.direction = 'right' # mise à jours de la direction utile pour la gestion des attaques
    

    def move_left(self):
        '''Méthode visant à déplacer le joueur vers la gauche tout en actualisant l'animation'''
        self.images = animations.get('run_left')
        self.rect.x -= self.velocity # on stocke l'image du déplacement dans self.images, variable de AnimateSprite
        self.direction = 'left' # mise à jours de la direction utile pour la gestion des attaques
    

    def move_back(self):
        '''Méthode visant à déplacer le joueur vers le bas tout en actualisant l'animation'''
        self.images = animations.get('run_down')
        self.rect.y += self.velocity # on stocke l'image du déplacement dans self.images, variable de AnimateSprite
        self.direction = 'down' # mise à jours de la direction utile pour la gestion des attaques
    

    def move_front(self):
        '''Méthode visant à déplacer le joueur vers le haut tout en actualisant l'animation'''
        self.images = animations.get('run_up')
        self.rect.y -= self.velocity # on stocke l'image du déplacement dans self.images, variable de AnimateSprite
        self.direction = 'up' # mise à jours de la direction utile pour la gestion des attaques


    def attack(self):
        '''Méthode visant à déclencher l'animation d'attaque. En fonction de self.direction défini plus tôt, si le joueur lance une attaque, l'animation sera adaptée
        en fontion de sa position'''
        if self.direction == 'right':
            self.images = animations.get('attack1_right')
        
        if self.direction == 'left':
            self.images = animations.get('attack1_left')

        if self.direction == 'down':
            self.images = animations.get('attack1_down')

        if self.direction == 'up':
            self.images = animations.get('attack1_up')
    

    def health_bar(self, surface, camera_x, camera_y):

        bar_color_health = (111, 210, 46)
        bar_color = (255, 0, 0)

        bar_x = self.rect.x - camera_x + 10
        bar_y = self.rect.y - camera_y - 10

        bar_position_health = [bar_x, bar_y, self.health, 5]
        bar_position = [bar_x, bar_y, self.max_health, 5]

        pygame.draw.rect(surface, bar_color, bar_position)
        pygame.draw.rect(surface, bar_color_health, bar_position_health)
    

    def damage(self, amount):

        self.health -= amount

        if self.health <= 0:
            self.health = 0