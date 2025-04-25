import pygame
import random 
import time
import sys
from abc import ABC, abstractmethod
from pygame.locals import *


name = input("Please enter your name: ")
if name == "":
    print("No name entered, using default name: Player")
    name = "Player"

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
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900\

font = pygame.font.SysFont(None, 30)

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
    
    def save_score(self,score,name):
        with open("scores.txt", "a+") as f:
            f.seek(0)  # Move to the start of the file to read existing scores
            lines = f.readlines()
            f.write(f"{name}: {score}\n")
            print("Score saved!")
            lines.append(f"{name}: {score}\n")
            lines.sort(key=lambda x: int(x.split(": ")[1]), reverse=True)
        print("Top 10 scores:")
        for line in lines[:10]:
            print(line.strip())

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
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


class cone(Obstacle):
    def __init__(self):
        image = pygame.image.load("assets/cone.png")
        super().__init__("cone", image)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

class rock(Obstacle):
    def __init__(self):
        image = pygame.image.load("assets/rock.png")
        super().__init__("rock", image)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)



score_text = font.render("Score: ", True, BLACK)
score_text_rect = score_text.get_rect()
score_text_rect.topleft = (10, 10)

end_score_text = font.render("Game Over", True, BLACK)
end_score_text_rect = end_score_text.get_rect()
end_score_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


player = Player()

obstacles = pygame.sprite.Group()

start_time = time.time()
score = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if time.time() - start_time > player.speed * 2:
        if player.speed < 20:
            player.speed += 1
    if len(obstacles) < player.speed:
        if random.randint(0, 50) * player.speed > 249:
            obstacles.add([tree(), cone(), rock()][random.randint(0, 2)])
    score += player.speed
    for obstacle in obstacles:
        obstacle.update(player.speed)
    player.update()
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(score_text, score_text_rect)
    score_text = font.render("Score: " + str(score), True, BLACK)
    for obstacle in obstacles:
        obstacle.draw(DISPLAYSURF, player.speed)
    player.draw(DISPLAYSURF)
    for obstacle in obstacles:
        if pygame.sprite.collide_circle(player, obstacle):
            DISPLAYSURF.fill(RED)
            pygame.display.update()
        if pygame.sprite.collide_circle(player, obstacle):
            DISPLAYSURF.fill(RED)
            end_score_text = font.render(f"Game Over!", True, BLACK)
            DISPLAYSURF.blit(score_text, score_text_rect)
            DISPLAYSURF.blit(end_score_text, end_score_text_rect)
            pygame.display.update()
            pygame.time.wait(2000)
            player.save_score(score, name)
            sys.exit()
            pygame.quit()
            break
    pygame.display.update()
    FramePerSec.tick(FPS)



    