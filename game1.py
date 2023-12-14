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

epsilon = 0.1; #this is the epsilon value that we will use to check for collisions.
class GameObject: #the ultimate class for all objects to derive from
    all_gameObjects = [];
    def __init__(self, x, y, width, height, id = None):
        GameObject.all_gameObjects.append(self);
        self.pos = np.array([x, y]); #this is the position of the object in the world.
        self.x = x #this corresponds to the center of the square, NOT the top left corner
        self.y = y #this corresponds to the center of the square, NOT the top left corner
        self.pixel_x = round(x); 
        self.pixel_y = round(y);
        self.width = width
        self.height = height
        self.halfheight = height/2;
        self.halfwidth = width/2;
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = np.array([0, 0]); #this is a vector that represents the velocity of the square.
        self.isCamera = False; #this is a boolean that determines whether or not the object is the camera.
        self.collision_layer_mask = 255;
        self.collision_layer = 1; #default collision layer. Each layer is an 8 bit value with 1 bit set to 1.
        self.elasticity = 1; # 1 means perfectly elastic, 0 means perfectly inelastic. 
        self.isStatic = True; #if this is true then the object will not move at all.
        #The velocity is measured in Pixels/Second.
        self.hidden = False; #if this is true then the object will not be drawn on the screen.
        if(id == None):
            self.id = len(GameObject.all_gameObjects);
        else:
            self.id = id;
    def update(self, dt):
        if(not self.isStatic):
            self.y += (self.velocity[1] * dt)/1000; 
            self.x += (self.velocity[0] * dt)/1000;
            self.pos = np.array([self.x, self.y]);
            self.collision_all(GameObject.all_gameObjects); 
        if(not self.hidden): 
            self.draw(screen); 
    
    def draw(self, screen = screen):
        pass;

    def set_velocity(self, v):
        self.velocity = v;
    def set_velocity(self, x, y):
        self.velocity[0] = x;
        self.velocity[1] = y;

    def y_collision_rect(self, other):
        #here other is also a gameobject. what we need to do is consider their positions as well as their sizes.
        #check for top collision.
        if(self.x + self.halfwidth + epsilon <= other.x - other.halfwidth or self.x - self.halfwidth - epsilon >= other.x + other.halfwidth):
            return 0; #not even in same x ranges brother. cannot collide like this.
        #otherwise it is possible for them to collide.
        #then we check which is on the top.
        if(self.y >= other.y):
            if(self.y - self.halfheight <= other.y + other.halfheight):
                return self.y - self.halfheight - other.y - other.halfheight; #-1 stands for bottom collision (for us).
            else:
                return 0;
        else:
            if(self.y + self.halfheight >= other.y - other.halfheight):
                return self.y + self.halfheight - other.y + other.halfheight; #1 stands for top collision (for us). 
            else:
                return 0;
    def x_collsion_rect(self,other):
        #here other is also a gameobject. what we need to do is consider their positions as well as their sizes.
        #check for top collision.
        if(self.y + self.halfheight + epsilon<= other.y - other.halfheight or self.y - self.halfheight - epsilon >= other.y + other.halfheight):
            return 0;
        #otherwise it is possible for them to collide.
        #then we check which is on the left.
        if(self.x >= other.x):
            if(self.x - self.halfwidth <= other.x + other.halfwidth):
                return self.x - self.halfwidth - other.x - other.halfwidth; #left collision.
            else:
                return 0;
        else:
            if(self.x + self.halfwidth >= other.x - other.halfwidth):
                return self.x + self.halfwidth - other.x + other.halfwidth; #right collilsion.
            else:
                return 0;

    def get_collision(self, other):
        #here other is also a gameobject. what we need to do is consider their positions as well as their sizes.
        #check for top collision.
        ycol = self.y_collision_rect(other);
        xcol = self.x_collsion_rect(other);
        return (xcol, ycol);
        
    def collision(self, other):
        #to handle the collisions what we will do IS.
        if(self.isStatic):
            return False; #no collision for static objects.
        if(self.isCamera):
            return False; #do literally nothing, as cameras don't collide.
        if(other.isCamera):
            return False; #do nothing here as well, cause we don't collide with camera objects.
        if((self.collision_layer_mask & other.collision_layer) == 0):
            return False;
        xcol,ycol = self.get_collision(other);
        if(xcol == 0 and ycol == 0):
            return False; #no collision.
        #otherwise if a collision does happen, then what we want to do is to reverse the direction of the velocity in that direction.
        if(abs(abs(xcol) - abs(ycol)) < epsilon):
           pass;
        else:
            if(abs(xcol) >=  abs(ycol)):
                print(xcol, ycol)
                xcol = 0;
            else:
                ycol = 0;
        if(xcol != 0):
            print("X Collision between ",self.id, " and ", other.id);  
            self.velocity[0] = -self.velocity[0] * self.elasticity;
        if(ycol != 0):
            print("Y Collision between ",self.id, " and ", other.id);  
            self.velocity[1] = -self.velocity[1] * self.elasticity;
    
    def collision_all(self, others):
        if(self.isCamera):
            return False; #do nothing here as well, cause we don't collide with camera objects.
        for other in others:
            if(other.id == self.id):
                continue;
            self.collision(other); 

class Camera(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height);
        self.isCamera = True;
        self.collision_layer = 0; #the camera is on the 0th layer, so it doesn't collide with anything at all.
        self.collision_layer_mask = 0; #the camera is on the 0th layer, so it doesn't collide with anything at all.
        self.hidden = True;
    def get_screen_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height);
    
    def set_position(self, x, y):
        self.x = x;
        self.y = y;
    
#    def pad_reposition(self, rect:pygame.rect):
        #if the rect is going out of bounds then we shall move the camera as well, with some lerp attached to it.


main_camera = Camera(0, 0, screen_width, screen_height); #the one camera that the game will use to render objects on the screen.
main_camera.hidden = True;
class Square(GameObject):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height);
        self.color = color;

    def get_rect(self):
        self.pixel_x = round(self.x)
        self.pixel_y = round(self.y)
        screenpos_x = round(self.x - main_camera.x - self.halfwidth); 
        screenpos_y = round(self.y - main_camera.y - self.halfheight); 
        self.rect = pygame.Rect(screenpos_x, screenpos_y, self.width, self.height)
        return self.rect

    def draw(self, screen = screen):
        pygame.draw.rect(screen, self.color, self.get_rect());

    def rect_collision(self, other:GameObject):
        return self.get_rect().colliderect(other.get_rect());
    def rect_collision(self, other:pygame.Rect):
        return self.get_rect().colliderect(other);

player_square = Square(0, 0, 100, 100, (0, 250, 210))
player_square.velocity = np.array([100, 100]);
player_square.isStatic = False; #is a dynamic object and responds to collisions.

bouncers = [];
bouncers.append(Square(500, 500, 100, 50, (240, 0, 0)));
bouncers.append(Square(100, 700, 900, 100, (240, 0, 0)));
prev_time = pygame.time.get_ticks();
print(prev_time)
while True:
    clock.tick(framerate) #sets framerate to 60 fps
    screen.fill(0) #fills screen with black
    #player_square.draw(screen)
    # bouncers[0].draw(screen);
    curtime = pygame.time.get_ticks();
    dt = curtime - prev_time;
    for obj in GameObject.all_gameObjects:
        obj.update(dt); #we run the update function for all our gameobjects. ALTHOUGH we should probably do this only for the main player.
    prev_time = pygame.time.get_ticks();
    pygame.display.flip(); 

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print("exiting pygame");
            sys.exit()
    

