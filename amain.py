import pygame
import pytmx # bibliothèque servant à ouvrir le fichier .tmx de la map ici
import pyscroll # bibliothèque servant à charger la map sur l'écran
from game import Game # importation de la classe Game du fichier game.py afin d'avoir les ressources
pygame.init() # chargement des modules pygame

# création de la fenêtre
width = 800
height = 800
pygame.display.set_caption('Undertale')
screen = pygame.display.set_mode((width, height))

'''tmx_data est assigné à la map du jeu qui est un fichier .tmx, map_data est assigné à la map du fichier extraite à partir de la
fonction pyscroll.data.TiledMapData() enfin group est assigné à la map adaptée à l'écran. Cette map va être dessinée sur l'écran
dans le 'while'.
'''
tmx_data = pytmx.util_pygame.load_pygame('assets/backgrounds/carte_undertale.tmx')

for image in tmx_data.images:
    if image:
        image.set_colorkey((255, 255, 255))

map_data = pyscroll.data.TiledMapData(tmx_data)
maplayer = pyscroll.orthographic.BufferedRenderer(map_data, screen.get_size())
group = pyscroll.PyscrollGroup(map_layer=maplayer, default_layer=3)

game = Game() # création de l'objet Game
running = True # boucle du jeu sur True

group.add(game.player)


while running:

    group.update()
    group.draw(screen) # dessine la map .tmx 
    game.player.all_projectiles.draw(screen) # dessine le groupe de projectile

    # En fonction des touches cliquées, le joueur se déplace tout en restant dans la zone du jeu, ici les touches peuvent être
    # maintenue afin de ne pas cliquer indéfiniment à chaque pixel
    if game.pressed.get(pygame.K_d) and game.player.rect.x + game.player.rect.width < width:
        game.player.move_right()
    
    elif game.pressed.get(pygame.K_q) and game.player.rect.x > 0:
        game.player.move_left()
    
    elif game.pressed.get(pygame.K_s) and game.player.rect.y + game.player.rect.height < height:
        game.player.move_back()
    
    elif game.pressed.get(pygame.K_z) and game.player.rect.y > 0:
        game.player.move_front()

    pygame.display.flip() # mise à jour de l'interface 

    # fermeture du jeu si le joueur quitte la fenêtre
    for event in pygame.event.get(): #.get() est un tuple de sortie de jeu
        if event.type == pygame.QUIT: # si l'événement est une sortie de jeu
            running = False # la boucle du jeu est arrêtée
            pygame.quit()
            print('Fermeture du jeu')

        # les touches ne peuvent pas être maintenue ici, un clic = un événement fini

        elif event.type == pygame.KEYDOWN: # si une touche est appuyée
            game.pressed[event.key] = True # elle est assignée à True dans le dictionnaire de game.py

            if event.key == pygame.K_SPACE: # si cette touche appuyée est 'ESPACE' le joueur lance un projectile
                game.player.launch_projectile() # méthode dans la classe Player du fichier player.py

        elif event.type == pygame.KEYUP: # si la touche n'est pas appuyée
            game.pressed[event.key] = False # elle est assignée à False

''' 
- Projectile marche pas encore, le code n'a pas d'erreurs pourtant les projectiles n'apparaissent pas lors du clic sur
'ESPACE'

- Les hitbox des murs n'ont pas encore été codé

- Le main n'a pas été touché, j'en ai crée un autre pour que mon code marche et pour pas casser le travail des autres, donc il fadrait
un seul main'''