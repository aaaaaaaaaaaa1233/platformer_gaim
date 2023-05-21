import pygame
import xml.etree.ElementTree as ET
import sys


class SpriteSheet: 
    def __init__(self, sheetfile, datafile = None):
        self.spritesheet = pygame.image.load(sheetfile).convert_alpha()
        if datafile:
            tree = ET.parse(datafile)
            self.map = {}
            for node in tree.iter():
                if node.attrib.get('name'):
                    name = node.attrib.get('name')
                    self.map[name] = {}
                    self.map[name]['x'] = int(node.attrib.get('x'))
                    self.map[name]['y'] = int(node.attrib.get('y'))
                    self.map[name]['width'] = int(node.attrib.get('width'))
                    self.map[name]['height'] = int(node.attrib.get('height'))

    def get_image_name(self, name):
        rect = pygame.Rect(self.map[name]['x'], self.map[name]['y'], self.map[name]['width'], self.map[name]['height'])
        image = self.spritesheet.subsurface(rect)
        return pygame.transform.scale(image, (35,35))
    def get_image_rect(self, x, y, width, height):
        image = self.spritesheet.subsurface(pygame.Rect(x, y, width, height))
        return pygame.transform.scale(image, (35,35))                          


if __name__ == "__main__":
    print(sys.argv)
    sheet_file = "platformer_gaim/tiles_spritesheet.png"
    datafile = "platformer_gaim/tiles_spritesheet.xml"
    pygame.init()
    display_surface = pygame.display.set_mode((1, 1))
    sheet = SpriteSheet(sheet_file, datafile)
    sheetw = sheet.spritesheet.get_rect().width
    sheeth = sheet.spritesheet.get_rect().height
    display_surface = pygame.display.set_mode((sheetw, sheeth))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        display_surface.fill("black")
        display_surface.blit(sheet.spritesheet, sheet.spritesheet.get_rect())

        mouse_pos = pygame.mouse.get_pos()
        mousex = mouse_pos[0]
        mousey = mouse_pos[1]


        for k,v in sheet.map.items():
            if (mousex > sheet.map[k]["x"] and mousex < sheet.map[k]["x"] + sheet.map[k]["width"] 
            and mousey > sheet.map[k]["y"] and mousey < sheet.map[k]["y"] + sheet.map[k]["height"]):
                image_name = k
                image_width = sheet.map[k]["width"]
                image_height = sheet.map[k]["height"]
                break
            image_name = ""
            image_width = ""
            image_height = ""

        pygame.display.set_caption(f"x = {mousex}   y = {mousey} name = {image_name} height = {image_height} width = {image_width}")



        pygame.display.update()
