# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 15:00:42 2024

@author: Mikko
"""
import pygame
import physics
import math
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

explosion_images = [pygame.image.load(f'rocket{i}.png') for i in range(3, 13)]

#Invisible sprite to top of all tiles to indicate collsion from top
class TileEdge(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height):
        super(TileEdge, self).__init__()
        self.rect = pygame.Rect(left, top, width, height)
       # self.rect.centerpoint = centerpoint
    



class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Wall(pygame.sprite.Sprite):
    def __init__(self, centerpoint):
        super(Wall, self).__init__()
        self.surf = pygame.image.load("tile.png").convert()
        #self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        #self.surf = pygame.Surface((50,50))
       #self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center = centerpoint)
        
        
class Goal(pygame.sprite.Sprite):
    def __init__(self, centerpoint):
        super(Goal, self).__init__()
        self.surf = pygame.image.load("landingpad2.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
   
        self.rect = self.surf.get_rect(center = centerpoint)
        
        
        
# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Rocket(pygame.sprite.Sprite):
    def __init__(self, startingpoint):
        super(Rocket, self).__init__()
        self.surf = pygame.image.load("rocket2.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.originalsurf = self.surf
        self.rect = self.surf.get_rect(center = startingpoint)
        
        #Forces effecting to piece
        self.thrust = 0 #thrust of rotating motors
        self.kitka = 0.1 #Kitka, joka hidastaa kappaletta
        self.gravity = [0, 0.1] #Vetovoima
        self.throttle = 0 #Keskimoottorin aiheuttama thrust
        self.spd = 0  #nopeuden magnitudi
        self.spd_vect = [0,0] #Nopeusvektori (lasketaan kiihtyvyyksistä)
        self.friction = 0
        self.acc = [0, 0]  #Kokonaiskiihtyvyys
        self.angle = 0
        self.rot = 0
        self.explode = False
        self.explosionIndex = 0
    
        self.inthegame = True

        self.onthefloor = False
        self.crashed = False       
        
    def rotate(self, angle):
        self.surf = pygame.transform.rotate(self.originalsurf, self.angle)
        self.rect = self.surf.get_rect(center = self.rect.center)
       
    def calculate_accelerations(self, angle, thrust, throttle):
        total_acc = thrust + throttle

        accy = -total_acc * math.cos(math.radians(self.angle))  
        accx = -total_acc * math.sin(math.radians(self.angle))  
                 
        return accx, accy
    
    def calculate_movement(self, angle, spd, thrust, throttle):
    
     
        
        spdy = -spd * math.cos(math.radians(self.angle)) 
        spdx = -spd * math.sin(math.radians(self.angle)) 
        
        return spdx, spdy
    
        
    def explosion(self):
        self.explode = True
        
    # Update function for the object.
    def update(self, pressed_keys):
        if self.explode == True:
            self.surf=explosion_images[self.explosionIndex].convert()
            self.explosionIndex += 1
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            
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
        if pressed == False:
            self.rot = 0
            self.throttle = 0
            self.thrust = 0

        #Calculate accelerations based on forces    
        self.acc = physics.introduce_force(self.angle, self.thrust, self.throttle)
        self.acc = physics.introduce_external_force(self.acc, self.gravity)
        

       
        #Update speed according accelerations
        self.spd = physics.update_speed(self.spd_vect, self.acc)
   
        
        #Update rotation angle based on the user controls
        if self.rot != 0:
            self.angle += self.rot
            self.rotate(self.angle)
            if self.angle > 360:
                self.angle -= 360
            if self.angle < 0:
                self.angle += 360

        #Update object location
        self.rect.move_ip(self.spd_vect)
        