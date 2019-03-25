import pygame
from main_func import *
from Dialog import Dialog


class Hacking(pygame.sprite.Sprite):
    
    def __init__(self, group, text, answer, camera, obj, term, screen):
        for i in group:
            i.close()
        super().__init__(group)
        self.group = group
        self.image = load_image('sprites\gui\hack_win.png')
        self.rect = self.image.get_rect()
        self.rect.x = 109 + camera.x
        self.rect.y = 550 + camera.y
        
        self.player = obj  # Игрок
        self.term = term  # Открытый терминал
        
        self.camera = camera
        
        self.text = ''.join(text).split('|')
        self.answer = answer
        self.player_answer = ''
        self.tips = ['Вводите ответ с клавиатуры',
                     'Нажмите Enter для подтверждения ввода',
                     'Нажмите Escape для выключения терминала']
            
        self.screen = screen # Поверхность, на которой отображается текст и изображения
        self.font_main = pygame.font.Font('data/fonts/segoepr.ttf', 22)
        self.font_tips = pygame.font.Font('data/fonts/segoepr.ttf', 16)
        self.text_color = (0, 0, 0)
        
        self.update()
        
    def update(self): # Работает
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
            self.screen.blit(mess, (x_coord + 360,
                                    y_coord + 195 + 25 * self.tips.index(i)))
        # ВВОДИМЫЙ ОТВЕТ    
        self.screen.blit(self.font_main.render(self.player_answer, 1, self.text_color),
                         (x_coord + 360, y_coord + 280))
        
        self.screen.blit(self.term.image, (x_coord + 35, y_coord + 25))
        
    def texting(self, key):
        if key not in ['', 'del', 'enter', 'click', 'esc'] and len(self.player_answer) < 5:
            self.player_answer += key.unicode
        elif key == 'del':
            self.player_answer = self.player_answer[:-1]
        elif key == 'enter':
            if self.player_answer == self.answer:
                self.term.broken = False
                if self.term.name == 'Oxygen':
                    text = ['Терминал заработал, теперь нужно перекрыть',
                            'красные вентили в коридорах, чтобы',
                            'устранить утечку воздуха.']               
                elif self.term.name == 'Energy':
                    text = ['Генератор запущен! В отсеке напротив есть',
                            'шаттл, на нем я и улечу!']
                elif self.term.name == 'Main':
                    text = ['Я разблокировал систему, теперь нужно',
                            'запустить аварийный генератор из реакторной.']
                Dialog(self.group, '|'.join(text), self.camera, self.player,
                           self.player, self.screen)
                self.close()
                
        elif key == 'esc':
            self.close()
        
    def close(self):
        self.player.can_move = True
        self.group.remove(self)
        self.term.dialog = False