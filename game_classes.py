from abc import ABC, abstractmethod
import pygame
from pygame.locals import *
import random

class Player():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, dx):
        self.x += dx
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.image.get_width():
            self.x = SCREEN_WIDTH - self.image.get_width()


class GameObject(ABC):
    def __init__(self, name, x, y,image):
        self.x = x
        self.y = y
        self.name = name
        self.image = image

    def draw(self, screen=None):
        if screen:
            screen.blit(self.image, (self.x, self.y))
        else:  
            raise ValueError("Screen not provided for drawing the object.")
    @abstractmethod
    def move(self, dx, dy):
        pass



    def move(self, dx):
        self.x += dx




