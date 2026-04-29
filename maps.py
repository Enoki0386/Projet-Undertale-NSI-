import pygame
import csv
from random import randint, choice
 
from player01 import Player01
from knight   import Knight
from item     import Item
from minigame import Minigame
from boss     import Boss
from boss     import Samurai
from boss     import Ghost
from npc      import NPC
 
# ------------------------------------------------------------------
# Répertoire des textures et autres
# ------------------------------------------------------------------
Map_settings = {
    1: {
        'background' : 'carte1/carte_undertale_background.png',
        'path'       : 'carte1/carte_undertale_path.png',
        'walls_img'  : 'carte1/carte_undertale_walls.png',
        'walls_csv'  : 'carte1/carte_undertale._walls.csv',
        'spawn_zone' : (800, 1400, 200, 1200),   # x_min, x_max, y_min, y_max
    },
    2: {
        'background' : 'carte2/carte_undertale_2_background.png',
        'path'       : 'carte2/carte_undertale_2_path.png',
        'walls_img'  : 'carte2/carte_undertale_2_walls.png',
        'walls_csv'  : 'carte2/carte_undertale_2_walls.csv',
        'spawn_zone' : (600, 1500, 200, 1400),
    },
    3: {
        'background' : 'carte3/carte_undertale_3_background.png',
        'path'       : 'carte3/carte_undertale_3_path.png',
        'walls_img'  : 'carte3/carte_undertale_3_walls.png',      # image vide (on est dehors)
        'walls_csv'  : 'carte3/carte_undertale_3_walls.csv',
        'spawn_zone' : (0, 1600, 0, 1600)
    }
}
 
Items_choice     = ['shield', 'heart', 'knife']
Dialogues_choice = ['npc_1', 'npc_2', 'npc_3', 'npc_4', 'npc_5', 'npc_6', 'npc_7', 'npc_8', 'npc_9']
Sprites_choice   = ['npc1_front', 'npc2_front', 'npc3_front']
Npcs_pos         = [(350, 640), (230, 1410), (1353, 1136), (258, 653), (1396, 303), (853, 1171), (1200, 300), (300, 800), (1000, 1000)] # trois premiers tuple = map 1, trois milieu tuple = map 2, trois dernier tuple = map 3
Boss_pos         = [(1060, 1410), (607, 873), (900, 1200)] # tuple 1 = map 1, tuple 2 = map 2, tuple 3 = map 3
Monstre_nbr      = 5
Items_nbr        = len(Items_choice)
Npcs_nbr         = 3
Boss_nbr         = 1
WALL_Y_OFFSET    = 8
# ------------------------------------------------------------------
# Création des murs
# ------------------------------------------------------------------
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image  = pygame.Surface((size, size))
        self.image.fill((0, 0, 0))
        self.rect   = pygame.Rect(x, y, size, size)
        self.mask   = pygame.mask.from_surface(self.image)
