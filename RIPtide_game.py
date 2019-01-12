# Name: Rebecca Bai, Vaanie Kathirkamar
# Course: ICS 3U1-01
# Assignment: CPT
# Description: "RIPtide-A Survival Video Game" 
# Date Started: June 3, 2016
# Date Delivered: June 16, 2016
# Last Modified: June 15, 2016

"""
Information for classes and sprites were found at:
http://programarcadegames.com/
"""
#import all necessary functions 
import pygame 
import time
import random

#initialize the game engine
pygame.init()

#define some colors 
BLACK = (0, 0 , 0)
WHITE = (255, 255, 255)
SAND = (232, 205, 162)
BLUE = (0, 187, 209)
AQUA = (176, 255, 213)
PINK = (255, 176, 196)

#set height and width of screen
screen_width = 700
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])

clock = pygame.time.Clock()

#---------- Classes -----------------------------------------------------------------------------
#Player class
#Authors: Rebecca Bai, Vaanie K.
#Last Updated: June 15, 2016 

class Player(pygame.sprite.Sprite):
    '''this class represents the character that the player controls''' 
    def __init__(self,x,y):
        #call parent constructor 
        super(Player, self).__init__()
        
        #load the sprite picture for the player 
        self.image = pygame.image.load("images/player.png").convert()
        self.image.set_colorkey(WHITE)

        #set the location where the image will appear 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        #set speed vector 
        self.change_x = 0
        self.change_y = 0

        #set the sound that will play if the player collides with spikes 
        self.pain = pygame.mixer.Sound("sounds/Pain.wav")

        #set the player's health bar 
        self.health = 90
        self.health_change = 0                      

                                       

    #--methods--
    def changespeed(self, x ,y):
        '''change the speed of the player'''
        self.change_x += x
        self.change_y += y
        
    def health_up(self):
        '''adds a heart to the player's health bar when called'''
        self.health_change = 30
        if self.health >= 90: #if player's health bar is full, it will not add a heart
            self.health_change = 0

    def health_down(self):
        '''takes away a heart from the player's health bar when called'''
        self.health_change = -30
        if self.health <= 30: #if the player runs out of health,
            youLose()         #load the game over screen 
            raise SystemExit() 
        


    def update(self):
        '''update the player position, as well as check for collisions with other objects'''
        self.rect.x += self.change_x #move left/right
        self.rect.y += self.change_y #move up/down
        self.health += self.health_change #update the health bar 
        self.health_change = 0
        
        #check if player has collided with an tree
        for t in tree_list:
            for player in player_list:
                if player.rect.colliderect(t.rect):
                    explosion_list.add(Explosion((t.rect.x, t.rect.y))) #if so, replace with an explosion
                    tsunami.tsunami_up() #and move the tsunami up.
                    t.kill()
                    
        #check if player has collided with a spike 
        for s in spike_list:
            for player in player_list:
                if player.rect.colliderect(s.rect):
                    explosion_list.add(Explosion((s.rect.x, s.rect.y)))
                    self.pain.play() #if so, play pain sound
                    self.health_down()#and deplete the health bar
                    s.kill()
                    
        #check if player has collided with a health powerup
        for s in health_p_list:
            for player in player_list:
                if player.rect.colliderect(s.rect):
                    self.health_up()#if so, add a heart back if any are missing
                              

        #check if player has collided with a tsunami powerup
        for t in tsunami_p_list:
            for player in player_list:
                if player.rect.colliderect(t.rect):
                    tsunami.tsunami_down() #if so, make the tsunami retreat           
        
        #the walls (the limits of where the player can move)
        if(self.rect.x<0):
            self.rect.x = 0
        elif(self.rect.x>660):
            self.rect.x = 660
                                
#-------------------------------------------------------------------------------------------
#Tsunami class
#Author: Rebecca Bai
#Last Updated: June 14, 2016
            
