import pygame
import random 
import time
import sys
from abc import ABC, abstractmethod
from pygame.locals import *



pygame.init()
 
FPS = 60
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1000
 
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

#Define the player class
# This class is used to create the player object

class GameObject(ABC, pygame.sprite.Sprite):
    def __init__(self, name, radius=10):
        self.name = name
        self.radius = radius

    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def draw(self, surface):
        pass

class Player(GameObject, pygame.sprite.Sprite):
    def __init__(self, speed=5):
        pygame.sprite.Sprite.__init__(self)
        GameObject.__init__(self, "Player")
        self.image = pygame.image.load("assets\car.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.88)
        self.speed = speed
   
    def update(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
         
        if self.rect.left >= 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)   

class Obstacle(GameObject, pygame.sprite.Sprite):
    def __init__(self, name, image, x=None, y=0, present=False, ticker=10):
        pygame.sprite.Sprite.__init__(self)
        self.x = x if x is not None else random.randint(20, SCREEN_WIDTH - 20)
        self.y = y
        self.name = name
        self.image = image
        self.rect = self.image.get_rect()
        self.present = present
        self.ticker = ticker

    def update(self,speed):
        if self.present:
            self.rect.move_ip(0, speed)
            if self.rect.top > SCREEN_HEIGHT:
                self.rect.bottom = 0
                self.present = False
                obstacles.remove(self)



    def draw(self, surface, speed):
        if self.present:
            surface.blit(self.image, self.rect)  
        else:
            if random.randint(0, 10) * speed >= self.ticker:
                self.present = True
            else:
                self.ticker -= 1
            

class tree(Obstacle):
    def __init__(self):
        image = pygame.image.load("assets/tree.png")
        super().__init__("tree", image)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


class cone(Obstacle):
    def __init__(self):
        image = pygame.image.load("assets/cone.png")
        super().__init__("cone", image)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

class rock(Obstacle):
    def __init__(self):
        image = pygame.image.load("assets/rock.png")
        super().__init__("rock", image)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)




player = Player()
obstacles = pygame.sprite.Group()


start_time = time.time()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if time.time() - start_time > player.speed:
        if player.speed < 10:
            player.speed += 1
    if len(obstacles) < player.speed:
        if random.randint(0, 50) * player.speed > 9:
            obstacles.add([tree(), cone(), rock()][random.randint(0, 2)])
    for obstacle in obstacles:
        obstacle.update(player.speed)
    player.update()
    DISPLAYSURF.fill(WHITE)
    for obstacle in obstacles:
        obstacle.draw(DISPLAYSURF, player.speed)
    player.draw(DISPLAYSURF)
    for obstacle in obstacles:
        if pygame.sprite.collide_circle(player, obstacle):
            DISPLAYSURF.fill(RED)
            pygame.display.update()
        if pygame.sprite.collide_circle(player, obstacle):
            DISPLAYSURF.fill(RED)
            sys.exit()
    pygame.display.update()
    FramePerSec.tick(FPS)


    