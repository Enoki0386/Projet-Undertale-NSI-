import pygame
from random import randint

class Projectile(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = randint(100, 880)
        self.rect.y = 100
        self.speed = 3
    

    def move(self):

        self.rect.y += self.speed
    

    def draw_projectile(self, screen):
        
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x, self.rect.y, self.rect.width, self.rect.height))


class Minigame(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()
        # définition des variables de l'écran de jeu
        self.width = 880 # 400
        self.height = 520 # 340
        self.x = 100 # 340
        self.y = 100 # 280

        # définition des variables pour notre curseur qui est un coeur
        self.image = pygame.image.load('objects/heart.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = (self.width // 2) - (self.rect.width // 2)
        self.rect.y = self.height + (100 - self.rect.height) - 10
        self.velocity = 5

        # gestion des projectiles
        self.projectiles = pygame.sprite.Group()
        self.spawn_time = 0
        
        # gestion de l'état du mini jeu 
        self.finished = False

        # grille du mini jeu 2
        self.grille = self.grille_minigame2()

        # gestion de la grille du mini jeu 2 (au bout de 10s la grille se redessine)
        self.compteur = 0

    
    def move_right(self):
        
        self.rect.x += self.velocity
    

    def move_left(self):
        
        self.rect.x -= self.velocity
    

    def move_back(self):
        
        self.rect.y -= self.velocity
    

    def move_front(self):
        
        self.rect.y += self.velocity
    

    def draw_mini_game(self, screen):

        # mini jeu
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2, border_radius=10)

        # curseur
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # projectiles
        for projectile in self.projectiles:
            projectile.draw_projectile(screen)
    

    def update_projectile(self):

        hits = pygame.sprite.spritecollide(self, self.projectiles, False)
        self.spawn_time += 1

        if hits:
            self.finished = True
            return 

        if self.spawn_time >= 60: 
            self.projectiles.add(Projectile())
            self.spawn_time = 0

        for projectile in self.projectiles:
            if projectile.rect.y < (620 - projectile.rect.height): # 15 = taille du projectile
                projectile.move()
            else:
                projectile.kill()
    

    def grille_minigame2(self):

        grille = []
        case = 60
        cols = 400 // case
        lines = 300 // case

        for y in range(lines):
            ligne = []

            for x in range(cols):
                ligne.append(randint(0, 1))
            
            grille.append(ligne)
        
        return grille


    def draw_minigame_2(self, screen):

        # mini jeu
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2, border_radius=10)

        case = 60
        cols = 400 // case
        lines = 300 // case

        for y in range(lines):
            for x in range(cols):
                x1 = 400 + (x * case)
                y1 = 200 + (y * case)
                
                if self.grille[y][x] == 0:
                    color = (0, 0, 0)
                else:
                    color = (255, 255, 255)

                rect = pygame.draw.rect(screen, color, pygame.Rect(x1, y1, case, case))
                pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(x1, y1, case, case), 1)

        # curseur
        screen.blit(self.image, (self.rect.x, self.rect.y))
    

    def update_minigame_2(self):
        self.compteur += 1

        if self.compteur >= 600: # 60 fps à chaque tour de boucle, ici 10s = 10 tours de boucles donc 10 x 60 = 600 fps
            self.grille = self.grille_minigame2()
            self.compteur = 0