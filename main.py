''' ЗАМЕТКИ
УСТАНОВИ МОДУЛЬ PYTMX!
INSTALL PYTMX LIB!
'''
import pygame, os, sys
import pytmx
from Back import Back
from Room import Room
from Button import Button
from Shattle import Shattle
from Valve import Valve
from main_func import *
from Dialog import Dialog
from Terms import *
from Door import Door
from Player import Player
from Camera import Camera
from Wall import Wall


class Renderer():
    
    def __init__(self, tile_map):
        self.gameMap = pytmx.load_pygame(tile_map)
        
        self.pixel_size = (self.gameMap.width * self.gameMap.tilewidth,
                           self.gameMap.height * self.gameMap.tileheight)
        
    # СОЗДАНИЕ ГЕРОЯ
    def create_hero(self, surface, hero_group, speed):
        for layer in self.gameMap.layers:
            if layer.name == 'player':
                p = layer[0]
                person = Player(p.image, p.x, p.y, surface, speed, hero_group)
                return person
        
    def generate_map(self, surface, camera, group):
        
        for layer in self.gameMap.layers:
            
            if isinstance(layer, pytmx.TiledTileLayer):
                self.render_tiles(surface, layer, camera)
        
            elif isinstance(layer, pytmx.TiledObjectGroup):
                self.generate_objects(surface, layer, camera, group)
        
    def render_map(self, surface, camera, group):
        
        surface.fill((255, 255, 255))
        for layer in self.gameMap.layers:
            
            if isinstance(layer, pytmx.TiledTileLayer):
                self.render_tiles(surface, layer, camera)
                
        order = [group['walls'], group['other'], group['valves'], group['terms'],
                 group['player'], group['doors'], group['shattle']]
        
        for each_group in order:
            for i in each_group:
                surface.blit(i.image, (i.rect.x - camera.x, i.rect.y - camera.y))
        
        group['terms'].update()
        group['valves'].update()
        # АПДЕЙТИНГ GUI
        for i in group['gui']:
            surface.blit(i.image, (i.rect.x - camera.x, i.rect.y - camera.y))
            
        group['gui'].update()
                
    def render_tiles(self, surface, layer, camera):
        
        tile_w = self.gameMap.tilewidth
        tile_h = self.gameMap.tileheight
        blit = surface.blit

        # iterate over the tiles in the layer, and blit them
        for x, y, image in layer.tiles():
            blit(image, (x * tile_w - camera.x, y * tile_h - camera.y)) 
    
    # ||||||||| ||||||||| ||||||||| ||||||||| ||||||||| #
    # ГЕНЕРАЦИЯ ОБЪЕКТОВ #        
    def generate_objects(self, surface, layer, camera, group):
        
        terms = {'Oxygen': O2Term, 'Energy': EnergyTerm, 'Main': MainTerm}
        
        for obj in layer:
            if layer.name == 'walls':
                Wall(obj.image, obj.x, obj.y, group['walls'])
                
            elif layer.name == 'doors':
                Door(obj.image, obj.x, obj.y, group['doors'], obj.properties['condition']) 
                
            elif layer.name == 'player':
                pass
            
            elif layer.name == 'terminals' and obj.name != None:
                if obj.name == 'Energy':
                    terms[obj.name](obj.image, obj.name, obj.x, obj.y, group['terms'], obj.properties['text'],
                                    obj.properties['answer'], obj.properties['improved_text'],
                                    obj.properties['task'], obj.properties['broken'])
                else:
                    terms[obj.name](obj.image, obj.name, obj.x, obj.y, group['terms'], obj.properties['text'],
                                    obj.properties['answer'], obj.properties['improved_text'],
                                    obj.properties['broken'])                    
                
            elif layer.name == 'volvo':
                Valve(obj.image, group['valves'], obj.x, obj.y, obj.properties['waste'])
                
            elif layer.name == 'shattle':
                Shattle(obj.image, group['shattle'], obj.x, obj.y)
            
            else:
                Wall(obj.image, obj.x, obj.y, group['other'])
    # ||||||||| ||||||||| ||||||||| ||||||||| ||||||||| #

