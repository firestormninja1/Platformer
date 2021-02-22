import pygame
import sys
import os
# ------ IMPORTANT ------
pygame.init()
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#-------------------------- Doing stuff with coords --------------------------#

def modify_coords(screen,coords,to_draw,block,dict,erase,erase_color):

    for i in range(len(coords)):
        for j in range(len(coords[i])):
            for pos in to_draw:
                mouse_x = pos[0] - 32*j
                mouse_y = pos[1] - 32*i

                obj = coords[i][j]
                if obj.recta.collidepoint((mouse_x,mouse_y)):
                    if erase == True:
                        coords[i][j].background = dict[erase_color]
                        coords[i][j].identifier = 0
                    else:
                        coords[i][j].background = block

                        if block == dict[list(dict.fromkeys(dict))[0]]: # 0th element
                            coords[i][j].identifier = 1
                        elif block == dict[list(dict.fromkeys(dict))[1]]:
                            coords[i][j].identifier = 2

                    to_draw = []
    return coords,to_draw

#--------------------- lines/margin/borders for surface ----------------------#

def plot_lines(screen, coords):
    for coord in range(len(coords)):
        for obj in range(len(coords[coord])):
            j = coords[coord][obj]
            #pygame.draw.rect(j.c, (255,255,255), (0,0,j.w,j.h), 3)
            if j.background != None:
                j.c.blit(j.background,(0,0))

            screen.blit(j.c,(j.w*obj, j.h*coord))

            j = coords[coord][obj]
            pygame.draw.rect(j.c, (150,150,150), (0,0,j.w,j.h), 3)
            screen.blit(j.c,(j.w*obj,j.h*coord))
