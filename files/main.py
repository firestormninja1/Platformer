#version 3
#---------------------------------------------------------------------------
import pygame
import sys
import os.path
import level_editor2 as ref
# ------ IMPORTANT ------
pygame.init()
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# ------ setting screen width and height
'''------------------------------- IMPORTANT -------------------------------'''
'''---------- Dimensions -----------'''
# enter in your dimensions for how big you want the map/canvas to be
TILE_DIMENSION_X,TILE_DIMENSION_Y = 32,32
blocks_x = 30
blocks_y = 19
SCREEN_WIDTH,SCREEN_HEIGHT = ref.get_dims()[0],ref.get_dims()[1] #just to make sure that the pixel arts can nicel fit ygm
print(SCREEN_WIDTH,SCREEN_HEIGHT)
'''-------------------------------------------------------------------------'''


# ------ setting up font
main_font = pygame.font.SysFont('comicsans',35)

# ------ Title/caption and icon
# pygame.display.set_caption("Moving Sprite " + 'version ' + version)
# icon = pygame.image.load('C://Users/Harsh/Desktop/A level CS/Pygame/Simple platformer/images/grass.png')
# pygame.display.set_icon(icon)
pygame.display.set_caption('transforming sutff')

RED = (255,0,0)
BLUE = (146,244,255)

class tile_rect:
    def __init__(self,image,x,y,w,h):
        self.image = image
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.rect = self.get_Rect()

    def get_Rect(self):
        return pygame.Rect(self.x,self.y,self.width,self.height)

    def tile_surface(self,img):
        tile_surface = pygame.Surface((img.get_width(),img.get_height()))
        return tile_surface

class Player:
    def __init__(self,x,y,w,h):
        self.x,self.y = x,y
        self.width,self.height = w,h
        self.gravity = 6
        self.rect = pygame.Rect((self.x,self.y,self.width,self.height))
        self.x_move = 4
        self.y_move = 4
        self.y_momentum = 3
        self.on_ground = False

    def draw_rect(self,surface):
        pygame.draw.rect(surface,(255,0,0), (self.x,int(self.y),self.width,self.height),4)


    def collision_check(self,tiles):
        collision_list = []
        for tile in tiles:
            if self.rect.colliderect(tile[1].rect):
                collision_list.append(tile[1])
        return collision_list

    def player_move_x(self,tiles):
        self.x += self.x_move
        self.rect.x = self.x
        collision_list = self.collision_check(tiles)
        if len(collision_list) == 0:
            return None
        for collision in collision_list:
            if self.x_move > 0:
                self.rect.right = collision.rect.left
                self.x = collision.rect.left - self.width
            elif self.x_move < 0:
                self.rect.left = collision.rect.right
                self.x = collision.rect.right
        return 'collided'
    
    def player_move_y(self,tiles):
        self.y += (self.y_move+self.y_momentum)
        self.rect.y = int(self.y)
        collision_list = self.collision_check(tiles)
        
        for collision in collision_list:
            if self.y_momentum > 0:
                self.rect.bottom = collision.rect.top
                self.y = int(collision.rect.top - self.height)
                return 'no'
            elif self.y_momentum < 0:
                self.rect.top = collision.rect.bottom
                self.y = collision.rect.bottom
                return 'yes'
        
#----------------------------------- main ------------------------------------#

def main():
    # ------ doing screen related stuff
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    block_pointer = {
    '0':'black',
    '1':'grass',
    '2':'dirt'
    }

    blocks= {
    'grass' : pygame.image.load('images/grass_block.png'),
    'dirt' : pygame.image.load('images/dirt_block.png'),
    'black': pygame.image.load('images/black.png')
    }
    

    game_map = []
    with open('C:/Users/Harsh/Desktop/A level CS/Pygame/Simple platformer/Game/maps/maps.txt','r') as map_file:
        f = map_file.read()
        steps = ref.get_block_x()
        start = steps
        game_map.append(f[0:steps+1])
        for i in range(start,len(f),steps):
            game_map.append(f[i:i+steps])


    TILE_DIMENSION_X,TILE_DIMENSION_Y = ref.TILE_DIMENSION_X,ref.TILE_DIMENSION_Y

    list_of_tiles = []
    for coord in range(len(game_map)):
        for j in range(len(game_map[coord])):
            if game_map[coord][j] != '0':
                num = game_map[coord][j]
                img_name = block_pointer[num]
                img = blocks[img_name]

                tile = tile_rect(img,TILE_DIMENSION_X*j,coord*TILE_DIMENSION_Y,img.get_width(),img.get_height())
                tile_surf = tile.tile_surface(img)
                tile_surf.blit(img,(0,0))
                
                list_of_tiles.append([tile_surf,tile,img_name])
    
    player = Player(316,284,32,32)

    jumped = False
    jumped_dist = 0
    y_momentum = 0
    b = pygame.image.load('images/background.png')
    b = pygame.transform.scale(b,(960,608))
    in_air = 0
    while True:
 
        player.x_move = 0
        player.y_move = 0
        #player.gravity = 3
        #player.gravity = 10

        moving = {
        'right':False,
        'left':False,
        'up':False,
        'down':False
        }

        screen.fill(BLUE)
        screen.blit(b,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_SPACE and in_air <= 3: # allow for jump within a few miliseconds of falling
                
                    y_momentum = -10
                    lock = True
                    player.on_ground = False

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d] and player.x < SCREEN_WIDTH - player.width: 
            player.x_move = 4          

        if keys[pygame.K_a] and player.x > 0:
            player.x_move =-4

        if keys[pygame.K_a] and keys[pygame.K_d]:
            player.x_move = 0
            
        player.y_momentum = y_momentum
        y_momentum += 0.4
        in_air += 0.5

        if player.y_momentum > 7:
            y_momentum = 7
       
        x_col = player.player_move_x(list_of_tiles)
        if x_col == 'collided': # just a cool lil feature which basically allows you to jump between walls
            in_air = 0

        if player.y > 0 and player.y+player.height < SCREEN_HEIGHT:
            a  = player.player_move_y(list_of_tiles)
            if a == 'yes':
                y_momentum = 0
                lock=True
            if a=='no':
                player.on_ground=True
                in_air = 0
        else:
            y_momentum = 0
            player.y += 5


        # if keys[pygame.K_w] and player.y > 0:
        #     player.y -= player.gravity
        #     moving['up'] = True
        # if keys[pygame.K_s] and player.y < SCREEN_HEIGHT + player.height:
        #     player.y += player.gravity
        #     moving['down'] = True

        # for coord in range(len(game_map)):
        #     for j in range(len(game_map[coord])):
        #         num = game_map[coord][j]
        #         screen.blit(blocks[images[num]],(TILE_DIMENSION_X*j,coord*TILE_DIMENSION_Y))
        
        for coord in list_of_tiles: # no need for nested for loop like done previously
            screen.blit(coord[0],(coord[1].x,coord[1].y))
            #coord[1] contains tile_rec object for each coord in game map
            #coord[0] is just a surface to blit the images onto
                
        player.draw_rect(screen)
        
        
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
