import sys, os, pygame


def terminate():
    pygame.quit()
    sys.exit()
    
    
def cut_sheet(obj, frames, sheet, columns, rows):
    obj.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                            sheet.get_height() // rows)
    for j in range(rows):
        for i in range(columns):
            frame_location = (obj.rect.w * i, obj.rect.h * j)
            frames.append(sheet.subsurface(pygame.Rect(
                frame_location, obj.rect.size)))  
    
                
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)

    try:
        image2 = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    image = pygame.Surface(image2.get_rect().size, pygame.SRCALPHA, 32).convert_alpha()
    image.blit(image2, (0, 0), image.get_rect())
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image