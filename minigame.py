import pygame
from random import randint

class Projectile(pygame.sprite.Sprite):

    def __init__(self, x, y, speed):
        super().__init__()

        # définition des variables indispensables
        self.image = pygame.image.load('objects/skull.png')
        self.image = pygame.transform.scale(self.image, (15, 15))

        self.rect = self.image.get_rect()
        self.place_rect(x, y)

        self.set_speed(speed)


    def move(self):

        self.rect.y += self.speed
    

    def missile_mode(self, rect):

        dx = rect.centerx - self.rect.centerx
        dy = rect.centery - self.rect.centery

        # Déplacement X
        if abs(dx) > 2:  
            step_x = self.speed if dx > 0 else -self.speed
            self.rect.x += step_x
 
        # Déplacement Y
        if abs(dy) > 2:
            step_y = self.speed if dy > 0 else -self.speed
            self.rect.y += step_y
    

    def place_rect(self, x, y):

        self.rect.x = x
        self.rect.y = y
    

    def set_speed(self, speed):

        self.speed = speed


    def draw_projectile(self, screen):
        
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Minigame(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()
        # définition des variables de l'écran de jeu
        self.width = 880 
        self.height = 520 
        self.x = 100 
        self.y = 100 

        # définition des variables pour notre curseur qui est un coeur
        self.image = pygame.image.load('objects/heart.png')
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = (self.width // 2) - (self.rect.width // 2)
        self.rect.y = self.y + self.height - self.rect.height - 5
        self.velocity = 5

        # pour le mini jeu 2 j'ai choisi d'ajouter un 2e rect
        self.rect2 = self.image.get_rect()

        # caractéristiques du rectangle jouable par le joueur
        self.movement = 5
        self.direction = 'right'
        self.WIDTH_RECT = 50
        self.HEIGHT_RECT = 30
        self.POS_X = self.x
        self.POS_Y = (self.y + (self.height / 2)) - (self.HEIGHT_RECT / 2)
        self.COLOR = (0, 0, 0)

        # gestion des projectiles
        self.projectiles = pygame.sprite.Group()
        self.spawn_time = 0

        # gestion de la victoire pour mini 1 et 4 (10 secondes de survie)
        self.survival_timer = 0
        self.survival_duration = 600 # 10 s à 60 fps    
        
        # gestion de l'état du mini jeu 
        self.finished = False
        self.win = None

        # grille du mini jeu 2
        self.grille = self.grille_minigame2()

        # position du rect 2
        self.place_cursor_and_win_case()

        # gestion de la grille du mini jeu 2 (au bout de 10s la grille se redessine)
        self.compteur = 0

        # coordonnées de la case gagnante (mini jeu 2)
        self.i = 0
        self.j = 0
        
    
    def move_right(self):
        
        self.rect.x += self.velocity
    

    def move_left(self):
        
        self.rect.x -= self.velocity
    

    def move_case_right(self):

        if self.rect2.x + 60 <= self.width + self.x:
            self.rect2.x += 60

    
    def move_case_left(self):

        if self.rect2.x - 60 >= self.x:
            self.rect2.x -= 60
    

    def move_case_up(self):

        if self.rect2.y - 60 >= self.y:
            self.rect2.y -= 60
    

    def move_case_down(self):

        if self.rect2.y + 60 <= self.y + self.height:
            self.rect2.y += 60
    

    def player_turn_minigame(self, screen):

        # mini jeu
        middle_x = (self.x + (self.width + self.x)) / 2
        pygame.draw.rect(screen, self.COLOR, (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2, border_radius=10)
        pygame.draw.line(screen, (255, 255, 255), (middle_x, self.y), (middle_x, self.height + self.y), 1)

        # RECT où le joueur doit interragir avec dans le mini jeu (pas le curseur) pour gagner
        RECT = pygame.draw.rect(screen, (255, 255, 255), (self.POS_X, self.POS_Y, self.WIDTH_RECT, self.HEIGHT_RECT), border_radius=10)

    
    def RECT_movements(self):

        self.POS_X += self.movement * (1 if self.direction == 'right' else -1)

        if self.POS_X + self.WIDTH_RECT >= self.width + self.x:
            self.direction = 'left'
            
        elif self.POS_X <= self.x:
            self.direction = 'right'
    

    def update_player_minigame(self):

        self.RECT_movements()
        middle = (self.x + (self.width + self.x)) / 2
        
        if middle - 50 <= self.POS_X <= middle + 50:
            self.COLOR = (0, 128, 0)

        else:
            self.COLOR = (0, 0, 0)


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
        self.survival_timer += 1

        if self.survival_timer >= self.survival_duration:
            self.finished = True
            self.win = True
            return 

        if hits:
            self.finished = True
            self.win = False
            return 

        if self.spawn_time >= 60:
            x = randint(100, 880)
            y = 100
            speed = 3
            self.projectiles.add(Projectile(x, y, speed))
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

                pygame.draw.rect(screen, color, pygame.Rect(x1, y1, case, case))
                pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(x1, y1, case, case), 1)
        
        pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(self.j, self.i, case, case))
        
        screen.blit(self.image, (self.rect2.x, self.rect2.y))
    

    def update_minigame_2(self):
        
        case = 60
        col = (self.rect2.centerx - 400) // case
        line = (self.rect2.centery - 200) // case

        cols = 400 // case
        lines = 300 // case

        if not (0 <= col < cols and 0 <= line < lines):
            return

        self.compteur += 1

        if self.compteur >= 200: # 60 fps à chaque tour de boucle, ici 10s = 10 tours de boucles donc 10 x 60 = 600 fps
            self.grille = self.grille_minigame2()
            self.compteur = 0
        
        if self.grille[line][col] == 1:
            self.finished = True
            self.win = False
        
        elif self.j == line and self.i == col:
            self.finished = True
            self.win = True

                
    def place_cursor_and_win_case(self):

        case = 60
        cols = 400 // case
        lines = 300 // case

        # case gagnante
        line = randint(0, lines - 1)
        col = randint(0, cols - 1)
        self.i = 200 + (case * line)
        self.j = 400 + (case * col)
        
        # curseur
        for i in range(lines):
            for j in range(cols):
                if self.grille[i][j] == 0 and not (i == line and j == col):
                    self.rect2.y = 200 + (case * i) + (case // 2) - (self.rect.height // 2)
                    self.rect2.x = 400 + (case * j) + (case // 2) - (self.rect.width // 2)
                    return
    

    def get_pos_cursor(self):

        if self.x < self.rect.x < self.width and self.y < self.rect.y < self.height:
            mx, my = pygame.mouse.get_pos()
            self.rect.x = mx
            self.rect.y = my
        
        else:
            self.rect.x = self.x + (self.width / 2)
            self.rect.y = self.y + (self.height / 2)

    
    def draw_minigame_4(self, screen):

        # mini jeu
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2, border_radius=10)

        # curseur
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # projectiles
        for projectile in self.projectiles:
            projectile.draw_projectile(screen)
    

    def update_minigame_4(self):

        hits = pygame.sprite.spritecollide(self, self.projectiles, False)
        self.spawn_time += 1
        self.survival_timer += 1

        if self.survival_timer > self.survival_duration:
            self.finished = True
            self.win = True
            return
        
        if hits:
            self.finished = True
            self.win = False
            return 

        if self.spawn_time >= 60: 
            x = randint(100, 880)
            y = randint(100, 520)
            speed = 1
            self.projectiles.add(Projectile(x, y, speed))
            self.spawn_time = 0

        for projectile in self.projectiles:
            if projectile.rect.y < (620 - projectile.rect.height): # 15 = taille du projectile
                projectile.missile_mode(self.rect)
            else:
                projectile.kill()