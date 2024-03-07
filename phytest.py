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
    lines = file.readlines()
    level = lines[levelnumber*15 : levelnumber*15 + 15]
    ylocation = 25
    startingpoint = (400, 600)
    for line in level:
        xlocation = 25
        for marker in line:
            
            if marker == 'C' or marker == 'L' or marker == 'R' or marker == 'F' or marker == 'G':
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
                tile = gameobjects.Wall((xlocation, ylocation))
                goals.add(tile)
 
            if marker == 'S':
                startingpoint = (xlocation, ylocation-50)
            xlocation += 50
        ylocation += 50
    return startingpoint




goal = gameobjects.Goal((800, 675))


all_sprites = pygame.sprite.Group()

leftwall = pygame.sprite.Group()
rightwall = pygame.sprite.Group()
floors = pygame.sprite.Group()
ceiling = pygame.sprite.Group()
goals = pygame.sprite.Group()
walls = pygame.sprite.Group()

all_sprites.add(goal)

floors.add(goal)
goals.add(goal)


lives = 3
level = 0
success = False
endgame = False


# Function to detect collision edge
def detect_collision_edge(sprite_a, sprite_b):
   pass
    


#END of edgecollision

while lives > 0:

    #floor = []
    #wall = []
    file = open('levels.txt')
    spoint = generate_level(file,level)
    rocket = gameobjects.Rocket(spoint)
    all_sprites.add(rocket)
    bg = gameobjects.Background("background.png", [0,0])
    running = True
    # Main loop
    while running:
        textstr = "Rockets: " + str(lives) + "  Level: " + str(level)
        print(textstr)
        text = font.render(textstr, True, (0,255,0))
        textRect = text.get_rect()
        textRect.center = (160, 25)
        
        
        
        screen.fill([255, 255, 255])
        screen.blit(bg.image, bg.rect)
        # Look at every event in the queue
        for event in pygame.event.get():
                    
            # Did the user click the window close button? If so, stop the loop.
            if event.type == QUIT:
                running = False
                lives = 0
                
     
            
        # Fill the screen with white
       # screen.fill((135, 206, 250)) 
    
        pressed_keys = pygame.key.get_pressed()
        #player.update(pressed_keys)
        rocket.update(pressed_keys)
        
        if rocket.crashed == True:
            running = False
    
            
            
            
        if pygame.sprite.spritecollideany(rocket, goals):
            if rocket.spd_vect[1] > 3:
                succes = False
                running = False
               
            else:
               
                running=False
                success = True
                
        
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