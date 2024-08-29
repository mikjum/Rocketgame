# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 16:52:10 2024

@author: Mikko
"""
# Comment here to indicate that we are in new branch

# Import the pygame module
import pygame
import random
import math
import gameobjects
import physics
import pyautogui


# Initialize pygame
pygame.init()
# Setup the clock for a decent framerate
clock = pygame.time.Clock()

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    K_SPACE,
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


def generate_level(file, levelnumber):
    print("Generating Level")
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




#goal = gameobjects.Goal((800, 675))


all_sprites = pygame.sprite.Group()

leftwall = pygame.sprite.Group()
rightwall = pygame.sprite.Group()
floors = pygame.sprite.Group()
ceiling = pygame.sprite.Group()
goals = pygame.sprite.Group()
walls = pygame.sprite.Group()

#all_sprites.add(goal)

#floors.add(goal)
#goals.add(goal)


lives = 3
level = 2
success = False
endgame = False


started = False
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

while lives > 0:

    #floor = []
    #wall = []
    try:
        file = open('Levels.txt')
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
    # Main loop
    while running:
        textstr = "Rockets: " + str(lives) + "  Level: " + str(level)
        #print(textstr)
        text = font.render(textstr, True, (0,255,0))
        textRect = text.get_rect()
        textRect.center = (160, 25)
        
        
        
        screen.fill([255, 255, 255])
        screen.blit(bg.image, bg.rect)
        # Look at every event in the queue
        for event in pygame.event.get():
                    
            # Did the user click the window close button? If so, stop the loop.
            if event.type == QUIT:
                pygame.quit()
               # file.close()
                
     
            
        # Fill the screen with white
       # screen.fill((135, 206, 250)) 
    
        pressed_keys = pygame.key.get_pressed()
        #player.update(pressed_keys)
        rocket.update(pressed_keys)
        
        # if rocket.crashed == True:
        #     running = False
    
            
            
            
        if pygame.sprite.spritecollideany(rocket, goals) and rocket.explode == False:
            if rocket.spd_vect[1] > 4:
                rocket.explosion()
                # succes = False
                # running = False
            elif rocket.angle > 10 and rocket.angle < 350:
                running = False
                success = False
               
            else:
            #    if rocket.explode == False:
                print("tääwwä")
                running=False
                success = True
                
        if rocket.crashed == True:
            running =False
            success = False
        collided_wall = pygame.sprite.spritecollideany(rocket, floors)   
        if collided_wall:
            pass
           # print (detect_collision_edge(rocket, collided_wall))
        
        if pygame.sprite.spritecollideany(rocket, floors) and rocket.spd_vect[1] > 0:
            
            rocket.spd_vect[1] = 0
        if pygame.sprite.spritecollideany(rocket, leftwall) and rocket.spd_vect[0] < 0:
            rocket.spd_vect[0] = 0
        if pygame.sprite.spritecollideany(rocket, rightwall) and rocket.spd_vect[0] > 0:
            rocket.spd_vect[0] = 0
            rocket.spd = physics.update_speed(rocket.spd_vect, rocket.acc)
        if pygame.sprite.spritecollideany(rocket, ceiling) and rocket.spd_vect[1] < 0:
            rocket.spd_vect[1] = 0
        
    
       # Draw the player on the screen
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        screen.blit(text, textRect)   
       
        # If so, then remove the player and stop the loop
         #   ball.spdx = -ball.spdx
            #running = False
       # for pallo in balls:
          #  if pallo.inthegame == False:
           #     running = False
        pygame.display.flip()
        # Ensure program maintains a rate of 30 frames per second
        clock.tick(30)
        
        #END While running
        
    if success == True:
        pyautogui.alert("Congratulations! You managed to get next level")
        level+=1
        for sps in all_sprites:
            sps.kill()
    else:
        
        lives -= 1
        rocket.kill()
        pyautogui.alert("Your Rocket destroyed!")
    print (lives)

          
pygame.quit()