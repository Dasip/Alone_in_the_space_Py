import pygame
from Dialog import Dialog
from Hacking import Hacking
from main_func import *


class Terminal(pygame.sprite.Sprite):
    
    def __init__(self, image, name, x, y, group, text, answer, improved, broken=True):
        
        super().__init__(group)
        self.image = image
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.broken = broken
        self.text = [text]
        self.improved_text = [improved]
        self.answer = answer
        
        self.Anim = []
        self.cur_frame = 0
        self.delay = 0
        self.delay_limit = 9
        
        self.x, self.y = x, y
        
        self.dialog = False
        
    def interact(self, obj, gui, camera, surface):
        
        tar = obj.rect
        me = self.rect
        x, y = self.rect.x, self.rect.y
        
        if obj.can_move:
            if abs(tar.top - me.top) < 120 and abs(me.left + 48 - tar.left) < 50 and self.dialog != True: 
                ost = pygame.mixer.Channel(2)
                ost.play(pygame.mixer.Sound('data/audio/terminal.wav'))                  
                if self.broken:
                    Hacking(gui, self.text, self.answer, camera, obj, self, surface)
                else:
                    if self.name != 'Oxygen':
                        improved = self.improved_text
                    else:
                        improved = ['{} {}%'.format(self.improved_text[0], self.waste)]
                    Dialog(gui, improved, camera, obj, self, surface)
                self.dialog = True  # открытие диалога - больше одного диалога открыть нельзя
                obj.can_move = False  # Обездвиживание персонажа
                 
    def update(self):
        if self.Anim != []:
            if self.broken:
                if self.delay == self.delay_limit:
                    self.update_im(self.Anim[self.cur_frame])
                self.cur_frame = (self.cur_frame + 1) % len(self.Anim) 
                self.delay += 1
            else:
                self.update_im(self.Anim[0])
                
    def update_im(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.delay = 0 
            
            
class O2Term(Terminal):
    
    def __init__(self, image, name, x, y, group, text, answer, improved, broken=True):
        super().__init__(image, name, x, y, group, text, answer, improved, broken)
        self.waste = 50
        cut_sheet(self, self.Anim, load_image('sprites\entities\Animated\Oxygen.png'), 5, 1)
        self.image = image
        self.rect.x, self.rect.y = x, y
        
        
class EnergyTerm(Terminal):
    
    def __init__(self, image, name, x, y, group, text, answer, improved, task, broken=True):
        super().__init__(image, name, x, y, group, text, answer, improved, broken)
        self.task = task
        cut_sheet(self, self.Anim, load_image('sprites\entities\Animated\Energy.png'), 5, 1)
        
    def unblock(self):
        self.answer = '13'
        self.text = self.task
        
        
class MainTerm(Terminal):
    
    def __init__(self, image, name, x, y, group, text, answer, improved, broken=True):
        super().__init__(image, name, x, y, group, text, answer, improved, broken)