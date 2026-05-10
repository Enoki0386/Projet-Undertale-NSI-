import pygame
import sys


class EndImageScreen:
    """Affiche l'écran de fin Good/Bad et ferme le jeu après 5 secondes."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.images = {
            'good': pygame.image.load('endingimg/NSI_undertale_good.png').convert_alpha(),
            'bad': pygame.image.load('endingimg/NSI_undertale_bad.png').convert_alpha(),
        }

    def run(self, result: str):
        image = self.images.get(result)
        if image is None:
            raise ValueError(f"Ending image inconnue : {result}")

        start_ticks = pygame.time.get_ticks()
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0, 0, 0))
            image_x = self.width // 2 - image.get_width() // 2
            image_y = self.height // 2 - image.get_height() // 2
            self.screen.blit(image, (image_x, image_y))
            pygame.display.flip()

            elapsed = pygame.time.get_ticks() - start_ticks
            if elapsed >= 5000:
                pygame.quit()
                sys.exit()

            clock.tick(60)
