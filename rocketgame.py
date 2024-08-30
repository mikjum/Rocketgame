# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 16:52:10 2024

@author: Mikko
"""
# Comment here to indicate that we are in new branch

# Import the pygame module
import pygame
import gameobjects
import physics
import pyautogui


# Initialize pygame
pygame.init()
# Setup the clock for a decent framerate
clock = pygame.time.Clock()

from pygame.locals import (
    QUIT
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750

font = pygame.font.Font('freesansbold.ttf', 32)


# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()


#Function to generate level consisting level objects defined in levels-file
def generate_level(file, levelnumber):
    lines = file.readlines()
    level = lines[levelnumber*15 : levelnumber*15 + 15]
    ylocation = 25
    startingpoint = (400, 600)
    for line in level:
        xlocation = 25
        for marker in line:
            
            if marker == 'C' or marker == 'L' or marker == 'R' or marker == 'F':
                tile = gameobjects.Wall((xlocation, ylocation))
                tilebottom = gameobjects.TileEdge(xlocation-20, ylocation+25, 40, 3)
                ceiling.add(tilebottom)
                tileright = gameobjects.TileEdge(xlocation+25, ylocation-20, 3, 40)
                leftwall.add(tileright)
                tileleft = gameobjects.TileEdge(xlocation-25, ylocation-20, 3, 40)
                rightwall.add(tileleft)
                tiletop = gameobjects.TileEdge(xlocation-20, ylocation-25, 40, 3)
                floors.add(tiletop)
                walls.add(tile)
                all_sprites.add(tile)
 
            if marker == 'G':         
            
                tile = gameobjects.Goal((xlocation+75, ylocation))
                all_sprites.add(tile)
                goals.add(tile)
                floors.add(tile)
 
            if marker == 'S':
                startingpoint = (xlocation, ylocation-50)
            xlocation += 50
        ylocation += 50
    return startingpoint



# Setting up sprite groups
#Left-right-up-down walls are required workaround to understand how rocket collided
all_sprites = pygame.sprite.Group()

leftwall = pygame.sprite.Group()
rightwall = pygame.sprite.Group()
floors = pygame.sprite.Group()
ceiling = pygame.sprite.Group()
goals = pygame.sprite.Group()
walls = pygame.sprite.Group()



#Initial game parameters
lives = 3
level = 1
success = False
endgame = False


started = False

#Splash screen
bg = gameobjects.Background("graphics/backgroundold.png", [0,0])
textstr = "Welcome to Rocket Game!"
text = font.render(textstr, True, (0,255,0))
textRect = text.get_rect()
textRect.center = (500, 350)
helptext = "Use Arrow keys to play. Land rocket slowly and straight"
helpbox = font.render(helptext, True, (255,255,255))
helpRect = helpbox.get_rect()
helpRect.center = (500, 600)
button_surface = pygame.Surface((200, 50))
buttontext = font.render("Start Game", True, (255, 0, 0))
text_rect = buttontext.get_rect(center=(button_surface.get_width()/2, button_surface.get_height()/2))
button_rect = pygame.Rect(400, 400, 200, 50)

#Loop polling splash screen to continue and drawing the splash screen
while started==False: 
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        # Call the on_mouse_button_down() function
            if button_rect.collidepoint(event.pos):
                
                started = True
        if event.type == QUIT:
            pygame.quit()
         #   file.close()
           
    # Shwo the button text
    button_surface.blit(buttontext, text_rect)

      # Draw the button on the screen
    screen.blit(button_surface, (button_rect.x, button_rect.y))

      # Update the game state
    pygame.display.update()
    screen.blit(bg.image, bg.rect)
    screen.blit(text, textRect)  
    screen.blit(helpbox, helpRect)


#Loop run as long as plauer is alive
while lives > 0:


    try:
        file = open('files/Levels.txt')
    except:
        pyautogui.alert("Could not open levels.txt")
        pygame.quit()
    spoint = generate_level(file,level)
    file.close()
    print (spoint)
    rocket = gameobjects.Rocket(spoint)
    all_sprites.add(rocket)
    bg = gameobjects.Background("graphics/background.png", [0,0])
    running = True
    # Main loop running within current live and current level
    while running:
        textstr = "Rockets: " + str(lives) + "  Level: " + str(level)
       
        text = font.render(textstr, True, (0,255,0))
        textRect = text.get_rect()
        textRect.center = (160, 25)
        
        
        
        screen.fill([255, 255, 255])
        screen.blit(bg.image, bg.rect)
        
        # Look at every event in the queue
        for event in pygame.event.get():
    
            # Did the user click the window close button? If so, stop the game.
            if event.type == QUIT:
                pygame.quit()
               # file.close()
    
        # Was there a key pressed?
        pressed_keys = pygame.key.get_pressed()

        #Update the game object and take pressed keys into account
        rocket.update(pressed_keys)
        
        #In case of hitting the goal (If rocket was not already exploded)
        if pygame.sprite.spritecollideany(rocket, goals) and rocket.explode == False:
            # With too high speed, the rocket will start explosion process
            if rocket.spd_vect[1] > 4:
                rocket.explosion()
            # It is also fatal if your rocket was too tilted during the landing    
            elif rocket.angle > 10 and rocket.angle < 350:
                running = False
                success = False
            
                # Othervice: "GREAT SUCCESS!"
            else:
            
                running=False
                success = True
        # In case of explosion, when the explosion process is done, end the loop        
        if rocket.crashed == True:
            running =False
            success = False
            
        #In case of wall collsion, consequences depend on the direction of collision
        # To Do: More sophisticated collisions (Bouncing, exploding etc)
        collided_wall = pygame.sprite.spritecollideany(rocket, floors)   
 
 
        
        if pygame.sprite.spritecollideany(rocket, floors) and rocket.spd_vect[1] > 0:
            
            rocket.spd_vect[1] = 0
        if pygame.sprite.spritecollideany(rocket, leftwall) and rocket.spd_vect[0] < 0:
            rocket.spd_vect[0] = 0
        if pygame.sprite.spritecollideany(rocket, rightwall) and rocket.spd_vect[0] > 0:
            rocket.spd_vect[0] = 0
            rocket.spd = physics.update_speed(rocket.spd_vect, rocket.acc)
        if pygame.sprite.spritecollideany(rocket, ceiling) and rocket.spd_vect[1] < 0:
            rocket.spd_vect[1] = 0
        
    
       # Draw the items on the screen
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        screen.blit(text, textRect)   
       

        pygame.display.flip()
        # Ensure program maintains a rate of 30 frames per second
        clock.tick(30)
        
        #END While running
    
    #When level ws succesfully completed    
    if success == True:
        pyautogui.alert("Congratulations! You managed to get next level")
        level+=1
        for sps in all_sprites:
            sps.kill()
    #And if it was not so succesfull
    else:
        
        lives -= 1
        rocket.kill()
        pyautogui.alert("Your Rocket destroyed!")
    print (lives)

# when lives == 0            
pygame.quit()