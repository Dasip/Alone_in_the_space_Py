import pygame


class Button(pygame.sprite.Sprite):
    
    def __init__(self, image, image2, x, y, condition, group):
        super().__init__(group)
        self.image = image
        self.images = [image, image2]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.condition = condition
        
    def turn_on(self, x_pos, y_pos):
        me = self.rect
        if me.left < x_pos < me.right and me.top < y_pos < me.bottom:
            self.image = self.images[1]
        else:
            self.image = self.images[0]
        
    def click(self, x_pos, y_pos):
        me = self.rect
        if me.left < x_pos < me.right and me.top < y_pos < me.bottom:
            return self.condition
        return 'True'