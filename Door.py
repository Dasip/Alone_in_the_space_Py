import pygame
from main_func import *


class Door(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y, group, condition):
        super().__init__(group)
        self.condition = condition
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.opened = False
        
    def open_door(self, obj, terms):
        
        o2 = terms['o2']
        energy = terms['energy']
        main = terms['main']
        
        tar = obj.rect
        me = self.rect
        x, y = self.rect.x, self.rect.y
        
        if abs(tar.top - me.top) < 180 and abs(me.left + 48 - tar.left) < 70: 
        
            if not self.opened and eval(self.condition):
                ost = pygame.mixer.Channel(2)
                ost.play(pygame.mixer.Sound('data/audio/door.wav'))                  
                self.opened = True
                self.image = load_image('sprites\entities\opened_door.png')
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
