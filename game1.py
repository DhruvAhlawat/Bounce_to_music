import pygame
import sys
import os
import numpy as np;
from pygame.locals import *
pygame.init() #initializes pygame
clock = pygame.time.Clock()
screen_width = 720; 
screen_height = 720;
screen = pygame.display.set_mode((screen_width, screen_height)) #creates screen
pygame.mouse.set_visible(0);
bg = pygame.image.load("./images/bubble2_large.jpg") #loads background image
framerate = 60; #sets framerate to 60 fps


class GameObject: #the ultimate class for all objects to derive from
    def __init__(self, x, y, width, height):
        self.x = x #this corresponds to the center of the square, NOT the top left corner
        self.y = y #this corresponds to the center of the square, NOT the top left corner
        self.pixel_x = round(x); 
        self.pixel_y = round(y);
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = np.array([0, 0]); #this is a vector that represents the velocity of the square.
        self.isCamera = False; #this is a boolean that determines whether or not the object is the camera.
        #The velocity is measured in Pixels/Second.

    def update(self, dt):
        self.x += (self.velocity[0] * dt)/1000;
        self.y += (self.velocity[1] * dt)/1000; 
    
    def set_velocity(self, v):
        self.velocity = v;
    def set_velocity(self, x, y):
        self.velocity[0] = x;
        self.velocity[1] = y;

class Camera(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height);
        self.isCamera = True;

main_camera = Camera(0, 0, screen_width, screen_height); #the one camera that the game will use to render objects on the screen.


class Square(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height);
        self.color = color;

    def get_rect(self):
        self.pixel_x = round(self.x)
        self.pixel_y = round(self.y)
        screenpos_x = round(self.x - main_camera.x - self.width/2); 
        screenpos_y = round(self.y - main_camera.y - self.height/2); 
        self.rect = pygame.Rect(screenpos_x, screenpos_y, self.width, self.height)
        return self.rect

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect());


player_square = Square(0, 0, 100, 100, (0, 250, 210))
player_square.velocity = np.array([100, 100]);
prev_time = pygame.time.get_ticks();
print(prev_time)
while True:
    clock.tick(framerate) #sets framerate to 60 fps
    screen.fill(0) #fills screen with black
    player_square.draw(screen)
    pygame.display.flip(); 
    curtime = pygame.time.get_ticks();
    dt = curtime - prev_time;
    player_square.update(dt); 
    prev_time = pygame.time.get_ticks();
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print("exiting pygame");
            sys.exit()
    

