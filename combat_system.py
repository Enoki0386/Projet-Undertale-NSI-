import pygame

class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 'player_turn' # système tour par tour
        self.finished = False
        self.result = None 

        # actions disponibles
        self.actions = ['Attaquer', 'Défendre', 'Fuir']
        self.selected_action = 0 # index de l'action dans la liste


    def draw_actions(self, screen, screen_width, screen_height):

        font = pygame.font.Font(None, 36)
        
        # boîte principale
        pygame.draw.rect(screen, (0, 0, 0), (50, screen_height - 200, screen_width - 100, 180), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (50, screen_height - 200, screen_width - 100, 180), 2, border_radius=10)

        # actions
        for i in range(len(self.actions)):
            color = (255, 255, 0) if i == self.selected_action else (255, 255, 255)
            text = font.render(self.actions[i], True, color)
            screen.blit(text, (100 + i * 200, screen_height - 150))
        
        # stats ennemi
        enemy_text = font.render(f'{self.enemy.health} / {self.enemy.max_health}', True, (255, 255, 255))
        screen.blit(enemy_text, (screen_width // 2 - 50, 50))
    

    def confirm_action(self):

        if self.actions[self.selected_action] == 'Attaquer':
            self.turn = 'minigame'  # déclenche le mini-jeu barre
            self.result = 'combat'
    
        elif self.actions[self.selected_action] == 'Défendre':
            self.player.protection += 5  # boost temporaire
            self.turn = 'enemy_turn'
            self.result = 'combat'
        
        elif self.actions[self.selected_action] == 'Fuir':
            self.finished = True
            self.result = 'fuite'
    

    def next_turn_enemy(self, screen):

        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2, border_radius=10)

        font = pygame.font.Font(None, 36)
        text = 'Enemy turn !'
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, 500, 300)


    def next_turn_player(self, screen):

        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2, border_radius=10)

        font = pygame.font.Font(None, 36)
        text = 'Player turn !'
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, 500, 300)