class Tsunami(pygame.sprite.Sprite):
    ''' This class represents the tsunami which is controlled by player collisions in-game'''
    def __init__(self, x, y):
        super(Tsunami, self).__init__()

        #load the sprite picture for the tsunami 
        self.image = pygame.image.load("images/tsunami.png").convert()
        self.image.set_colorkey(WHITE)

        #set the location where the image will appear 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #set speed vector 
        self.change_y = 0

    #--methods--
                
    def tsunami_up(self):
        '''moves the tsunami up when the method is called'''
        self.change_y = 50

    def tsunami_down(self):
        '''moves the tsunami down when the method is called''' 
        self.change_y = -50
        if self.rect.y >= 400: #will not move tsunami down if it is already at the lowest point
            self.change_y = 0
    
    def update(self):
        ''' update the tsunami's position '''
        self.rect.y -= self.change_y #move up/down
        self.change_y = 0

#------------------------------------------------------------------------------------------------
#Obstacle Class and Inheritances
#Author: Rebecca Bai
#Last Updated: June 14, 2016
        
class Obstacles(pygame.sprite.Sprite): #main obstacle class
    ''' this class represents the obstacles which are created in-game '''
    def __init__(self,startpos):
        super(Obstacles, self).__init__()
        #load the image for the obstacle sprite
        self.image = pygame.Surface([0,0])

        #set the location where the image will appear 
        self.rect = self.image.get_rect() 
        self.rect.x = random.randrange(0, screen_width)
        self.rect.y = random.randrange(-50, 100)
        self.rect.midtop = startpos
        
    #--methods--
   
    def update(self):
        '''update obstacle position'''
        self.rect.y += 1 #moves the obstacle down

        if self.rect.y > 400: #if obstacles fall too far, they are destroyed
            self.kill()
    

class Explosion(Obstacles, pygame.sprite.Sprite):
    ''' this class represents the explosion created from collisions with other objects // It inherits from the Obstacle class '''
    def __init__(self, startpos):
        super(Obstacles, self).__init__()
        #load the image for the explosion sprite 
        self.image = pygame.image.load("images/explosion.png").convert()
        self.image.set_colorkey(WHITE)

        #set the location where the image will appear 
        self.rect = self.image.get_rect()
        self.rect.midtop = startpos

#---------------------------------------------------------------------------------------------
#Powerup Class and Inheritances
#Author: Rebecca Bai
#Last Updated: June 15, 2016
            
class Powerups(pygame.sprite.Sprite): #main powerups class// *when collected, these disappear
    '''this class represents the powerups that can be collected in-game''' 
    def __init__(self):
        super(Powerups, self).__init__()
        #load the image for the powerup sprites
        self.image = pygame.Surface([0,0])

        #set the location where the image will appear
        self.rect = self.image.get_rect() 
        self.rect.x = random.randrange(0, screen_width)
        self.rect.y = random.randrange(0, 300)
        
        #--methods--

    def reset_pos(self): 
        '''reset position of powerup to top of screen at a random position'''
        self.rect.x = random.randrange(0, screen_width)
        self.rect.y = random.randrange(-500,-499) 
        
    def update(self):
        '''update position of powerup''' 
        self.rect.y += 1 #moves the powerup down 
        if self.rect.y > 1000: 
            self.reset_pos() #if it falls too far, reset the position
            

