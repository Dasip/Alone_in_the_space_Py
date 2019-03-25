import pygame
from main_func import *
from Dialog import Dialog


class Valve(pygame.sprite.Sprite):
    
    def __init__(self, image, group, x, y, waste):
        
        super().__init__(group)
        self.Anim = []
        self.cur_frame = 1
        self.spins = 0
        self.spinning_limit = 9
        self.delay = 0
        self.delay_limit = 7
        
        cut_sheet(self, self.Anim, load_image('sprites/entities/Animated/valving.png'), 4, 1)
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.waste = waste
        self.spinned = False
        
    def update_im(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.delay = 0 
        self.spins += 1
        
    def update(self):
        if self.spinned and self.spins < self.spinning_limit:
            if self.delay == self.delay_limit:
                self.update_im(self.Anim[self.cur_frame], self.rect.x, self.rect.y)
                pygame.display.flip()
            self.cur_frame = (self.cur_frame + 1) % len(self.Anim) 
            self.delay += 1
        
    def interact(self, obj, o2, gui, camera, screen):
        
        tar = obj.rect
        me = self.rect
        x, y = self.rect.x, self.rect.y
        
        if abs(tar.top - me.top) < 180 and abs(me.left + 48 - tar.left) < 70: 
            if not self.spinned and not o2.broken:
                ost = pygame.mixer.Channel(2)
                ost.play(pygame.mixer.Sound('data/audio/valve.wav'))                   
                o2.waste -= self.waste
                self.spinned = True
                if o2.waste == 0:
                    Dialog(gui, ['Отлично, теперь нужно запустить аварийный|генератор и улетать отсюда.'],
                           camera, obj, obj, screen)
                    obj.can_move = False