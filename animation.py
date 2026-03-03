import pygame

class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, animation):

        super().__init__()
        self.sprite_sheet = pygame.image.load(f'Sprites/RUN/{animation}.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])

        self.current_image = 0
        self.images = animations.get(animation)
    

    def animate(self):

        self.current_image += 1

        if self.current_image >= len(self.images):
            self.current_image = 0
        
        self.image = self.images[self.current_image]
    

    def get_image(self, x, y):
       
        image = pygame.Surface([96, 80])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 96, 80))

        return image


def load_animation_images(animation):

    images = []
    sprite_sheet = pygame.image.load(f'Sprites/RUN/{animation}.png')
    x = 96

    for num in range(7):

        if x < 768:
            image = pygame.Surface([96, 80])
            image.blit(sprite_sheet, (0, 0), (x, 0, 96, 80))
            image.set_colorkey([0, 0, 0])
            images.append(image)
            x += 96
    
    return images


animations = {
    'run_right' : load_animation_images('run_right'),
    'run_left' : load_animation_images('run_left'),
    'run_up' : load_animation_images('run_up'),
    'run_down' : load_animation_images('run_down')
}