class Tsunami_p(Powerups, pygame.sprite.Sprite): #this powerup will make the tsunami "retreat" 
    '''this class represents the tsunami powerup // It inherits from the Powerups class '''
    def __init__(self):
        super(Tsunami_p, self).__init__()
        #load the image for the sprite
        self.image = pygame.image.load("images/tsunami_potion.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

class Health_p(Powerups, pygame.sprite.Sprite): #this powerup will restore health
    def __init__(self):
        '''this class represents the health powerup // It inherits from the Powerups class '''
        super(Health_p, self).__init__()
        #load the image for the sprite
        self.image = pygame.image.load("images/heart3.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

#------------------------------------------------------------------------------------------------
#HealthBar Class
#Author: Rebecca Bai
#Last Updated: June 15, 2016

class HealthBar(pygame.sprite.Sprite):
    '''this class represents the health bar of the player'''
    def __init__(self):
        super(HealthBar, self).__init__()
        #load the image for the sprite
        self.image = health_bar = pygame.image.load("images/heart3.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = -100

        #controls the number of hearts in the healthbar 
        self.health_change = 0
   
        #--methods--
    
    def update(self):
        '''updates the number of hearts the player has based on how much health they have '''
        self.health_change = 0
        if player.health >=30: #if the player has at least 30 health, one heart is drawn
            screen.blit(self.image, [10, 5])
        if player.health >=60: #if the player has at least 60 health, two hearts are drawn
            screen.blit(self.image, [25, 5])
        if player.health >=90: #if the player has at least 90 health, three hearts are drawn
            screen.blit(self.image, [40, 5]) 
        
#----------------------------------------------------------------------------------------------
#Function for the game over screen
#Author: Vaanie Kathirkamar
#Last Updated: June 14, 2016

def youLose():
    '''this is the screen for when you lose'''
    pygame.init()
    
    #creates a screen and fills it with a color
    screen = pygame.display.set_mode((700, 500))
    screen.fill(BLUE)
    pygame.display.set_caption("R.I.P.tide ~ RIP")
    font = pygame.font.SysFont('Calibri', 35, True, False)        

    ren = font.render("| RIP | GAME OVER |", True, WHITE)
    screen.blit(ren,(210, 200))
    
    ###Tells program to end if exit button is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit() 
            
    pygame.display.flip()

    
#------------- Game Code -----------------------------------------------------------------------------
'''everything is created // required variables are set'''

#all lists required to run game
player_list = pygame.sprite.Group()

tsunami_list = pygame.sprite.Group()

tree_list = pygame.sprite.Group()

spike_list = pygame.sprite.Group()

obstacle_list = pygame.sprite.Group()

powerup_list = pygame.sprite.Group()

tsunami_p_list = pygame.sprite.Group()

health_p_list = pygame.sprite.Group()

explosion_list = pygame.sprite.Group()

healthbar_list = pygame.sprite.Group()

#list of every sprite in game (includes player, obstacles, powerups)
all_sprites_list = pygame.sprite.Group()

#all variables required to run game
bar = 0

#variables required for drawing trees
tree_counter = 0
num_tree = 10 #determine number of trees on screen
max_trees = num_tree

#variables required for drawing spikes
spike_counter = 0
num_spike = 8 #determine number of spikes on screen
max_spikes = num_spike

#create player
player = Player(350,200)
player_list.add(player) 
all_sprites_list.add(player) 

#create tsunami
tsunami = Tsunami(0, 400)
tsunami_list.add(tsunami) 
all_sprites_list.add(tsunami)

#create health bar
health_bar = HealthBar()
healthbar_list.add(health_bar)

#create powerups
for i in range (1):
    tp = Tsunami_p()
    hp = Health_p()
  
    all_sprites_list.add(tp)
    all_sprites_list.add(hp)
  
    powerup_list.add(tp)
    powerup_list.add(hp)

    tsunami_p_list.add(tp)
    health_p_list.add(hp)

    #set the powerup location 
    tp.rect.x = random.randrange(screen_width)
    tp.rect.y = random.randrange(0,300)
    hp.rect.x = random.randrange(screen_width)
    hp.rect.y = random.randrange(0,300)

#loop until user clicks close button
done = False

clock = pygame.time.Clock()

#----------instructions page-----------------------------------------------------------------
#Creates the screen for instructions that appears when the program is run
#Author: Vaanie K.
#Last Updated: June 15, 2016
font = pygame.font.SysFont('Comic Sans', 30, True, False)
display_instructions = True
instruction_page = 1

#--Instruction Page Loop--
while not done and display_instructions:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN: #if the user clicks the mousebutton, the instructions will move to the next page
            instruction_page += 1
            if instruction_page == 3: #after the user hits the max number of pages, the instructions close
                display_instructions = False

    screen.fill(AQUA)

    if instruction_page == 1:
        text = font.render("R.I.P TIDE", True, PINK)
        screen.blit(text, [290, 200]) 
        text = font.render("Instructions: Click to Continue", True, PINK)
        screen.blit(text, [180, 400])

    if instruction_page == 2:
        text = font.render("Use Arrow Keys to move." , True, PINK)
        screen.blit(text, [10, 100])
        text = font.render("Avoid the trees and the spikes.", True, PINK)
        screen.blit(text, [10, 200])
        text = font.render("Avoid the tsunami.", True, PINK)
        screen.blit(text, [10, 300])
        text = font.render("Blue potions slow the tsunami, and hearts restore health.", True, PINK)
        screen.blit(text, [10, 400])

    clock.tick(60)
    pygame.display.flip()
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True
            
        #move the player based on key inputs 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3,0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3,0)
            elif event.key == pygame.K_UP:
                player.changespeed(0,-3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0,3)

            # Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, 3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -3)


    #makes sure that there are always [num_tree] trees on screen
    while len(tree_list) < num_tree :
        tree = Obstacles((random.randrange(screen_width),random.randrange(-100,-10)))
        tree.image = pygame.image.load("images/tree_sprite.png").convert()
        tree.image.set_colorkey(WHITE)
        tree_counter += 1 
        if tree_counter == num_tree: #if there are the max number of trees, 
            tree_counter = 0         #no more are added
        if not len(tree_list.sprites()) == max_trees:
            if tree_counter == num_tree - 1: #if there are less than the max number of trees,
                tree_list.add(tree)          #add trees until the max are reached
                obstacle_list.add(tree)
                all_sprites_list.add(tree)
                
    ##makes sure that there are always [num_spike] spikes on screen
    while len(spike_list) < num_spike :
        spikes = Obstacles((random.randrange(screen_width),random.randrange(-100,-10)))
        spikes.image = pygame.image.load("images/spikes.png").convert()
        spikes.image.set_colorkey(WHITE)
        spike_counter += 1
        if spike_counter == num_spike: #if there are the max number of spikes, 
            spike_counter = 0          #no more are added
        if not len(spike_list.sprites()) == max_spikes:
            if spike_counter == num_spike - 1: #if there are less than the max number of spikes,
                spike_list.add(spikes)         #add spikes until the max are reached
                obstacle_list.add(spikes)
                all_sprites_list.add(spikes)
                
    #check tsunami collisons 
    for t in tsunami_list:
        for p in player_list: #if player collides with tsunami
            if player.rect.colliderect(t.rect):
                player.rect.bottom = tsunami.rect.top
                youLose()     #call game over screen                 
                raise SystemExit()
            

    
    # Clear the screen
    screen.fill(SAND)

    #call update() method for every sprite 
    all_sprites_list.update()
    explosion_list.update()
    healthbar_list.update()
 
    

    #see if player has collected any powerups
    p_hit_list = pygame.sprite.spritecollide(player, powerup_list, False)

    #check list of collisions
    for ip in p_hit_list: #if the player collects a powerup, its position is reset
        ip.reset_pos()
 


    #---------- drawing code ------------------------------------------------------------

    #draw all lists to screen 
    tree_list.draw(screen)
    spike_list.draw(screen)
    obstacle_list.draw(screen)
    powerup_list.draw(screen)
    explosion_list.draw(screen)
    healthbar_list.draw(screen)

    #draws player and tsunami to screen     
    screen.blit(player.image, [player.rect.x, player.rect.y])        
    screen.blit(tsunami.image,[tsunami.rect.x,tsunami.rect.y])

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)
    
#be IDLE friendly!  
pygame.quit()
