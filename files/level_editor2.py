#---------------------------------------------------------------------------
''' version 1.5 '''
import pygame
import sys
import os.path
import magic
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
SCREEN_WIDTH,SCREEN_HEIGHT = TILE_DIMENSION_X*blocks_x, TILE_DIMENSION_Y*blocks_y #just to make sure that the pixel arts can nicel fit ygm
'''-------------------------------------------------------------------------'''


# ------ setting up font
main_font = pygame.font.SysFont('comicsans',35)

# ------ Title/caption and icon
# pygame.display.set_caption("Moving Sprite " + 'version ' + version)
# icon = pygame.image.load('C://Users/Harsh/Desktop/A level CS/Pygame/Simple platformer/images/grass.png')
# pygame.display.set_icon(icon)
pygame.display.set_caption('transforming sutff')

RED = (255,0,0)
BLUE = (0,0,255)

class rectangle:
    def __init__(self, screen, w=TILE_DIMENSION_X, h=TILE_DIMENSION_Y):
        self.screen = screen
        self.background = None
        self.b = 'black'
        self.w = w
        self.h = h
        self.c = self.draw_surf()
        self.recta = self.c.get_rect()
        self.identifier = 0

    def draw_surf(self):
        return pygame.Surface((self.w,self.h))

#----------------------------------- main ------------------------------------#
def get_dims():
    return SCREEN_WIDTH,SCREEN_HEIGHT

def get_block_x():
    return blocks_x
def main():
    # ------ doing screen related stuff
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    coords = []
    to_draw = []

    for j in range(0,SCREEN_HEIGHT,32):
        a = []
        for i in range(0,SCREEN_WIDTH,32):
            rec1 = rectangle(screen)
            a.append(rec1)
        coords.append(a)

    dict = {
        'grass' : pygame.image.load('images/grass_block.png'),
        'dirt' : pygame.image.load('images/dirt_block.png'),
        'black': pygame.image.load('images/black.png')
    }

    block = dict['dirt']
    current,default = 'dirt','dirt'
    erase,erase_color = False,'black'

    while True:
        block = dict[default] # this is here cuz when you press right click to erase,
        # it sets that as the current background to add to any surfaces where theres
        #a mouse pointer... essentially alllows you to resume drawing with previous
        #'block' instead of having to select it again

        screen.fill((8,8,8))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return coords
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    current = 'grass'
                    default = 'grass'
                if event.key == pygame.K_d:
                    current = 'dirt'
                    default = 'dirt'
                if event.key == pygame.K_ESCAPE:
                    return coords
                    pygame.quit()


        mouse_press = pygame.mouse.get_pressed()
        #print(mouse_press)
        #1 = clicked, 0 = not clicked
        # returns (a,b,c) a = left click, b = middle, c = right click
        if any((mouse_press[0],mouse_press[2])): # if left or right click is pressed
            if mouse_press[0] == 1:
                erase = False
                mouse_pos = pygame.mouse.get_pos()
                to_draw.append(mouse_pos)
                block = dict[current]

            if mouse_press[2] == 1:
                erase = True
                mouse_pos = pygame.mouse.get_pos()
                to_draw.append(mouse_pos)

            change = magic.modify_coords(screen,coords,to_draw,block,dict,erase,erase_color) # only calling this when right or left click pressed
                                                                                       # so it saved unnecessary nested for loop execution ygm
            coords,to_draw = change[0],change[1] # go ahead and updates the values

        magic.plot_lines(screen,coords)

        pygame.display.update()
        clock.tick(60)

final = []
a = []
if __name__ == '__main__':
    map = main()

    for y in map:
        for x in y:
            a.append(x.identifier)
        final.append(a)
        a = []
    save = 'maps.txt'

    with open(save,'w') as file:
        for i in final:
            for val in i:
                file.write(str(val))
            #file.write(',')
        file.close()
    print(final)


# EXPLANATION of shitty map logic xD:
# basically, the reason i did the dimensinos as a multiple of 32 is for this reason...
# for each tile in the 'map' its gonna be 32 px. therefore we can reference the
# x and y coordinates based on the index in the 2d list..... if there is a block at
# index 5 (total indexes on x xis == to the dimension you pyt before) then the
# x coordinate of where it needs to be placed, is 5*32 and likewise, same for y
# if the block was at index (5,3) it means 3 indexes, down in the list == 3*32 == y coord
# and then 5 inside of that 3rd list == 5*32 == x coord
# we can use this sort of mapping style in a main project to plot the tiles at their
# respective coordinates
