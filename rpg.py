import pygame
import rpg_levels as rpg_levels
from spritesheet import SpriteSheet


pygame.init()

TILE_SIZE = 30
BORDER_COLOR = (255, 0, 0)
WINDOW_W = TILE_SIZE * 31
WINDOW_H = TILE_SIZE * 21
CENTER_X = WINDOW_W // 2
CENTER_Y = WINDOW_H // 2
SKY_BLUE = (177, 229, 233)
PLAYER_SPEED = 5

display_surface = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("RPG")

FPS = 60
clock = pygame.time.Clock()


sprite_sheet = SpriteSheet("roguelikeSheet_transparent.png")




class Tile(pygame.sprite.Sprite):
    def __init__(self,x, y, tile_type):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        if tile_type == "B":
            # self.image.fill(BORDER_COLOR)
            self.image = sprite_sheet.get_image_rect(5, 5, 30, 30)
        elif tile_type == "P":
            self.image.fill(SKY_BLUE)
            pygame.draw.circle(self.image, "grey", (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 2)
        else:
            self.image.fill(SKY_BLUE)
            pygame.draw.circle(self.image, "grey", (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 2)
        self.rect.topleft = ((x, y))

    def update(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y
        

class Player(pygame.sprite.Sprite):
    def __init__(self,x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.image.fill("blue")
        self.rect.topleft = (x, y)


    def update(self, shift_x, shift_y):
        self.rect.x += shift_x
        self.rect.y += shift_y
        
class Game():

    def __init__(self, main_tile_group, player_group):
        self.levels = rpg_levels.levels
        self.level = 1
        self.main_tile_group = main_tile_group
        self.player_group = player_group
        # self.font = pygame.font.Font("MondayMonkey.otf", 40)

    def new_level(self):
        self.level += 1
        main_tile_group.empty()
        self.load_tile_map()

    def load_tile_map(self):
        level = self.levels[self.level - 1]
        for row in range(len(level)):
            for col in range(len(level[row])):
                tile = Tile(col * TILE_SIZE, row * TILE_SIZE, level[row][col])
                self.main_tile_group.add(tile)
                if col == 0 and row == 0:
                    self.tltile = tile
                elif col == len(level[row]) - 1 and row == len(level) - 1:
                    self.brtile = tile
                if level[row][col] == "P":
                    self.player = Player(col * TILE_SIZE, row * TILE_SIZE)
                    self.player_group.add(self.player)


main_tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
game = Game(main_tile_group, player_group)
game.load_tile_map()


#center viewport on player
offset_x = (WINDOW_W // 2) - game.player.rect.left
offset_y = (WINDOW_H // 2) - game.player.rect.top
game.player.rect.topleft = ((WINDOW_W // 2), (WINDOW_H // 2))

for sprite in main_tile_group.sprites():
    sprite.rect.x += offset_x
    sprite.rect.y += offset_y


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    map_shift_x = 0
    map_shift_y = 0

    player_shift_x = 0
    player_shift_y = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if (game.tltile.rect.left >= 0 and game.player.rect.left > 30) or (game.player.rect.x > CENTER_X):
            player_shift_x = -PLAYER_SPEED
        elif game.tltile.rect.left < 0:
            map_shift_x = PLAYER_SPEED
    elif keys[pygame.K_RIGHT]:
        if (game.brtile.rect.right <= WINDOW_W and game.player.rect.right < WINDOW_W - 30) or (game.player.rect.x < CENTER_X):
            player_shift_x = PLAYER_SPEED
        elif game.brtile.rect.right > WINDOW_W:
            map_shift_x = -PLAYER_SPEED
    elif keys[pygame.K_UP]:
        if (game.tltile.rect.top >= 0 and game.player.rect.top > 30) or (game.player.rect.y > CENTER_Y):
            player_shift_y = -PLAYER_SPEED
        elif game.tltile.rect.top < 0:
            map_shift_y = PLAYER_SPEED
    elif keys[pygame.K_DOWN]:
        if (game.brtile.rect.bottom <= WINDOW_H and game.player.rect.bottom < WINDOW_H - 30) or (game.player.rect.y < CENTER_Y):
            player_shift_y = PLAYER_SPEED
        elif game.brtile.rect.bottom > WINDOW_H:
            map_shift_y = -PLAYER_SPEED



    display_surface.fill("black")

    main_tile_group.update(map_shift_x, map_shift_y)
    main_tile_group.draw(display_surface)

    player_group.update(player_shift_x, player_shift_y)
    player_group.draw(display_surface)

    pygame.display.update()
    clock.tick(FPS)