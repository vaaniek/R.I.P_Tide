# Names: Rebecca Bai, Vaanie Kathirkamar
# Course: ICS 3U1-01
# Assignment: CPT
# Description: Image Loader Testing 
# Date Started: June 9, 2016
# Date Delivered: June 16, 2016
# Last Modified: June 15, 2016

#import functions
import pygame
import time
WHITE = (255,255,255)
BLACK = (0,0,0)

#initalize pygame
pygame.init()
screen_width = 700
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])

#put the fileimage you want to load here
p = pygame.image.load("images/tsunami_potion.png").convert() 
p.set_colorkey(BLACK) #set backgroud transparency
p.get_rect()

done = False
clock = pygame.time.Clock()

#---------------- Main program loop -------------
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True

    #clear screen
    screen.fill(WHITE)

    #draw the loaded image
    screen.blit(p, [100,100])

    #display what has been drawn
    pygame.display.flip()

    #limit to 60 frames per second
    clock.tick(60)
    
#be IDLE friendly 
pygame.quit() 
