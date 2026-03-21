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
        self.run()

  
    def handle_wall_collisions(self, direction):

        hits = pygame.sprite.spritecollide(self.map.player, self.map.wall_group, False)

        for wall in hits:
            if direction == 'right':
                self.map.player.rect.right = wall.rect.left
            elif direction == 'left':
                self.map.player.rect.left = wall.rect.right
            elif direction == 'down':
                self.map.player.rect.bottom = wall.rect.top
            elif direction == 'up':
                self.map.player.rect.top = wall.rect.bottom   


    def handle_monster_collisions(self, direction):

        hits = pygame.sprite.spritecollide(self.map.player, self.map.all_monsters, False, pygame.sprite.collide_mask)

        for monster in hits:
            if direction == 'right':
                self.map.player.rect.right = monster.rect.left
            elif direction == 'left':
                self.map.player.rect.left = monster.rect.right
            elif direction == 'down':
                self.map.player.rect.bottom = monster.rect.top
            elif direction == 'up':
                self.map.player.rect.top = monster.rect.bottom
    
    
    def handle_monster_wall_collisions(self, monster):

        hits = pygame.sprite.spritecollide(monster, self.map.wall_group, False)

        for wall in hits:
            if monster.direction == 1:
                monster.rect.right = wall.rect.left
                monster.direction = -1
            elif monster.direction == -1:
                monster.rect.left == wall.rect.right
                monster.direction = 1


    def inventory(self):

        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        pygame.draw.rect(self.screen, (20, 20, 30), (200, 100, 400, 300), border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), (200, 100, 400, 300), 2, border_radius=10)

        for i in range(9):
            x = 220 + (i % 3) * 120
            y = 140 + (i // 3) * 80
            pygame.draw.rect(self.screen, (80, 80, 80), (x, y, 80, 60))
            pygame.draw.rect(self.screen, (200, 200, 200), (x, y, 80, 60), 1)

                
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
            
            for monster in self.map.all_monsters:
                self.screen.blit(monster.image, (monster.rect.x - self.camera_x, monster.rect.y - self.camera_y))

            self.screen.blit(self.map.walls, (-self.camera_x, -self.camera_y))
            
            # En fonction des touches cliquées, le joueur se déplace tout en restant dans la zone du jeu, ici les touches peuvent être
            # maintenue afin de ne pas cliquer indéfiniment à chaque pixel
            if self.map.player.pressed.get(pygame.K_d) and self.map.player.rect.right < self.map.width:
                self.map.player.move_right()
                self.map.update_player()
                self.handle_wall_collisions(self.map.player.direction)
                self.handle_monster_collisions(self.map.player.direction)
            
            elif self.map.player.pressed.get(pygame.K_q) and self.map.player.rect.x > 0:
                self.map.player.move_left()
                self.map.update_player()
                self.handle_wall_collisions(self.map.player.direction)
                self.handle_monster_collisions(self.map.player.direction)

            elif self.map.player.pressed.get(pygame.K_s) and self.map.player.rect.bottom < self.map.height:
                self.map.player.move_back()
                self.map.update_player()
                self.handle_wall_collisions(self.map.player.direction)
                self.handle_monster_collisions(self.map.player.direction)
            
            elif self.map.player.pressed.get(pygame.K_z) and self.map.player.rect.y > 0:
                self.map.player.move_front()
                self.map.update_player()
                self.handle_wall_collisions(self.map.player.direction)
                self.handle_monster_collisions(self.map.player.direction)
            
            if self.map.player.inventor:
                self.inventory()
            

            if self.map.player.attacking:
                self.map.update_player()
                self.map.player.anim_count += 1

                if self.map.player.anim_count >= len(self.map.player.images):
                    self.map.player.attacking = False
                    self.map.player.anim_count = 0


            for monster in self.map.all_monsters:
                player = self.map.player
                monster.health_bar(self.screen, self.camera_x, self.camera_y)
                self.handle_monster_wall_collisions(monster)

                if monster.health == 0:
                    monster.kill()

                if abs(player.rect.centerx - monster.rect.centerx) < 100 and abs(player.rect.centery - monster.rect.centery) < 100:
                    monster.chase_player(player)
                else:
                    monster.default_state()
                    
                self.map.update_monsters()
                

            pygame.display.flip() # mise à jour de l'interface 


            # fermeture du jeu si le joueur quitte la fenêtre
            for event in pygame.event.get(): #.get() est un tuple de sortie de jeu

                if event.type == pygame.QUIT: # si l'événement est une sortie de jeu
                    running = False # la boucle du jeu est arrêtée
                    pygame.quit()
                    print('Fermeture du jeu')

                # les touches ne peuvent pas être maintenue ici, un clic = un événement fini

                if event.type == pygame.KEYDOWN: # si une touche est appuyée
                    self.map.player.pressed[event.key] = True # elle est assignée à True dans le dictionnaire de game.py

                    if event.key == pygame.K_LSHIFT and 600 < self.map.player.rect.centerx < 630 and 630 < self.map.player.rect.centery < 660:
                        self.map.load_maps(2, 28, 653)
                    
                    elif event.key == pygame.K_LSHIFT and 25 < self.map.player.rect.centerx < 66 and 640 < self.map.player.rect.centery < 700:
                        self.map.load_maps(1, 600, 630)
                    
                    if event.key == pygame.K_e:
                        self.map.player.inventor = not self.map.player.inventor


                elif event.type == pygame.KEYUP: # si la touche n'est pas appuyée
                    self.map.player.pressed[event.key] = False # elle est assignée à False
                

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.map.player.pressed[event.button] = True  

                    if self.map.player.pressed.get(1):
                        self.map.player.attacking = True
                        self.map.player.current_image = 0
                        self.map.player.attack()

                        if abs(player.rect.centerx - monster.rect.centerx) < 5 and abs(player.rect.centery - monster.rect.centery) < 5: 
                            monster.damage(10)
        

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.map.player.pressed[event.button] = False
                    
            
            clock.tick(60)