import pygame
import sys


class LoreScreen:
    """Affiche une courte séquence d'images avant de démarrer le jeu."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/PixelOperator8-Bold.ttf", 28)
        self.images = self.load_images()

    def load_images(self):
        images = []
        for path in ["lore/marche.png", "lore/migraine.png"]:
            try:
                image = pygame.image.load(path).convert_alpha()
            except pygame.error:
                image = pygame.Surface((self.w, self.h))
                image.fill((0, 0, 0))
            else:
                image = pygame.transform.scale(image, (self.w, self.h))
            images.append(image)
        return images

    def run(self):
        self.show_image(self.images[0], duration=1800)
        self.show_image(self.images[1], wait_key=pygame.K_SPACE)

    def show_image(self, image: pygame.Surface, wait_key=None, duration=None):
        timer = 0

        while True:
            dt = self.clock.tick(60)
            if duration is not None:
                timer += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if wait_key is not None and event.type == pygame.KEYDOWN:
                    if event.key == wait_key:
                        return

            self.screen.blit(image, (0, 0))

            if wait_key is not None:
                prompt = "Appuyez sur ESPACE pour commencer"
                prompt_surf = self.font.render(prompt, True, (255, 255, 255))
                shadow_surf = self.font.render(prompt, True, (0, 0, 0))
                px = self.w // 2 - prompt_surf.get_width() // 2
                py = self.h - prompt_surf.get_height() - 32
                self.screen.blit(shadow_surf, (px + 2, py + 2))
                self.screen.blit(prompt_surf, (px, py))

            pygame.display.flip()

            if duration is not None and timer >= duration:
                return
