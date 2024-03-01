# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 16:52:10 2024

@author: Mikko
"""


# Import the pygame module
import pygame
import random
import math
import gameobjects
import physics

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
            
            if marker == 'C':
                tile = gameobjects.Wall((xlocation, ylocation))
                ceiling.add(tile)
                walls.add(tile)
                all_sprites.add(tile)
            if marker == 'L':
                tile = gameobjects.Wall((xlocation, ylocation))
                leftwall.add(tile)
                walls.add(tile)
                all_sprites.add(tile)
            if marker == 'R':
                tile = gameobjects.Wall((xlocation, ylocation))
                rightwall.add(tile)
                walls.add(tile)
                all_sprites.add(tile)
            if marker == 'F':
                tile = gameobjects.Wall((xlocation, ylocation))
                floors.add(tile)
                walls.add(tile)
                all_sprites.add(tile)
            if marker == 'G':
                tile = gameobjects.Wall((xlocation, ylocation))
                floors.add(tile)
                walls.add(tile)
                goals.add(tile)
                all_sprites.add(tile)
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
    # print ("right -left", sprite_a.rect.right - sprite_b.rect.left)
    # print ("right -top", sprite_a.rect.right - sprite_b.rect.top)
    # print ("right -right", sprite_a.rect.right - sprite_b.rect.right)
    # print ("right -bottom", sprite_a.rect.right - sprite_b.rect.bottom)
   
    # print ("bottom -left", sprite_a.rect.bottom - sprite_b.rect.left)
    # print ("bottom -top", sprite_a.rect.bottom - sprite_b.rect.top)
    # print ("bottom -right", sprite_a.rect.bottom - sprite_b.rect.right)
    # print ("bottom -bottom", sprite_a.rect.bottom - sprite_b.rect.bottom) 

    # print ("left -left", sprite_a.rect.left - sprite_b.rect.left)
    # print ("left -top", sprite_a.rect.left - sprite_b.rect.top)
    # print ("left -right", sprite_a.rect.left - sprite_b.rect.right)
    # print ("left -bottom", sprite_a.rect.left - sprite_b.rect.bottom) 
    
    # print ("top -left", sprite_a.rect.top - sprite_b.rect.left)
    # print ("top -top", sprite_a.rect.top - sprite_b.rect.top)
    # print ("top -right", sprite_a.rect.top - sprite_b.rect.right)
    # print ("top -bottom", sprite_a.rect.top - sprite_b.rect.bottom) 
    distance_to_top = min(abs(sprite_a.rect.right - sprite_b.rect.top), abs(sprite_a.rect.bottom - sprite_b.rect.top), abs(sprite_a.rect.left - sprite_b.rect.top), abs(sprite_a.rect.top - sprite_b.rect.top))
    distance_to_right = min(abs(sprite_a.rect.right - sprite_b.rect.right), abs(sprite_a.rect.bottom - sprite_b.rect.right), abs(sprite_a.rect.left - sprite_b.rect.right), abs(sprite_a.rect.top - sprite_b.rect.right))
    distance_to_bottom = min(abs(sprite_a.rect.right - sprite_b.rect.bottom), abs(sprite_a.rect.bottom - sprite_b.rect.bottom), abs(sprite_a.rect.left - sprite_b.rect.bottom), abs(sprite_a.rect.top - sprite_b.rect.bottom))
    distance_to_left = min(abs(sprite_a.rect.right - sprite_b.rect.left), abs(sprite_a.rect.bottom - sprite_b.rect.left), abs(sprite_a.rect.left - sprite_b.rect.left), abs(sprite_a.rect.top - sprite_b.rect.left))
    
    
    
    print ("Distance to top ", distance_to_top)
    print ("Distance to right ", distance_to_right)
    print ("Distance to bottom ", distance_to_bottom)
    print ("Distance to left ", distance_to_left)
    
    
       
      
    
    


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
                
        
        collided_wall = pygame.sprite.spritecollideany(rocket, walls)   
        if collided_wall:
            print (detect_collision_edge(rocket, collided_wall))
        
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
        level+=1
        for sps in all_sprites:
            sps.kill()
    else:
        
        lives -= 1
        rocket.kill()
    print (lives)

          
pygame.quit()