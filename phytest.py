# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 16:52:10 2024

@author: Mikko
"""


# Import the pygame module
import pygame
import random
import math

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

kimmokerroin = 0.9

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()

gravity = 1
# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = pygame.image.load("arrow2.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.originalsurf = self.surf
        self.rect = self.surf.get_rect(center = (500, 400))
        
        #Forces effecting to piece
        self.thrust = 0 #thrust of rotating motors
        self.kitka = 0.1 #Kitka, joka hidastaa kappaletta
        self.gravity = (0, 0.1) #Vetovoima
        self.throttle = 0 #Keskimoottorin aiheuttama thrust
        self.spd = 0  #nopeuden magnitudi
        self.spd_vect = (0,0) #Nopeusvektori (lasketaan kiihtyvyyksistä)
 #       self.direction = 30 #Suuntavektorin kulma
        self.acc = (0, 0)  #Kokonaiskiihtyvyys
    
 #       self.kimmokerroin = 0.9
  #      self.kitka = 0.001
        self.inthegame = True
        self.angle = 0
        self.rot = 0
   
        
        
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
    
        
        
        
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):

        pressed = False
        if pressed_keys[K_LEFT]:
            self.thrust = 0.2
            self.rot = 5
         #   self.spd += self.acc
            pressed = True
        if pressed_keys[K_RIGHT]:
            self.thrust = 0.2
            self.rot = -5
           # self.spd += self.acc
            pressed = True
        if pressed_keys[K_UP]:
            self.throttle = 0.1
            pressed = True
        if pressed == False:
            self.rot = 0
            self.throttle = 0
            self.thrust = 0
            self.spd -= self.kitka
            if self.spd < 0:
                self.spd = 0
            
        if pressed == True:
             self.spd = self.spd + self.throttle
             self.spd_vect = self.calculate_movement(self.angle, self.spd, self.thrust, self.throttle)
            
        # if self.spd > 10:
        #     self.spd = 10
        # if self.spd < 0:
        #     self.spd = 0
        #     self.acc = 0
        # if self.rot > 5:
        #     self.rot = 5
        # if self.rot < -5:
        #     self.rot = -5
        if self.rot != 0:
            self.angle += self.rot
            self.rotate(self.angle)

       
        
     #   if self.rect.center[0]> SCREEN_WIDTH:
      #      self.spdx = -self.spdx
        
      #  if self.rect.center[0] < 0:
      #      self.inthegame = False
            
      #  if self.rect.center[1] > SCREEN_HEIGHT or self.rect.center[1] < 0:
      #      self.spdy = -self.spdy
           
       # self.acc = self.calculate_accelerations(self.angle, self.thrust, self.throttle)
        
        
       # self.spd = self.spd_vect[0]*self.spd_vect[0] + self.spd_vect[1]*self.spd_vect[1]
        print(self.spd)
        print (self.spd_vect)
        
        self.rect.move_ip(self.spd_vect)
       
        
        


# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 100))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(10, 400))
        self.spd = 0
     
        
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        
        if pressed_keys[K_UP]:
            self.spd = -5
        elif pressed_keys[K_DOWN]:
            self.spd = 5
        else:
            self.spd = 0
        self.rect.move_ip(0,self.spd)
            
        if self.rect.top < 0:
            self.rect.top = 0
            
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        




ball = Ball()
player = Player()
running = True
all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
players = pygame.sprite.Group()
balls.add(ball)
players.add(player)
all_sprites.add(ball)
all_sprites.add(player)

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
                
        # Did the user click the window close button? If so, stop the loop.
        if event.type == QUIT:
            running = False
            
 
        
    # Fill the screen with white
    screen.fill((135, 206, 250))  
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    ball.update(pressed_keys)
    
    
    # pelaaja = pygame.sprite.spritecollideany(ball, players)
    # if pelaaja:
    #     ball.spdx = -ball.spdx
    #     ball.spdy = ball.spdy + pelaaja.spd
    

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

          
pygame.quit()