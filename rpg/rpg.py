import pygame
from pytmx.util_pygame import load_pygame


pygame.init()

TILE_SIZE = 48
BORDER_COLOR = (255, 0, 0)
WINDOW_W = TILE_SIZE * 20
WINDOW_H = TILE_SIZE * 12
CENTER_X = WINDOW_W // 2
CENTER_Y = WINDOW_H // 2
SKY_BLUE = (177, 229, 233)
PLAYER_SPEED = TILE_SIZE / 6

display_surface = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("RPG")

FPS = 60
clock = pygame.time.Clock()







class Tile(pygame.sprite.Sprite):
    def __init__(self,x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = ((x, y))
        
class Player(pygame.sprite.Sprite):
    def __init__(self,x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.image.fill("blue")
        self.rect.center = (x, y)


    # def update(self, shift_x, shift_y):
    #     self.rect.x += shift_x
    #     self.rect.y += shift_y
        
class Game():

    def __init__(self, main_tile_group, player_group):
        self.level = 1




ground_tile_group = pygame.sprite.Group()
terrain_tile_group = pygame.sprite.Group()
object_tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tmx_data = load_pygame("resources/levels/level01.tmx")

ground_layer = tmx_data.get_layer_by_name("ground")
terrain_layer = tmx_data.get_layer_by_name("terrain")
object_layer = tmx_data.get_layer_by_name("objects")

for x,y,image in ground_layer.tiles():
    tile = Tile(x * TILE_SIZE, y * TILE_SIZE, image)
    ground_tile_group.add(tile)
for x,y,image in terrain_layer.tiles():
    tile = Tile(x * TILE_SIZE, y * TILE_SIZE, image)
    terrain_tile_group.add(tile)
for obj in object_layer:
    if obj.type == "Player": 
        player = Player(x * TILE_SIZE//16, y * TILE_SIZE//16)
        player_group.add(player)
    else:
        tile = Tile(obj.x * TILE_SIZE//16, obj.y * TILE_SIZE//16, obj.image)
        object_tile_group.add(tile)





running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    map_shift_x = 0
    map_shift_y = 0

    player_shift_x = 0
    player_shift_y = 0




    display_surface.fill("black")

    ground_tile_group.update()
    ground_tile_group.draw(display_surface)
    terrain_tile_group.update()
    terrain_tile_group.draw(display_surface)
    object_tile_group.update()
    object_tile_group.draw(display_surface)
    player_group.update()
    player_group.draw(display_surface)
    


    pygame.display.update()
    clock.tick(FPS)