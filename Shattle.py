import pygame


class Shattle(pygame.sprite.Sprite):
    
    def __init__(self, image, group, x, y):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        
    def interact(self, obj):
        tar = obj.rect
        me = self.rect
        if abs(tar.top - me.top) < 200 and abs(me.left + 48 - tar.left) < 180: 
            return 'away'
        return 'True'