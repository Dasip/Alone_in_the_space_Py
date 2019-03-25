import pygame


class Back(pygame.sprite.Sprite):
    
    def __init__(self, image, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0