import pygame
from main_func import *


class Dialog(pygame.sprite.Sprite):
    
    def __init__(self, group, text, camera, player, speaker, screen,
                 condition=None):  # obj - объект, который говорит 
        for i in group:
            i.texting('click')
        super().__init__(group)
        self.group = group
        
        self.player = player
        self.player.can_move = False
        self.speaker = speaker
        self.image = load_image('sprites\gui\mess_win.png')
        self.rect = self.image.get_rect()
        self.rect.x = 109 + camera.x
        self.rect.y = 550 + camera.y  
        
        self.cond = condition
        
        self.text = ''.join(text).split('|')
        self.tips = ['Нажмите ЛКМ, чтобы продолжить']
        self.camera = camera
        self.screen = screen  # Поверхность, на которой отображается текст и изображения
        
        self.font_main = pygame.font.Font('data/fonts/segoepr.ttf', 22)
        self.font_tips = pygame.font.Font('data/fonts/segoepr.ttf', 16)        
        self.text_color = (0, 0, 0)
        
    def update(self):
        pygame.font.init()
    
        x_coord = self.rect.x - self.camera.x
        y_coord = self.rect.y - self.camera.y
    
        # ТЕКСТ ЗАДАЧИ
        for i in self.text:
            mess = self.font_main.render(i, 1, self.text_color)
            self.screen.blit(mess, (x_coord + 160,
                                    y_coord + 15 + 40 * self.text.index(i))) 
        # ПОДСКАЗКИ    
        for i in self.tips:
            mess = self.font_tips.render(i, 1, self.text_color)
            self.screen.blit(mess, (x_coord + 420,
                                    y_coord + 240 + 25 * self.tips.index(i)))
            
        if self.player != self.speaker:
            self.screen.blit(self.speaker.image, (x_coord + 35, y_coord + 25))  
        else:
            self.screen.blit(self.speaker.GoDown_anim[0], (x_coord + 35, y_coord + 25)) 
        
    def close(self):
        self.group.remove(self)
        self.player.can_move = True
        if self.cond == 'help':
            self.player.helped = True
            self.player.dialoged = True
        if self.speaker != self.player and self.speaker != None:
            self.speaker.dialog = False    
            
    def texting(self, key):
        if key == 'click':
            self.close()