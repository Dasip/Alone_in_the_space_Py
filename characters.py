import pygame, os


class Character(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image, *groups):
        super().__init__(*groups)
        self.coords = [x, y]
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image2 = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    image = pygame.Surface(image2.get_rect().size, pygame.SRCALPHA, 32).convert_alpha()
    image.blit(image2, (0, 0), image.get_rect())
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        pass  # image = image.convert_alpha()
    return image