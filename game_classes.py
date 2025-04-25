import pygame
import random
import sys
import time
from pygame.locals import *
from abc import ABC, abstractmethod
from game_config import SCREEN_WIDTH, SCREEN_HEIGHT

# Group to hold obstacles
obstacles = pygame.sprite.Group()

# Abstract base class for game objects
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

# Define the player class
class Player(GameObject, pygame.sprite.Sprite):
    def __init__(self, speed=5):
        pygame.sprite.Sprite.__init__(self)
        GameObject.__init__(self, "Player")
        # Load and scale the player image
        self.image = pygame.image.load("assets\car.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.88)
        self.speed = speed
   
    def update(self):
        # Handle player movement based on key presses
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left >= 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
 
    def draw(self, surface):
        # Draw the player on the screen
        surface.blit(self.image, self.rect)  
    
    def save_score(self, score, name):
        # Save the player's score to a file and display the top 10 scores
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

# Define the obstacle class
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

    def update(self, speed):
        # Update the obstacle's position and reset if it moves off-screen
        if self.present:
            self.rect.move_ip(0, speed)
            if self.rect.top > SCREEN_HEIGHT:
                self.rect.bottom = 0
                self.present = False
                obstacles.remove(self)

    def draw(self, surface, speed):
        # Draw the obstacle on the screen
        if self.present:
            surface.blit(self.image, self.rect)  
        else:
            if random.randint(0, 10) * speed >= self.ticker:
                self.present = True
            else:
                self.ticker -= 1

# Define specific obstacle types
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
