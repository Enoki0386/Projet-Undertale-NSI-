
import csv
import pygame
pygame.init()
from maps import Map

class Game01:
    
    def __init__(self):

        self.width = 1080
        self.height = 720

        pygame.display.set_caption('Undertale')
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.map = Map()

        self.map.load_maps(1, 430, 540)
        self.tile_size = 16
        self.walls = self.load_hitbox('carte1/carte_undertale._walls.csv')
    
        self.run()


    def load_hitbox(self, filename):

        rects = []

        with open(filename) as f:
            reader = csv.reader(f)
            for row_index, row in enumerate(reader):
                for col_index, tile in enumerate(row):
                    if int(tile.strip()) != -1:  
                        x = col_index * self.tile_size
                        y = row_index * self.tile_size
                        rects.append(pygame.Rect(x, y, self.tile_size, self.tile_size))

        return rects


    def run(self):

        clock = pygame.time.Clock()
        running = True

        while running:
            
            self.camera_x = self.map.player.rect.centerx - self.width // 2
            self.camera_y = self.map.player.rect.centery - self.height // 2

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.map.background, (-self.camera_x, -self.camera_y))
            self.screen.blit(self.map.path, (0-self.camera_x, -self.camera_y))
            self.screen.blit(self.map.player.image, (self.width // 2 - self.map.player.image.get_width() // 2, self.height // 2 - self.map.player.image.get_height() // 2))
            self.screen.blit(self.map.walls, (-self.camera_x, -self.camera_y))


            # En fonction des touches cliquées, le joueur se déplace tout en restant dans la zone du jeu, ici les touches peuvent être
            # maintenue afin de ne pas cliquer indéfiniment à chaque pixel
            if self.map.player.pressed.get(pygame.K_d) and self.map.player.rect.x + self.map.player.rect.width < self.map.width:
                self.map.player.move_right()
                self.map.update_player()

                for rect in self.walls:
                    if self.map.player.rect.colliderect(rect):
                        self.map.player.rect.right = rect.left
            
            elif self.map.player.pressed.get(pygame.K_q) and self.map.player.rect.x > 0:
                self.map.player.move_left()
                self.map.update_player()

                for rect in self.walls:
                    if self.map.player.rect.colliderect(rect):
                        self.map.player.rect.left = rect.right

            elif self.map.player.pressed.get(pygame.K_s) and self.map.player.rect.y + self.map.player.rect.height < self.map.height:
                self.map.player.move_back()
                self.map.update_player()

                for rect in self.walls:
                    if self.map.player.rect.colliderect(rect):
                        self.map.player.rect.bottom = rect.top
            
            elif self.map.player.pressed.get(pygame.K_z) and self.map.player.rect.y > 0:
                self.map.player.move_front()
                self.map.update_player()

                for rect in self.walls:
                    if self.map.player.rect.colliderect(rect):
                        self.map.player.rect.top = rect.bottom

            pygame.display.flip() # mise à jour de l'interface 


            # fermeture du jeu si le joueur quitte la fenêtre
            for event in pygame.event.get(): #.get() est un tuple de sortie de jeu

                if event.type == pygame.QUIT: # si l'événement est une sortie de jeu
                    running = False # la boucle du jeu est arrêtée
                    pygame.quit()
                    print('Fermeture du jeu')

                # les touches ne peuvent pas être maintenue ici, un clic = un événement fini

                elif event.type == pygame.KEYDOWN: # si une touche est appuyée
                    self.map.player.pressed[event.key] = True # elle est assignée à True dans le dictionnaire de game.py

                    if event.key == pygame.K_LSHIFT and 600 < self.map.player.rect.centerx < 630 and 630 < self.map.player.rect.centery < 660:
                        self.map.load_maps(2, 28, 653)
                        self.walls = self.load_hitbox('carte2/carte_undertale_2_walls.csv')
                    
                    elif event.key == pygame.K_LSHIFT and 25 < self.map.player.rect.centerx < 66 and 640 < self.map.player.rect.centery < 700:
                        self.map.load_maps(1, 600, 630)
                        self.walls = self.load_hitbox('carte1/carte_undertale._walls.csv')


                elif event.type == pygame.KEYUP: # si la touche n'est pas appuyée
                    self.map.player.pressed[event.key] = False # elle est assignée à False
            
            clock.tick(60)