def menu(clock, Screen, display_width, display_height, dis_size):
    
    fon = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    back = Back(load_image('sprites/main_fon.png'), fon)
    start_button = Button(load_image('sprites/gui/new_game.png'),
                          load_image('sprites/gui/new_game2.png'), 350, 300,
                          'start', all_sprites)
    exit_button = Button(load_image('sprites/gui/exit.png'),
                         load_image('sprites/gui/exit2.png'), 350, 600, 'exit',
                         all_sprites)
    
    ost = pygame.mixer.Channel(1)
    ost.play(pygame.mixer.Sound('data/audio/main_menu.wav'), 1000)    
    
    menuExit = False
    while not menuExit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()            
            if event.type == pygame.MOUSEMOTION:
                start_button.turn_on(event.pos[0], event.pos[1])
                exit_button.turn_on(event.pos[0], event.pos[1])
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    a = start_button.click(event.pos[0], event.pos[1])
                    b = exit_button.click(event.pos[0], event.pos[1])
                    if a == 'start':
                        menuExit = True
                    if b == 'exit':
                        terminate()
        for i in fon:
            Screen.blit(i.image, (i.rect.x, i.rect.y))
        for i in all_sprites:
            Screen.blit(i.image, (i.rect.x, i.rect.y))
        pygame.display.flip()
        clock.tick(60)
    


def action(clock, Screen, display_width, display_height, dis_size):
    
    walls = pygame.sprite.Group()
    other = pygame.sprite.Group()
    player = pygame.sprite.Group()
    doors = pygame.sprite.Group()
    terminals = pygame.sprite.Group()
    valves = pygame.sprite.Group()
    gui = pygame.sprite.Group()
    shattle = pygame.sprite.Group()
    
    ost = pygame.mixer.Channel(1)
    ost.play(pygame.mixer.Sound('data/audio/ost.wav'), 1000)
    
    groups = {'walls': walls, 'other': other, 'player': player, 'doors': doors,
              'valves': valves, 'gui': gui, 'terms': terminals, 'shattle': shattle}
    
    render = Renderer('data/maps/level_1_final.tmx')
    person = render.create_hero(Screen, player, 4)
    camera = Camera(person.rect.x, person.rect.y, 6, render.gameMap,
                    (display_width, display_height))
    render.generate_map(Screen, camera, groups)
    

    terms_objects = {'o2': list(filter(lambda x: x.name == 'Oxygen', terminals))[0],
             'energy': list(filter(lambda x: x.name == 'Energy', terminals))[0],
             'main': list(filter(lambda x: x.name == 'Main', terminals))[0]}
    
    player_vx, player_vy = 0, 0
    gameExit = False
    while not gameExit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                
            if event.type == pygame.KEYDOWN:
                if not person.can_move:
                    ev = event
                    if event.key == pygame.K_BACKSPACE:
                        ev = 'del'
                    elif event.key == 13:
                        ev = 'enter'
                    for i in gui:
                        i.texting(ev)
                        
                if event.key == pygame.K_s:
                    player_vy = 1
                elif event.key == pygame.K_w:
                    player_vy = -1
                if event.key == pygame.K_a:
                    player_vx = -1
                elif event.key == pygame.K_d:
                    player_vx = 1
                if event.key == pygame.K_ESCAPE:
                    counter = 0
                    for i in gui:
                        counter += 1
                        i.texting('esc')
                    if counter == 0:
                        gameExit = True
                    
            if event.type == pygame.KEYUP:
                
                if not person.can_move:
                    for i in gui:
                        i.texting('')
                        
                if event.key in [pygame.K_s, pygame.K_w]:
                    player_vy = 0
                    
                if event.key in [pygame.K_d, pygame.K_a]:
                    player_vx = 0
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if person.can_move:
                        for i in doors:
                            i.open_door(person, terms_objects)
                        for i in terminals:
                            i.interact(person, gui, camera, Screen)
                        for i in valves:
                            i.interact(person, terms_objects['o2'], gui, camera, Screen)
                        for i in shattle:
                            a = i.interact(person)
                            if a == 'away':
                                gameExit = True
                    else:
                        for i in gui:
                            i.texting('click')
        
        if not terms_objects['main'].broken:
            terms_objects['energy'].unblock()
        person.move(player_vx, player_vy, groups, camera, Screen)
        camera.update(person, dis_size)
        
        Screen.fill((255, 0, 0))
        render.render_map(Screen, camera, groups)   
        pygame.display.flip()
        clock.tick(60) 
        
        
def flight(clock, Screen, display_width, display_height, dis_size):
    
    ost = pygame.mixer.Channel(1)
    ost.stop()
    fon = pygame.sprite.Group()
    back = Back(load_image('sprites/fon.png'), fon)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                
        fon.draw(Screen)
        pygame.display.flip()

def game_loop():
    
    pygame.init()
    
    dis_size = display_width, display_height = 1000, 900
    
    Screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('2d Game')
    clock = pygame.time.Clock()
    
    Room1 = Room(menu)
    Room2 = Room(action)
    Room3 = Room(flight)
    
    Room1.loop(clock, Screen, display_width, display_height, dis_size)
    Room2.loop(clock, Screen, display_width, display_height, dis_size)
    Room3.loop(clock, Screen, display_width, display_height, dis_size)
    
    terminate()
    
        

game_loop()
pygame.quit()