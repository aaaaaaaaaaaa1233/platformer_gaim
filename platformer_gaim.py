import pygame
import random
import sys
from spritesheet import SpriteSheet
import tile_maps as tm
pygame.init()

 
 

WINDOW_W = 1050
WINDOW_H = 700
SKY_BLUE = (160, 210, 220)
BLACK = (0,0,0)


display_surface = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("platformer gaim")







FPS = 60
clock = pygame.time.Clock()


sprite_sheet = SpriteSheet("platformer_gaim/tiles_spritesheet.png", "platformer_gaim/tiles_spritesheet.xml")


class Tile(pygame.sprite.Sprite):
    def __init__(self,x, y, imageint, maingroup, subgroup = ""):
        super().__init__()

        self.is_door_bottom = False
        self.is_door_top = False

        if imageint == 1:
            self.image = sprite_sheet.get_image_name("grassCenter.png")
        elif imageint == 2:
            self.image = sprite_sheet.get_image_name("grassMid.png")  
        elif imageint == 3:
            self.image = sprite_sheet.get_image_name("liquidWater.png")      
        elif imageint == 5:
            self.image = sprite_sheet.get_image_name("door_closedMid.png")      
            self.is_door_bottom = True
        elif imageint == 6:
            self.image = sprite_sheet.get_image_name("door_closedTop.png")      
            self.is_door_top = True
        elif imageint == 8:
            self.image = sprite_sheet.get_image_name("liquidLava.png")      
        elif imageint == 9:
            self.image = sprite_sheet.get_image_name("liquidWater.png")      
        elif imageint == 10:
            self.image = sprite_sheet.get_image_name("castleMid.png")      
        elif imageint == 11:
            self.image = sprite_sheet.get_image_name("castleCenter.png")      
        elif imageint == 12:
            self.image = sprite_sheet.get_image_name("bridgeLogs.png")
            self.image = pygame.transform.flip(self.image, False, True)
        elif imageint == 13:
            self.image = sprite_sheet.get_image_name("boxAlt.png")      
        elif imageint == 14:
            self.image = sprite_sheet.get_image_name("stoneMid.png")      
        elif imageint == 15:
            self.image = sprite_sheet.get_image_name("stoneCenter.png")      



        maingroup.add(self)
        if subgroup != "":
            subgroup.add(self)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Player(pygame.sprite.Sprite):

    def __init__(self, platform, water, door, game, ice, lava):
        super().__init__()
        self.spritesheet = SpriteSheet("platformer_gaim/p1_spritesheet.png")

        self.move_right_sprites = []
        self.move_left_sprites = []
        
        self.move_right_sprites.append(self.spritesheet.get_image_rect(0, 0, 72, 97).convert_alpha())
        self.move_right_sprites.append(self.spritesheet.get_image_rect(73, 0, 72, 97).convert_alpha())
        self.move_right_sprites.append(self.spritesheet.get_image_rect(146, 0, 72, 97).convert_alpha())
        self.move_right_sprites.append(self.spritesheet.get_image_rect(0, 0, 72, 97).convert_alpha())
        self.move_right_sprites.append(self.spritesheet.get_image_rect(0, 98, 72, 97).convert_alpha())
        self.move_right_sprites.append(self.spritesheet.get_image_rect(73, 98, 72, 97).convert_alpha())
        self.move_right_sprites.append(self.spritesheet.get_image_rect(146, 98, 72, 97).convert_alpha())
        self.move_right_sprites.append(self.spritesheet.get_image_rect(219, 0, 72, 97).convert_alpha())
        self.move_right_sprites.append(self.spritesheet.get_image_rect(292, 0, 72, 97).convert_alpha())
        self.move_right_sprites.append(self.spritesheet.get_image_rect(219, 98, 72, 97).convert_alpha())
        self.move_right_sprites.append(self.spritesheet.get_image_rect(365, 0, 72, 97).convert_alpha())
        self.move_right_sprites.append(self.spritesheet.get_image_rect(292, 98, 72, 97).convert_alpha())



        for sprite in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        self.stand_right_sprite = self.spritesheet.get_image_rect(67, 196, 66, 92).convert_alpha()
        self.stand_left_sprite = pygame.transform.flip(self.stand_right_sprite, True, False)

        self.currentsprite = 0
        self.animate_speed = 0.5
        
        
        self.image = self.stand_right_sprite
        self.rect = self.image.get_rect()



       
        self.platform_tiles = platform
        self.water_tiles = water
        self.door_tiles = door
        self.game = game
        self.ice = ice
        self.lava = lava

        #kinematic vectors
        self.position = pygame.math.Vector2(50, 300)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        

        #kinematic constants
        self.HORIZONTAL_ACCELERATION = 1
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCELERATION = 0.5
        self.VERTICAL_JUMP_SPEED = 15
        self.TERMINAL_VELOCITY = 15

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.move()
        self.check_collisions()
    
    def move(self):
        self.acceleration = pygame.math.Vector2(0, self.VERTICAL_ACCELERATION)

        #set acceleration vector
        keys = pygame.key.get_pressed()    
        if keys[pygame.K_LEFT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION * -1
            self.animate(self.move_left_sprites)
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites)
        else:
            if self.velocity.x > 0:
                self.image = self.stand_right_sprite
            else:
                self.image = self.stand_left_sprite

        if keys[pygame.K_UP]:
            if self.velocity.y == 0:
                self.jump()    


        #calculate new kinematic values
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        if self.velocity.y > self.TERMINAL_VELOCITY:
            self.velocity.y = self.TERMINAL_VELOCITY
        self.position += self.velocity + (0.5 * self.acceleration)     

        #update rect
        if self.position.x < 0 and self.check_blocks_on_other_side("right"):
            self.position.x = 0
        elif self.position.x > WINDOW_W - self.rect.width and self.check_blocks_on_other_side("left"):
            self.position.x = WINDOW_W - self.rect.width  
        else:
            half_width = self.rect.width // 2
            if self.position.x < -half_width:
                self.position.x = WINDOW_W - half_width
            if self.position.x > WINDOW_W - half_width:
                self.position.x = -half_width
            if self.position.y > WINDOW_H:
                self.position.y = 0

        self.rect.bottomleft = self.position
        

    def check_blocks_on_other_side(self, side):
        if side == "left":
            test_rect = self.rect
            test_rect.left = 0
            test_rect = test_rect.inflate(-6, -6)
            for tile in self.platform_tiles:
                if pygame.Rect.colliderect(tile.rect, test_rect):
                    return True
                
            return False
        elif side == "right":
            test_rect = self.rect
            test_rect.right = WINDOW_W
            test_rect = test_rect.inflate(-6, -6)
            for tile in self.platform_tiles:
                if pygame.Rect.colliderect(tile.rect, test_rect):
                    return True
            return False    


    def animate(self, sprite_List):
        if self.currentsprite < len(sprite_List) - 1:
            self.currentsprite += 1
        else:
            self.currentsprite = 0

        self.image = sprite_List[self.currentsprite]    


    def check_collisions(self):

        collided_door = pygame.sprite.spritecollide(self, self.door_tiles, False)
        if collided_door and self.game.door_is_open:
            self.game.new_level()
        else:
            collided_lava = pygame.sprite.spritecollide(self, self.lava, False)

            if collided_lava:

                game.die()
            else:

                collided_ice = pygame.sprite.spritecollide(self, self.ice, False)

                if collided_ice:
                    
                    centx = self.rect.centerx
                    centy = self.rect.centery

                    self.HORIZONTAL_FRICTION = 0.075

                    for collided_sprite in collided_ice:
                        #if falling then 
                        if (self.velocity.y > 0 and 
                        self.rect.bottom > collided_sprite.rect.top and
                        centy < collided_sprite.rect.top and 
                        self.rect.left < collided_sprite.rect.right - 6 and 
                        self.rect.right > collided_sprite.rect.left + 5):
                            self.position.y = collided_sprite.rect.top + 1
                            self.velocity.y = 0
                        #jump'n bump head    
                        elif (self.velocity.y <= 0 and
                            centy > collided_sprite.rect.bottom and
                            self.rect.left < collided_sprite.rect.right - 6 and
                            self.rect.right > collided_sprite.rect.left + 5):
                            self.velocity.y = 0
                            while pygame.sprite.collide_mask(self, collided_sprite):
                                self.position.y += 1
                                self.rect.bottomleft = self.position
                        elif centx > collided_sprite.rect.centerx and centy > collided_sprite.rect.top:
                            self.position.x = collided_sprite.rect.right + 2
                            self.rect.bottomleft = self.position
                        elif centx < collided_sprite.rect.centerx and centy > collided_sprite.rect.top:
                            self.position.x = collided_sprite.rect.left - self.rect.width - 2
                            self.rect.bottomleft = self.position

                collided_platforms = pygame.sprite.spritecollide(self, self.platform_tiles, False, pygame.sprite.collide_mask)


                if collided_platforms:
                    
                    centx = self.rect.centerx
                    centy = self.rect.centery
                    
                    self.HORIZONTAL_FRICTION = 0.15

                    for collided_sprite in collided_platforms:
                        #if falling then 
                        if (self.velocity.y > 0 and 
                        self.rect.bottom > collided_sprite.rect.top and
                        centy < collided_sprite.rect.top and 
                        self.rect.left < collided_sprite.rect.right - 6 and 
                        self.rect.right > collided_sprite.rect.left + 5):
                            self.position.y = collided_sprite.rect.top + 1
                            self.velocity.y = 0
                        #jump'n bump head    
                        elif (self.velocity.y <= 0 and
                            centy > collided_sprite.rect.bottom and
                            self.rect.left < collided_sprite.rect.right - 6 and
                            self.rect.right > collided_sprite.rect.left + 5):
                            self.velocity.y = 0
                            while pygame.sprite.collide_mask(self, collided_sprite):
                                self.position.y += 1
                                self.rect.bottomleft = self.position
                        elif centx > collided_sprite.rect.centerx and centy > collided_sprite.rect.top:
                            self.position.x = collided_sprite.rect.right + 2
                            self.rect.bottomleft = self.position
                        elif centx < collided_sprite.rect.centerx and centy > collided_sprite.rect.top:
                            self.position.x = collided_sprite.rect.left - self.rect.width - 2
                            self.rect.bottomleft = self.position
            

    
    def jump(self):
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_tiles, False, pygame.sprite.collide_mask)
        collided_ice = pygame.sprite.spritecollide(self, self.ice, False, pygame.sprite.collide_mask)
        if collided_platforms:
            if self.rect.bottom > collided_platforms[0].rect.top:
                self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED
        if collided_ice:
            if self.rect.bottom > collided_ice[0].rect.top:
                self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED

    def set_start_pos(self, x, y):
        self.position = (x, y)