# ------------------------------------------------------------------
# Creation de la map
# ------------------------------------------------------------------
class Map:
    def __init__(self):
        self.width          = 1600
        self.height         = 1600
        self.tile_size      = 16

        self.player         = Player01()
        self.minigame       = Minigame()
        self.boss = None
        self.all_monsters   = pygame.sprite.Group()
        self.wall_group     = pygame.sprite.Group()
        self.items_group    = pygame.sprite.Group()
        self.npc_grp        = pygame.sprite.Group()
        
        # Surfaces chargées lors de load_maps()
        self.background: pygame.Surface | None = None
        self.path:       pygame.Surface | None = None
        self.walls:      pygame.Surface | None = None


    # ------------------------------------------------------------------
    # Chargement map et murs
    # ------------------------------------------------------------------
    def load_maps(self, map, x, y):
        '''Charge une carte : images, CSV des murs, monstres et objets.'''
        self.all_monsters.empty()
        self.items_group.empty()
        self.npc_grp.empty()

        if self.boss is not None:
            self.boss.kill()
        
        Map_set = Map_settings[map]
        self.background = pygame.image.load(Map_set['background'])
        self.path       = pygame.image.load(Map_set['path'])
        self.walls      = pygame.image.load(Map_set['walls_img'])
 
        self.load_wall_group(Map_set['walls_csv'])
        self.spawn_monsters(Map_set['spawn_zone'])
        self.spawn_npcs(map)
        self.spawn_items(Map_set['spawn_zone'])
        self.spawn_boss(map)
 
        self.player.rect.x = x
        self.player.rect.y = y
        self.player.sync_float_pos()   # resync la position flottante
        
    
    def load_wall_group(self, filename):
        '''Lit le CSV et crée les sprites de collision pour chaque tuile non vide.'''
        self.wall_group.empty()

        with open(filename) as f:
            for row_index, row in enumerate(csv.reader(f)):
                for col_index, tile in enumerate(row):
                    if int(tile.strip()) != -1:
                        x = col_index * self.tile_size
                        y = row_index * self.tile_size
                        self.wall_group.add(Wall(x, y, self.tile_size))

    # ------------------------------------------------------------------
    # Spawn montre et items 
    # ------------------------------------------------------------------
    def spawn_monsters(self, zone):
        '''Fait apparaître Monster_nbr chevaliers dans la zone définie.'''
        x_min, x_max, y_min, y_max = zone
        res = 0
        while res < Monstre_nbr:
            x = randint(x_min, x_max)
            y = randint(y_min, y_max)
            k = Knight(x, y)
            # Transmet les limites de la map au knight pour le clamping
            k.map_width  = self.width
            k.map_height = self.height
            self.all_monsters.add(k)
            res += 1
    

    def spawn_items(self, zone):
        '''Fait apparaître Item_nbr objets aléatoires dans la zone définie.'''
        x_min, x_max, y_min, y_max = zone
        res = 0
        while res < Items_nbr:
            x    = randint(x_min, x_max)
            y    = randint(y_min, y_max)
            name = choice(Items_choice)
            self.items_group.add(Item(name, x, y))
            res += 1
    

    def spawn_npcs(self, map):
        '''Fait apparître des personnages non jouable dans la zone entrée'''
        # c'est ici où j'attribue les différents dialogues des npcs, j'en donne des différents mais la gestion peut être améliorée
        res = 0
        while res < Npcs_nbr:
            if map == 1:
                x = Npcs_pos[res][0]
                y = Npcs_pos[res][1]
                filename = Dialogues_choice[res]
            elif map == 2:
                x = Npcs_pos[res + 3][0]
                y = Npcs_pos[res + 3][0]
                filename = Dialogues_choice[res + 3]
            elif map == 3:
                x = Npcs_pos[res + 6][0]
                y = Npcs_pos[res + 6][0]
                filename = Dialogues_choice[res + 6]
                
            sprite = Sprites_choice[res]
            n = NPC(x, y, filename, sprite)
            # Transmet les limites de la map au npc pour le clamping
            n.map_width = self.width
            n.map_height = self.height
            self.npc_grp.add(n)
            res += 1


    def spawn_boss(self, map):
        
        res = 0
        while res < Boss_nbr:
            if map == 1:
                x = Boss_pos[res][0]
                y = Boss_pos[res][1]
                self.boss = Boss(x, y)
                self.boss_index = 0

            elif map == 2:
                x = Boss_pos[res + 1][0]
                y = Boss_pos[res + 1][1]
                self.boss = Samurai(x, y)
                self.boss_index = 1
            
            elif map == 3:
                x = Boss_pos[res + 2][0]
                y = Boss_pos[res + 2][1]
                self.boss = Ghost(x, y)
                self.boss_index = 2

            self.boss.map_width  = self.width
            self.boss.map_height = self.height
            res += 1


    # ------------------------------------------------------------------
    # Update des joueurs + monstres 
    # ------------------------------------------------------------------
    def update_player(self):
        self.player.update_animation_player()
    
    def update_monsters(self):
        for monster in self.all_monsters:
            monster.update_animation_knight()
    
    def update_npcs(self):
        for npc in self.npc_grp:
            npc.update_animation_npc()
    
    def update_boss(self):
        self.boss.update_animation_boss()