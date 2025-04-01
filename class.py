from abc import ABC, abstractmethod
import pygame

class playercar:
    def __init__(self, xpos, ypos, dir, img):
        self.xpos = xpos
        self.ypos = ypos
        self.dir = dir
        self.img = img
    def draw(self):


class obstacle(ABC):
    def __init__(self, xpos, ypos)
        self.xpos = xpos
        self.ypos = ypos


class tree(obstacle):
    def __init__(self, xpos, ypos, img):
        self.xpos = xpos
        self.ypos = ypos
        self.img = img
    def draw(self):
        screen.blit(self.img, (self.xpos, self.ypos))

class rock(obstacle):
    def draw(self):
        pygame.draw.rect(screen, (139, 69, 19), (self.xpos, self.ypos, 20, 20))
