import pygame
pygame.init()
from maps import Map
# ------------------------------------------------------------------ 
#  Init + touches de deplacements                                          
# ------------------------------------------------------------------ 
Depl_key = {
    pygame.K_d: ( 1,  0),
    pygame.K_q: (-1,  0),
    pygame.K_s: ( 0,  1),
    pygame.K_z: ( 0, -1),
}

class Game01:
    def __init__(self):
        self.width      = 1080
        self.height     = 720

        self.state              = 'exploration'
        self.minigame_active    = False
        self.objects            = {}

        pygame.display.set_caption('Undertale')
        self.screen     = pygame.display.set_mode((self.width, self.height))
        self.map        = Map()

        self.init_inventory()
        self.give_start_item('start_sword')
        self.map.load_maps(1, 430, 540)
        self.run()
    # ------------------------------------------------------------------ 
    #  COLLISIONS (x,y séparer pour eviter bug de colision)                                                         
    # ------------------------------------------------------------------ 
  
    def resolve_wall_x(self, entity, dx: float) -> None:
        """Résout les collisions horizontales du joueur contre les murs."""
        for wall in pygame.sprite.spritecollide(entity, self.map.wall_group, False):
            if dx > 0:   # allait vers la droite → recule sur le bord gauche du mur
                entity.rect.right = wall.rect.left
            elif dx < 0: # allait vers la gauche → recule sur le bord droit du mur
                entity.rect.left  = wall.rect.right
 
 
    def resolve_wall_y(self, entity, dy: float) -> None:
        """Résout les collisions verticales du joueur contre les murs."""
        for wall in pygame.sprite.spritecollide(entity, self.map.wall_group, False):
            if dy > 0:
                entity.rect.bottom = wall.rect.top
            elif dy < 0:
                entity.rect.top    = wall.rect.bottom
 
 
    def resolve_monster_x(self, dx: float) -> None:
        """Résout les collisions horizontales joueur↔monstres."""
        for monster in pygame.sprite.spritecollide(
            self.map.player, self.map.all_monsters, False, pygame.sprite.collide_mask
        ):
            if dx > 0:
                self.map.player.rect.right = monster.rect.left
            elif dx < 0:
                self.map.player.rect.left  = monster.rect.right
 
 
    def resolve_monster_y(self, dy: float) -> None:
        """Résout les collisions verticales joueur↔monstres."""
        for monster in pygame.sprite.spritecollide(
            self.map.player, self.map.all_monsters, False, pygame.sprite.collide_mask
        ):
            if dy > 0:
                self.map.player.rect.bottom = monster.rect.top
            elif dy < 0:
                self.map.player.rect.top    = monster.rect.bottom
 
 
    def resolve_monster_walls(self, monster) -> None:
        """
        Résout les collisions d'un monstre contre les murs.
        On vérifie les 4 directions pour éviter que le knight traverse les murs
        quand il est "poussé" par le joueur.
        """
        for wall in pygame.sprite.spritecollide(monster, self.map.wall_group, False):
            # Calcul du chevauchement sur chaque axe pour choisir la bonne résolution
            overlap_left  = monster.rect.right  - wall.rect.left
            overlap_right = wall.rect.right     - monster.rect.left
            overlap_top   = monster.rect.bottom - wall.rect.top
            overlap_bot   = wall.rect.bottom    - monster.rect.top
 
            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bot)
 
            if min_overlap == overlap_left:
                monster.rect.right  = wall.rect.left
            elif min_overlap == overlap_right:
                monster.rect.left   = wall.rect.right
            elif min_overlap == overlap_top:
                monster.rect.bottom = wall.rect.top
            else:
                monster.rect.top    = wall.rect.bottom
 
    # ------------------------------------------------------------------ 
    #  INVENTAIRE                                                          
    # ------------------------------------------------------------------ 

    def init_inventory(self):
        '''Initialise la grille de l'inventaire sans l'afficher.'''
        case = 60
        cols = 400 // case
        rows = 300 // case
 
        for col in range(cols):
            for row in range(rows):
                x    = 400 + col * case
                y    = 200 + row * case
                rect = pygame.Rect(x, y, case, case)
                self.objects[(x, y)] = [rect, False, None, None]

    def give_start_item(self, name):
        image = pygame.image.load(f'objects/{name}.png')
        image = pygame.transform.scale(image, (50, 50))
        
        for key, slot in self.objects.items():
            if not slot[1]:
                slot[1], slot[2], slot[3] = True, image, name
                break
    
    def put_in_inventory(self, item):
        # Évite les doublons
        if any(slot[3] == item.name for slot in self.objects.values()):
            return

        for slot in self.objects.values():
            if not slot[1]:
                slot[1], slot[2], slot[3] = True, item.image, item.name
                break

    def inventory(self, mx, my):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        pygame.draw.rect(self.screen, (20, 20, 30), (380, 180, 400, 340), border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), (380, 180, 400, 340), 2, border_radius=10)

        for (x, y), slot in self.objects.items():
            rect  = slot[0]
            color = (120, 120, 120) if rect.collidepoint(mx, my) else (80, 80, 80)
 
            pygame.draw.rect(self.screen, color,           rect)
            pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
 
            if slot[1] and slot[2] is not None:
                self.screen.blit(slot[2], rect)

    # ------------------------------------------------------------------ 
    #  MINI-JEU                                                            
    # ------------------------------------------------------------------ 
    def launch_minigame(self, screen):

        self.map.minigame.draw_mini_game(screen)
        self.map.minigame.update_projectile()

        if self.map.minigame.finished:
            self.state = 'exploration'
            self.map.minigame.finished = False
            self.map.minigame.projectiles.empty()
    

    def launch_minigame2(self, screen):
        self.map.minigame.draw_minigame_2(screen)
        self.map.minigame.update_minigame_2()

        if self.map.minigame.finished:
            self.state = 'exploration'
            self.map.minigame.finished = False
    

    def launch_minigame_player(self, screen):
        self.map.minigame.player_turn_minigame(screen)
        self.map.minigame.update_player_minigame()

        if self.map.minigame.finished:
            self.state = 'exploration'
            self.map.minigame.finished = False
    

    def launch_minigame_4(self, screen):
        pygame.mouse.set_visible(False)
        self.map.minigame.draw_minigame_4(screen)
        self.map.minigame.update_minigame_4()
        self.map.minigame.get_pos_cursor()

        if self.map.minigame.finished:
            self.state = 'exploration'
            self.map.minigame.finished = True


    # ------------------------------------------------------------------ 
    #  Main boucle                                                       
    # ------------------------------------------------------------------ 
    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.fill((0, 0, 0))
            # Camera centré sur le joueur 
            cam_x = self.map.player.rect.centerx - self.width    // 2
            cam_y = self.map.player.rect.centery - self.height   // 2

            # --Événements--
            for event in pygame.event.get():        #.get() est un tuple de sortie de jeu
                if event.type == pygame.QUIT:       # si l'événement est une sortie de jeu
                    running = False                 # la boucle du jeu est arrêtée
                    pygame.quit()
                    print('Fermeture du jeu')

                # les touches ne peuvent pas être maintenue ici, un clic = un événement fini
                if event.type == pygame.KEYDOWN:                # si une touche est appuyée
                    self.map.player.pressed[event.key] = True   # elle est assignée à True dans le dictionnaire de game.py

                    if self.state == 'exploration':

                        # Changement de map
                        px, py = self.map.player.rect.centerx, self.map.player.rect.centery
                        if event.key == pygame.K_LSHIFT:
                            if 600 < px < 630 and 630 < py < 660:
                                self.map.load_maps(2, 28, 653)
                            elif 25 < px < 66 and 640 < py < 700:
                                self.map.load_maps(1, 600, 630)
                    
                        # Ramassage d'item
                        if event.key == pygame.K_f:
                            for item in self.map.items_group:
                                if abs(self.map.player.rect.x - item.rect.x) < 25 and \
                                abs(self.map.player.rect.y - item.rect.y) < 25:      #pour éviter d'etre trop long on met un \
                                    self.put_in_inventory(item)
                                    item.kill()
                                    break
                        

                        if event.key == pygame.K_e:
                            self.map.player.inventor = not self.map.player.inventor
                    

                    if self.state == 'minigame':
                        if event.key == pygame.K_ESCAPE:
                            self.state = 'exploration'

                        if event.key == pygame.K_LEFT:
                            self.map.minigame.move_case_left()

                        elif event.key == pygame.K_RIGHT:
                            self.map.minigame.move_case_right()
                        
                        elif event.key == pygame.K_UP:
                            self.map.minigame.move_case_up()
                        
                        elif event.key == pygame.K_DOWN:
                            self.map.minigame.move_case_down()
                        

                        if event.key == pygame.K_SPACE:
                            if self.map.minigame.COLOR == (0, 128, 0):
                                self.map.minigame.finished = True
                            else:
                                self.map.minigame.COLOR = (255, 0, 0)
                                self.map.minigame.finished = True


                elif event.type == pygame.KEYUP:                # si la touche n'est pas appuyée
                    self.map.player.pressed[event.key] = False  # elle est assignée à False
                

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.map.player.pressed[event.button] = True  
                    if self.map.player.pressed.get(1):
                        self.map.player.attacking   = True
                        self.map.player.just_attack = True
                        self.map.player.attack()
                        self.map.player.anim_count  = 0
        
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.map.player.pressed[event.button] = False

            # ------------------------------------------------------------------ 
            #  Dépalcement                                              
            # ------------------------------------------------------------------ 


            # -- État exploration --
            if self.state == 'exploration':
                self.update_exploration(cam_x, cam_y)
 
            # -- État mini-jeu --
            elif self.state == 'minigame':
                self._update_minigame()
 
            pygame.display.flip()
            clock.tick(60) # nbr de frames par sec
 
    # ------------------------------------------------------------------ 
    #  Exploration update                                            
    # ------------------------------------------------------------------ 
    def update_exploration(self, cam_x, cam_y):
        player = self.map.player
 
        # Affichage des couches de la carte
        self.screen.blit(self.map.background, (-cam_x, -cam_y))
        self.screen.blit(self.map.path,       (-cam_x, -cam_y))
 
        # Affichage des items
        for item in self.map.items_group:
            self.screen.blit(item.image, (item.rect.x - cam_x, item.rect.y - cam_y))
 
        # Affichage des monstres
        for monster in self.map.all_monsters:
            self.screen.blit(monster.image, (monster.rect.x - cam_x, monster.rect.y - cam_y))
 
        # Affichage du boss
        self.screen.blit(self.map.boss.image, (self.map.boss.rect.x - cam_x, self.map.boss.rect.y - cam_y))
 
        # Affichage du joueur (toujours centré à l'écran)
        self.screen.blit(
            player.image,
            (self.width  // 2 - player.image.get_width()  // 2,
             self.height // 2 - player.image.get_height() // 2)
        )
 
        # Texture des murs (par-dessus pour masquer les entités derrière)
        self.screen.blit(self.map.walls, (-cam_x, -cam_y))
 
        # HUD
        player.health_bar(self.screen, cam_x, cam_y)
 
        # ── Déplacement diagonal du joueur ───────────────────────────────────
        #
        #  On additionne les vecteurs de toutes les touches pressées.
        dx = sum(v[0] for k, v in Depl_key.items() if player.pressed.get(k))
        dy = sum(v[1] for k, v in Depl_key.items() if player.pressed.get(k))
 
        # Clamp à -1/+1 (si deux touches opposées → neutralisation)
        dx = max(-1, min(1, dx))
        dy = max(-1, min(1, dy))
 
        moving = (dx != 0 or dy != 0)
 
        if moving and not player.attacking:
            # Facteur diagonal si les deux axes sont actifs
            Diagonal = 0.707
            factor = Diagonal if (dx != 0 and dy != 0) else 1.0
 
            # ── Déplacement + collision X ──
            old_x    = player.rect.x
            player._fx += dx * factor * player.velocity
            player.rect.x = int(player._fx)
 
            # Garder le joueur dans les limites de la map
            player.rect.left  = max(0, player.rect.left)
            player.rect.right = min(self.map.width, player.rect.right)
 
            self.resolve_wall_x(player, dx)
            self.resolve_monster_x(dx)
            player.sync_float_pos()   # resync flottant après correction de collision
 
            # ── Déplacement + collision Y ──
            old_y    = player.rect.y
            player._fy += dy * factor * player.velocity
            player.rect.y = int(player._fy)
 
            player.rect.top    = max(0, player.rect.top)
            player.rect.bottom = min(self.map.height, player.rect.bottom)
 
            self.resolve_wall_y(player, dy)
            self.resolve_monster_y(dy)
            player.sync_float_pos()
 
            # Met à jour l'animation de course selon le vecteur de déplacement
            player.move(dx * factor, dy * factor)
            # On resync encore car move() a modifié _fx/_fy mais rect a déjà bougé
            player._fx = float(player.rect.x)
            player._fy = float(player.rect.y)
 
            self.map.update_player()
 
        elif not player.attacking:
            # Aucune touche pressée et pas d'attaque → idle dans la dernière direction
            player.idle()
            self.map.update_player()
 
        # ── Animation et fin d'attaque ────────────────────────────────────────
        if player.attacking:
            self.map.update_player()
            player.anim_count += 1
            if player.anim_count >= len(player.images):
                player.attacking  = False
                player.anim_count = 0
 
        # ── Inventaire ────────────────────────────────────────────────────────
        if player.inventor:
            self.inventory(*pygame.mouse.get_pos())

 
        # ── Monstres (IA + collisions + dégâts) ──────────────────────────────
        for monster in list(self.map.all_monsters):
 
            # L'IA du knight prend en charge déplacement + animation
            monster.update_ai(player)
 
            # Résolution des collisions monster↔murs
            self.resolve_monster_walls(monster)
 
            # Mort du knight
            if monster.health <= 0:
                monster.kill()
                continue
 
            # Dégâts du joueur sur le knight
            if player.just_attack and \
               abs(player.rect.centerx - monster.rect.centerx) < 55 and \
               abs(player.rect.centery - monster.rect.centery) < 55:
                monster.damage(10)

            # permet de passer en mini jeu lorsqu'on s'approche du boss
            if not self.minigame_active and (abs(player.rect.centerx - self.map.boss.rect.centerx) < 50 and abs(player.rect.centery - self.map.boss.rect.centery) < 50):
                self.state = 'minigame'
                self.minigame_active = True

        player.just_attack = False
 
 
    # ═════════════════════════════════════════════════════════════════════════
    #  UPDATE MINI-JEU
    # ═════════════════════════════════════════════════════════════════════════
 
    def _update_minigame(self) -> None:
        """Délègue l'affichage et la logique au mini-jeu, gère les contrôles."""
        self.launch_minigame_4(self.screen)
        '''
        if self.map.player.pressed.get(pygame.K_LEFT):
            self.map.minigame.move_left()
        elif self.map.player.pressed.get(pygame.K_RIGHT):
            self.map.minigame.move_right()
        '''