class Game():

    def __init__(self):
        self.tile_maps = tm.tile_maps
        self.keys_collected = 0
        self.all_keys_collected = False
        self.level = 1
        self.door_is_open = False
        self.font = pygame.font.Font("MondayMonkey.otf", 40)

    def new_level(self):
        self.level += 1
        self.door_is_open = False
        self.all_keys_collected = False
        main_tile_group.empty()
        platform_tile_group.empty()
        water_tile_group.empty()
        key_group.empty()
        door_tile_group.empty()
        self.load_tile_map()
        self.keys_collected = 0

    def die(self):
        main_tile_group.empty()
        platform_tile_group.empty()
        water_tile_group.empty()
        key_group.empty()
        door_tile_group.empty()
        self.load_tile_map()
        self.keys_collected = 0

    def load_tile_map(self):
        tile_map = self.tile_maps[self.level - 1]
        for row in range(len(tile_map)):
            for col in range(len(tile_map[row])):
                if tile_map[row][col] == 1:
                    Tile(col * 35, row * 35, 1, main_tile_group, platform_tile_group)
                elif tile_map[row][col] == 2:
                    Tile(col * 35, row * 35, 2, main_tile_group, platform_tile_group)
                elif tile_map[row][col] == 3:
                    Tile(col * 35, row * 35, 3, main_tile_group, water_tile_group)
                elif tile_map[row][col] == 4:
                    key = Key(col * 35, row * 35, game)
                    key_group.add(key)
                elif tile_map[row][col] == 5:
                    Tile(col * 35, row * 35, 5, main_tile_group, door_tile_group)
                elif tile_map[row][col] == 6:
                    Tile(col * 35, row * 35, 6, main_tile_group, door_tile_group)  
                elif tile_map[row][col] == 7:
                    player.set_start_pos(col * 35, row * 35)
                elif tile_map[row][col] == 8:
                    Tile(col * 35, row * 35, 8, main_tile_group, lava_tile_group)  
                elif tile_map[row][col] == 9:
                    Tile(col * 35, row * 35, 9, main_tile_group, ice_tile_group)  
                elif tile_map[row][col] == 10:
                    Tile(col * 35, row * 35, 10, main_tile_group, platform_tile_group)
                elif tile_map[row][col] == 11:
                    Tile(col * 35, row * 35, 11, main_tile_group, platform_tile_group)
                elif tile_map[row][col] == 12:
                    Tile(col * 35, row * 35, 12, main_tile_group, platform_tile_group)
                elif tile_map[row][col] == 13:
                    Tile(col * 35, row * 35, 13, main_tile_group, platform_tile_group)
                elif tile_map[row][col] == 14:
                    Tile(col * 35, row * 35, 14, main_tile_group, platform_tile_group)
                elif tile_map[row][col] == 15:
                    Tile(col * 35, row * 35, 15, main_tile_group, platform_tile_group)
        
    def update(self):
        if self.all_keys_collected:
            self.door_is_open = True
            for sprite in main_tile_group:
                if sprite.is_door_top:
                    sprite.image = sprite_sheet.get_image_name("door_openTop.png")
                if sprite.is_door_bottom:
                    sprite.image = sprite_sheet.get_image_name("door_openMid.png")
    
    def draw(self, display_surface):
        keys_collected_text = self.font.render(f"keys collected: {game.keys_collected}", True, BLACK, None)
        keys_collected_rect = keys_collected_text.get_rect()
        keys_collected_rect.center = (WINDOW_W//2, 50)
        display_surface.blit(keys_collected_text, keys_collected_rect)

        level_text = self.font.render(f"level: {game.level}", True, BLACK, None)
        level_rect = level_text.get_rect()
        level_rect.center = (WINDOW_W//2 + 200, 50)
        display_surface.blit(level_text, level_rect)

class Key(pygame.sprite.Sprite):

    def __init__(self, x, y, game):
        self.game = game
        super().__init__()
        self.image = pygame.image.load("platformer_gaim/key.webp")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)



        self.rect.x = x - 7
        self.rect.y = y - 10
    def update(self, player):
        self.check_collisions(player)
    
    def check_collisions(self, player):
        collided_sprites = pygame.sprite.collide_mask(self, player)
        if collided_sprites:
            self.game.keys_collected += 1
            self.kill()
            if not key_group:
                self.game.all_keys_collected = True

              

    


        

main_tile_group = pygame.sprite.Group()
platform_tile_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
door_tile_group = pygame.sprite.Group()
lava_tile_group = pygame.sprite.Group()
ice_tile_group = pygame.sprite.Group()


game = Game()

player = Player(platform_tile_group, water_tile_group, door_tile_group, game, ice_tile_group, lava_tile_group)
player_group.add(player)

game.load_tile_map()











running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.jump()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        FPS = 5
    else:
        FPS = 60    

    



    #fill bg
    display_surface.fill(SKY_BLUE)

    #draw tile map
    main_tile_group.draw(display_surface) 

    #update game

    game.update()
    game.draw(display_surface)
    



    #draw player
    player_group.update()
    player_group.draw(display_surface)

    key_group.update(player)
    key_group.draw(display_surface)


    pygame.display.update()
    clock.tick(FPS)

  