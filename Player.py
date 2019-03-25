import pygame
from main_func import *
from Dialog import Dialog


class Player(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y, surface, speed, group):
        
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        
        self.can_move = False
        
        self.helped = False
        self.dialoged = False
        
        self.GoUp_anim = []
        self.GoDown_anim = []
        self.GoRight_anim = []
        self.GoLeft_anim = []
        
        self.cur_frame = 0
        self.delay = 0
        self.delay_limit = 7
        
        cut_sheet(self, self.GoUp_anim, load_image('sprites\player\go_up.png'), 4, 1)
        cut_sheet(self, self.GoLeft_anim, load_image('sprites\player\go_left.png'), 4, 1)
        cut_sheet(self, self.GoDown_anim, load_image('sprites\player\go_down.png'), 4, 1)
        cut_sheet(self, self.GoRight_anim, load_image('sprites\player\go_right.png'), 4, 1)
        self.last_move = ''        
        
        self.rect.width = 80  # ширина спрайита
        self.rect.height = 40  # высота спрайта
        self.rect.x = x  # начальная икс-координата
        self.rect.y = y  # начальная игрек-координата
        self.speed = speed  # скорость передвижения игрка
  
        
    def move(self, vx, vy, groups, camera, surface):
         
        if self.can_move:
            self.rect.x += vx * self.speed
            self.rect.y += vy * self.speed
            
            # ДВИЖЕНИЕ ВЛЕВО
            if vy == 0:
                if vx == -1:
                    if self.last_move != '-x':
                        self.cur_frame = 0
                        self.last_move = '-x'
                    else:
                        self.cur_frame = (self.cur_frame + 1) % len(self.GoLeft_anim)
                        
                    if self.delay == self.delay_limit:
                        self.update_im(self.GoLeft_anim[self.cur_frame], self.rect.x, self.rect.y)   
                        
                elif vx == 1:
                    if self.last_move != 'x':
                        self.cur_frame = 0
                        self.last_move = 'x'
                    else:
                        self.cur_frame = (self.cur_frame + 1) % len(self.GoRight_anim)
                        
                    if self.delay == self.delay_limit:
                        self.update_im(self.GoRight_anim[self.cur_frame], self.rect.x, self.rect.y)                
            
            # ДВИЖЕНИЕ ВВЕРХ
            if vy == -1:
                if self.last_move != '-y':
                    self.cur_frame = 0
                    self.last_move = '-y'
                else:
                    self.cur_frame = (self.cur_frame + 1) % len(self.GoUp_anim)
                    
                if self.delay == self.delay_limit:
                    self.update_im(self.GoUp_anim[self.cur_frame], self.rect.x, self.rect.y)
                    
            #  ДВИЖЕНИЕ ВНИЗ
            
            elif vy == 1:
                if self.last_move != 'y':
                    self.cur_frame = 0
                    self.last_move = 'y'
                else:
                    self.cur_frame = (self.cur_frame + 1) % len(self.GoDown_anim)
                    
                if self.delay == self.delay_limit:
                    self.update_im(self.GoDown_anim[self.cur_frame], self.rect.x, self.rect.y)
            
            if vx != 0 or vy != 0:
                self.delay += 1
            
            # ПРОВЕРКА СТОЛКНОВЕНИЙ
            for i in groups.values():
                if pygame.sprite.spritecollideany(self, i) and i != groups['player']:
                    self.rect.x += -self.speed * vx
                    self.rect.y += -self.speed * vy
                    
        else:
            if not self.helped and not self.dialoged:
                text = ['Для передвижения используйте клавиши', 'WASD. Для взаимодействи с объктами',
                        'подойдите к ним и нажмите ЛКМ.', 'Внимательно читайте диалоги и подсказки.',
                        'Для начала разблокируйте кислородный', 'терминал в кислородном отсеке.']
                Dialog(groups['gui'], '|'.join(text), camera, self, self, surface,
                       'help')
                
    def update_im(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.delay = 0 