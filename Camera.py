import pygame


class Camera():
    
    def __init__(self, x, y, speed, field, screen_size):
        self.x = x  # Икс координата камеры 
        self.y = y
        self.map_width = field.width * field.tilewidth
        self.map_height = field.height * field.tileheight
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        
    def update(self, target, size):
        
        x = (target.rect.x + target.rect.w // 2 - size[0] // 2)
        y = (target.rect.y + target.rect.h // 2 - size[1] // 2)
        if 0 < x < self.map_width - self.screen_width:
            self.x = x
        else:
            self.x = 0 if x <= 0 else self.map_width - self.screen_width
            
        if 0 < y < self.map_height - self.screen_height:
            self.y = y
        else:
            self.y = 0 if y <= 0 else self.map_height - self.screen_height