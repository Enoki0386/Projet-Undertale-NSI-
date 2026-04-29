# tutoriel.py
import pygame

class Tutoriel:
    def __init__(self, filename):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.dialogues = self._load_dialogue(filename)
        self.dialogue_index = 0
        self.finished = False

        self.nb_lettres = 0.0
        self.vitesse = 1.5
        self.timer = 0      # ← manquait
        self.delai = 180    # ← manquait (3s à 60fps)

        self.font = pygame.font.Font('assets/PixelOperator8-Bold.ttf', 24)
        self.small_font = pygame.font.Font('assets/PixelOperator8-Bold.ttf', 16)

    def _load_dialogue(self, filename):
        with open(f'dialogues/{filename}.txt', 'r') as f:
            lignes = f.readlines()
        return lignes
        
    def update(self):
        if self.finished or self.dialogue_index >= len(self.dialogues):
            return

        texte = self.dialogues[self.dialogue_index].strip()
        self.nb_lettres = min(self.nb_lettres + self.vitesse, len(texte))

        if self.texte_complet():
            self.timer += 1
            if self.timer >= self.delai:
                self.next_dialogue()
                self.timer = 0

    def texte_complet(self):
        if self.dialogue_index >= len(self.dialogues):
            return False
        texte = self.dialogues[self.dialogue_index].strip()
        return int(self.nb_lettres) >= len(texte)

    def next_dialogue(self):
        if not self.texte_complet():
            self.nb_lettres = len(self.dialogues[self.dialogue_index].strip())
            return

        self.timer = 0
        self.dialogue_index += 1
        self.nb_lettres = 0.0
        if self.dialogue_index >= len(self.dialogues):
            self.finished = True

    def draw_dialogue(self, screen, screen_width, screen_height):
        if self.finished or self.dialogue_index >= len(self.dialogues):
            return

        x = 50
        y = 150
        w = screen_width - 100
        h = 120

        pygame.draw.rect(screen, self.BLACK, (x, y, w, h), border_radius=10)
        pygame.draw.rect(screen, self.WHITE, (x, y, w, h), 2, border_radius=10)

        texte_visible = self.dialogues[self.dialogue_index].strip()[:int(self.nb_lettres)]
        screen.blit(self.font.render(texte_visible, True, self.WHITE), (x + 20, y + 40))

        if self.texte_complet():
            invite = self.small_font.render("[ Espace ]", True, (200, 200, 200))
            screen.blit(invite, (x + w - 110, y + h - 25))