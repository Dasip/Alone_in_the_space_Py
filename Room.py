import pygame


class Room(pygame.sprite.Sprite):
    
    def __init__(self, loop):
        pygame.mixer.init()
        self.loop = loop