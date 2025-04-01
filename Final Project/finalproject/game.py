import pygame
import random
from class import *

# Initialize the game
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((800, 600))

# Set the title of the game
pygame.display.set_caption("Car Game")

# Load the images
playercar = pygame.image.load("assets/Car_1_01.png")
dmgcar = pygame.image.load("assets/Car_1_04.png")
tree = pygame.image.load("assets/tree.png")
rock = pygame.image.load("assets/rock.png")

# Create the player car
player = playercar(400, 500, 0, playercar)

# Create the obstacles
obstacles = []

# Game loop
running = True

while running:
    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the player car
    player.draw()

    # Draw the obstacles
    for obstacle in obstacles:
        obstacle.draw()

    # Update the display
    pygame.display.update()

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Add a new obstacle
    if random.randint(1, 100) == 1:
        if random.randint(1, 2) == 1:
            obstacles.append(tree(random.randint(0, 800), 0))
        else:
            obstacles.append(rock(random.randint(0, 800), 0))
    


