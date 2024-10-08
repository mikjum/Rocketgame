# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 15:00:42 2024

@author: Mikko
"""
import pygame
import physics
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_LEFT,
    K_RIGHT

)

# Array of images used in explosion process
explosion_images = [pygame.image.load(f'graphics/rocket{i}.png') for i in range(3, 13)]

#Invisible sprite to tile edges. The side of the tile is determined by sprite group of the edge
class TileEdge(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height):
        super(TileEdge, self).__init__()
        self.rect = pygame.Rect(left, top, width, height)
       # self.rect.centerpoint = centerpoint
    


# Sprite for the background image
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        try:
            self.image = pygame.image.load(image_file)
            self.rect = self.image.get_rect()
            self.rect.left, self.rect.top = location
        except:
            self.surf = pygame.Surface((1000, 700))
            self.surf.fill((0, 0, 0))  
            self.rect = self.surf.get_rect()
            self.rect.left, self.rect.top = location
            self.image = self.surf
            
        
        
 # Wall tile sprite
class Wall(pygame.sprite.Sprite):
    def __init__(self, centerpoint):
        super(Wall, self).__init__()
        self.surf = pygame.image.load("graphics/tile.png").convert()
        #self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        #self.surf = pygame.Surface((50,50))
       #self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center = centerpoint)
        
# Goal sprite       
class Goal(pygame.sprite.Sprite):
    def __init__(self, centerpoint):
        super(Goal, self).__init__()
        self.surf = pygame.image.load("graphics/landingpad2.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
   
        self.rect = self.surf.get_rect(center = centerpoint)
        
        
        
#Player sprite
class Rocket(pygame.sprite.Sprite):
    def __init__(self, startingpoint):
        super(Rocket, self).__init__()
        try:
            self.surf = pygame.image.load("graphics/rocket2.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        except:
            print("Could not open image file rocket2.png")
       
            self.surf = pygame.Surface((70, 100))
            self.surf.fill((255, 255, 255))
        
        self.originalsurf = self.surf
        self.rect = self.surf.get_rect(center = startingpoint)
        
        #Forces effecting to piece
        self.thrust = 0 #thrust of rotating motors
        self.gravity = [0, 0.1] #Gravity force vector
        self.throttle = 0 #Force generated by main engine
        self.spd = 0  #Magnitude of the speed
        self.spd_vect = [0,0] #Speed vector
        self.acc = [0, 0]  #Acceleration vector
        self.angle = 0 #angle of the rocket
        self.rot = 0 #Angular rotation speed of the rocket
        self.explode = False # Just to understand if the rocket has exploded
        self.explosionIndex = 0 #Number of frame in explosion process
    
    
        self.crashed = False       
        
    
    # Function to transform Rocket graphics according to the angle of rocket
    def rotate(self, angle):
        
        if self.explode == False:
            
            self.surf = pygame.transform.rotate(self.originalsurf, self.angle)
        self.rect = self.surf.get_rect(center = self.rect.center)
       

    
    # In case of explosion, set the flag  
    def explosion(self):
        self.explode = True
        
    # Update function for the object.
    def update(self, pressed_keys):
        
        #If explosion flag is on, run the explosion process
        if self.explode == True:
            self.surf=explosion_images[self.explosionIndex].convert()
            self.explosionIndex += 1
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rotate(self.angle)
            if self.explosionIndex == len(explosion_images):
                self.explosionIndex = 0
                self.crashed = True
        
        # setting the forces according to the user commands
        pressed = False
        if pressed_keys[K_LEFT]:
            self.thrust = 0.2
            self.rot = 5
            pressed = True
        if pressed_keys[K_RIGHT]:
            self.thrust = 0.2
            self.rot = -5
            pressed = True
        if pressed_keys[K_UP]:
            self.throttle = 0.2
            pressed = True
        
        #When no key is pressed, forces shall go zero
        if pressed == False:
            self.rot = 0
            self.throttle = 0
            self.thrust = 0

        #Calculate accelerations based on forces  
        
        #The trust force
        self.acc = physics.introduce_force(self.angle, self.thrust, self.throttle)
        #The gravity force
        self.acc = physics.introduce_external_force(self.acc, self.gravity)
        
    
        #Update speed according accelerations
        self.spd = physics.update_speed(self.spd_vect, self.acc)
   
        
        #Update rotation angle based on the user controls, also keep the angle between 0 and 360
        if self.rot != 0:
            self.angle += self.rot
            self.rotate(self.angle)
            if self.angle > 360:
                self.angle -= 360
            if self.angle < 0:
                self.angle += 360

        #Update object location
        self.rect.move_ip(self.spd_vect)
        