import pygame


class Wall(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.def_x = x
        self.def_y = y
        self.rect.x = x
        self.rect.y = y
        
    def update(self, vx, vy):
        self.rect.x = vx
        self.rect.y = vy