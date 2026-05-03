import pygame
import sys
import math
import random
from sons import bg_son

# ─────────────────────────────────────────────────────────────────────────────
#  Palette ambiance
# ─────────────────────────────────────────────────────────────────────────────
C_BG          = (10,  10,  15)
C_OVERLAY     = (0,   0,   0)
C_BTN_IDLE    = (22,  22,  30)
C_BTN_HOVER   = (38,  38,  52)
C_BTN_SAVES   = (15,  15,  20)
C_BORDER      = (255, 255, 255)
C_BORDER_GREY = (80,  80,  80)
C_TEXT        = (255, 255, 255)
C_TEXT_GREY   = (90,  90,  90)
C_GLOW        = (180, 60,  60)   # rouge Undertale pour le halo du titre
C_PARTICLE    = (60,  60,  80)

BUTTON_W = 220
BUTTON_H = 56
BUTTON_GAP = 18

# ─────────────────────────────────────────────────────────────────────────────
#  Particules — petites âmes qui flottent vers le haut
# ─────────────────────────────────────────────────────────────────────────────
class Particle:
    """Petite particule en arriere plan"""
    def __init__(self, screen_w: int, screen_h: int):
        self.sw = screen_w
        self.sh = screen_h
        self.reset(random.randint(0, screen_h))

    def reset(self, start_y: int = None):
        self.x     = random.uniform(0, self.sw)
        self.y     = self.sh if start_y is None else start_y
        self.speed = random.uniform(0.3, 1.2)
        self.size  = random.randint(1, 3)
        self.alpha = random.randint(60, 180)
        self.drift = random.uniform(-0.3, 0.3)   # balancement gauche/droite

    def update(self):
        self.y -= self.speed
        self.x += self.drift
        if self.y < -10:
            self.reset()   # réapparition en bas

    def draw(self, surface: pygame.Surface):
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*C_PARTICLE, self.alpha), (self.size, self.size), self.size)
        surface.blit(s, (int(self.x), int(self.y)))


# ─────────────────────────────────────────────────────────────────────────────
#  Écran game over
# ─────────────────────────────────────────────────────────────────────────────
class GameOverScreen:
    """
    Affiche l'écran de game over et retourne au titre ou quitte
    """

    def __init__(self, screen: pygame.Surface):
        self.screen  = screen
        self.w, self.h = screen.get_size()

        # Police Pixel Operator (Undertale)
        self.font_title = pygame.font.Font("assets/PixelOperator8-Bold.ttf", 72)
        self.font_btn   = pygame.font.Font("assets/PixelOperator8-Bold.ttf", 26)
        self.font_sub   = pygame.font.Font("assets/PixelOperator8-Bold.ttf", 14)

        # 80 particules
        self.particles = [Particle(self.w, self.h) for _ in range(80)]

        # Positions des boutons — empilés verticalement, centrés, ancrés en bas
        total_h  = 2 * BUTTON_H + BUTTON_GAP
        top_y    = self.h - 110 - total_h
        cx       = self.w // 2 - BUTTON_W // 2

        self.btn_restart  = pygame.Rect(cx, top_y,                               BUTTON_W, BUTTON_H)
        self.btn_quit     = pygame.Rect(cx, top_y + BUTTON_H + BUTTON_GAP,       BUTTON_W, BUTTON_H)

        # Timer pour l'effet de pulsation du titre
        self.tick = 0.0

        # Initialiser le gestionnaire de sons
        self.sons = bg_son()

    def run(self) -> str:
        # Jouer la musique de game over
        self.sons.play_game_over()
        
        clock = pygame.time.Clock()

        while True:
            dt     = clock.tick(60) / 1000.0
            self.tick += dt
            mx, my = pygame.mouse.get_pos()

            # ── Événements ───────────────────────────────────────────────────
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_restart.collidepoint(mx, my):
                        pygame.mixer.music.stop()  # Arrêter immédiatement la musique de game over
                        return 'restart'
                    if self.btn_quit.collidepoint(mx, my):
                        pygame.mixer.music.stop()  # Arrêter la musique
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return 'restart'

            # ── Rendu ────────────────────────────────────────────────────────
            self.screen.fill(C_BG)

            for p in self.particles:
                p.update()
                p.draw(self.screen)

            self.draw_title()
            self.draw_buttons(mx, my)

            pygame.display.flip()

    def draw_title(self):
        pulse = math.sin(self.tick * 1.8) * 3
        text   = 'GAME OVER'
        surf   = self.font_title.render(text, True, C_TEXT)
        tx     = self.w // 2 - surf.get_width() // 2
        ty     = int(self.h * 0.22 + pulse)

        for offset, alpha in [(4, 90), (8, 55), (14, 25)]:
            glow = self.font_title.render(text, True, C_GLOW)
            glow.set_alpha(alpha)
            self.screen.blit(glow, (tx, ty + offset))

        self.screen.blit(surf, (tx, ty))

        # Sous-titre
        sub  = self.font_sub.render('You cannot just give up yet...', True, (100, 100, 100))
        self.screen.blit(sub, (self.w // 2 - sub.get_width() // 2, ty + surf.get_height() + 8))

    def draw_buttons(self, mx: int, my: int):
        self.btn(self.btn_restart, 'RESTART',        mx, my, disabled=False)
        self.btn(self.btn_quit,    'QUITTER',       mx, my, disabled=False)

    def btn(self, rect: pygame.Rect, label: str, mx: int, my: int, disabled: bool):
        hovered = rect.collidepoint(mx, my) and not disabled

        bg     = C_BTN_SAVES if disabled else (C_BTN_HOVER if hovered else C_BTN_IDLE)
        border = C_BORDER_GREY if disabled else C_BORDER
        color  = C_TEXT_GREY   if disabled else C_TEXT

        pygame.draw.rect(self.screen, bg,     rect, border_radius=4)
        pygame.draw.rect(self.screen, border, rect, 3 if hovered else 2, border_radius=4)

        # effet styler quand la souris passe dessus
        if hovered:
            pygame.draw.rect(
                self.screen, C_GLOW,
                (rect.x, rect.y + 10, 3, rect.h - 20),
                border_radius=2
            )

        txt = self.font_btn.render(label, True, color)
        self.screen.blit(txt, (
            rect.x + (rect.w - txt.get_width())  // 2,
            rect.y + (rect.h - txt.get_height()) // 2,
        ))