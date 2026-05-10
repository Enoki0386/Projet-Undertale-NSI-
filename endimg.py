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
C_GLOW        = (180, 60,  60)
C_PARTICLE    = (60,  60,  80)

BUTTON_W = 220
BUTTON_H = 56
BUTTON_GAP = 18


class Particle:
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
        self.drift = random.uniform(-0.3, 0.3)

    def update(self):
        self.y -= self.speed
        self.x += self.drift
        if self.y < -10:
            self.reset()

    def draw(self, surface: pygame.Surface):
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*C_PARTICLE, self.alpha), (self.size, self.size), self.size)
        surface.blit(s, (int(self.x), int(self.y)))


class FinalEndingScreen:
    def __init__(self, screen: pygame.Surface):
        self.screen   = screen
        self.w, self.h = screen.get_size()

        self.font_title = pygame.font.Font("assets/PixelOperator8-Bold.ttf", 72)
        self.font_sub   = pygame.font.Font("assets/PixelOperator8-Bold.ttf", 22)
        self.font_btn   = pygame.font.Font("assets/PixelOperator8-Bold.ttf", 26)

        self.particles = [Particle(self.w, self.h) for _ in range(80)]

        total_h  = 2 * BUTTON_H + BUTTON_GAP
        top_y    = self.h - 110 - total_h
        cx       = self.w // 2 - BUTTON_W // 2

        self.btn_restart = pygame.Rect(cx, top_y, BUTTON_W, BUTTON_H)
        self.btn_quit    = pygame.Rect(cx, top_y + BUTTON_H + BUTTON_GAP, BUTTON_W, BUTTON_H)

        self.images = {
            'good': pygame.image.load('endingimg/NSI_undertale_good.png').convert_alpha(),
            'bad': pygame.image.load('endingimg/NSI_undertale_bad.png').convert_alpha(),
        }

        self.tick = 0.0
        self.sons = bg_son()

    def run(self, result: str) -> str:
        image = self.images.get(result)
        if image is None:
            raise ValueError(f"Unknown ending result: {result}")

        self.sons.play_game_over()

        clock = pygame.time.Clock()
        while True:
            pygame.mouse.set_visible(True)
            dt = clock.tick(60) / 1000.0
            self.tick += dt
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_restart.collidepoint(mx, my):
                        pygame.mixer.music.stop()
                        return 'restart'
                    if self.btn_quit.collidepoint(mx, my):
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    pygame.mixer.music.stop()
                    return 'restart'

            self.screen.fill(C_BG)
            for p in self.particles:
                p.update()
                p.draw(self.screen)

            title = 'BONNE FIN' if result == 'good' else 'MAUVAISE FIN'
            subtitle = (
                'Vous avez fui tous les boss jusqu\'au bout.'
                if result == 'good'
                else 'Vous avez tué tous les boss.'
            )

            self.draw_title(title)
            self.draw_subtitle(subtitle)
            self.draw_image(image)
            self.draw_buttons(mx, my)

            pygame.display.flip()

    def draw_title(self, text: str):
        pulse = math.sin(self.tick * 1.8) * 3
        surf = self.font_title.render(text, True, C_TEXT)
        tx = self.w // 2 - surf.get_width() // 2
        ty = int(self.h * 0.16 + pulse)

        for offset, alpha in [(4, 90), (8, 55), (14, 25)]:
            glow = self.font_title.render(text, True, C_GLOW)
            glow.set_alpha(alpha)
            self.screen.blit(glow, (tx, ty + offset))

        self.screen.blit(surf, (tx, ty))

    def draw_subtitle(self, text: str):
        surf = self.font_sub.render(text, True, C_TEXT_GREY)
        self.screen.blit(surf, (self.w // 2 - surf.get_width() // 2, self.h * 0.28))

    def draw_image(self, image: pygame.Surface):
        max_w = self.w - 160
        max_h = self.h * 0.35
        iw, ih = image.get_size()
        scale = min(max_w / iw, max_h / ih, 1.0)
        if scale < 1.0:
            image = pygame.transform.smoothscale(image, (int(iw * scale), int(ih * scale)))

        x = self.w // 2 - image.get_width() // 2
        y = int(self.h * 0.35)
        self.screen.blit(image, (x, y))

    def draw_buttons(self, mx: int, my: int):
        self.btn(self.btn_restart, 'RESTART', mx, my)
        self.btn(self.btn_quit, 'QUITTER', mx, my)

    def btn(self, rect: pygame.Rect, label: str, mx: int, my: int):
        hovered = rect.collidepoint(mx, my)
        bg = C_BTN_HOVER if hovered else C_BTN_IDLE
        border = C_BORDER
        color = C_TEXT

        pygame.draw.rect(self.screen, bg, rect, border_radius=4)
        pygame.draw.rect(self.screen, border, rect, 3 if hovered else 2, border_radius=4)

        if hovered:
            pygame.draw.rect(self.screen, C_GLOW, (rect.x, rect.y + 10, 3, rect.h - 20), border_radius=2)

        txt = self.font_btn.render(label, True, color)
        self.screen.blit(txt, (rect.x + (rect.w - txt.get_width()) // 2, rect.y + (rect.h - txt.get_height()) // 2))
