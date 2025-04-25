import pygame
import random 
import time
import sys
from pygame.locals import QUIT, K_LEFT, K_RIGHT
from game_classes import Player, tree, cone, rock, obstacles
from game_config import SCREEN_WIDTH, SCREEN_HEIGHT

# Initialize Pygame
pygame.init()
 
# Set the frame rate
FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Font for rendering text
font = pygame.font.SysFont(None, 30)

# Initialize the display surface
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Game")

# Initialize score display
score_text = font.render("Score: ", True, BLACK)
score_text_rect = score_text.get_rect()
score_text_rect.topleft = (10, 10)

# Initialize game over text
end_score_text = font.render("Game Over", True, BLACK)
end_score_text_rect = end_score_text.get_rect()
end_score_text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Create the player object
player = Player()



# Initialize game variables
start_time = time.time()
score = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    # Increase player speed over time
    if time.time() - start_time > player.speed * 2:
        if player.speed < 20:
            player.speed += 1
    
    # Add new obstacles based on player speed
    if len(obstacles) < player.speed:
        if random.randint(0, 50) * player.speed > 249:
            obstacles.add([tree(), cone(), rock()][random.randint(0, 2)])
    
    # Update score
    score += player.speed
    
    # Update obstacles and player
    for obstacle in obstacles:
        obstacle.update(player.speed)
    player.update()
    
    # Clear the screen
    DISPLAYSURF.fill(BLACK)
    
    # Display the score
    DISPLAYSURF.blit(score_text, score_text_rect)
    score_text = font.render("Score: " + str(score), True, BLACK)
    
    # Draw obstacles and player
    for obstacle in obstacles:
        obstacle.draw(DISPLAYSURF, player.speed)
    player.draw(DISPLAYSURF)
    
    # Check for collisions
    for obstacle in obstacles:
        if pygame.sprite.collide_circle(player, obstacle):
            # Handle game over
            DISPLAYSURF.fill(RED)
            pygame.display.update()
            DISPLAYSURF.fill(RED)
            end_score_text = font.render("Game Over!", True, BLACK)
            DISPLAYSURF.blit(score_text, score_text_rect)
            DISPLAYSURF.blit(end_score_text, end_score_text_rect)
            pygame.display.update()
            pygame.time.wait(2000)
            
            # Handle name input for saving score
            input_active = True
            name = ""
            input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 30)
            color_inactive = pygame.Color('lightskyblue3')
            color_active = pygame.Color('dodgerblue2')
            color = color_inactive
            font = pygame.font.Font(None, 32)
            instruction_text = font.render("Enter your name and press Enter:", True, RED)
            while input_active:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if input_box.collidepoint(event.pos):
                            input_active = True
                            color = color_active
                        else:
                            color = color_inactive
                    if event.type == pygame.KEYDOWN:
                        if input_active:
                            if event.key == pygame.K_RETURN:
                                input_active = False
                                if not name.strip():
                                    name = "Player"
                            elif event.key == pygame.K_BACKSPACE:
                                name = name[:-1]
                            else:
                                name += event.unicode
                DISPLAYSURF.fill(WHITE)
                DISPLAYSURF.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
                pygame.draw.rect(DISPLAYSURF, color, input_box, 2)
                text_surface = font.render(name, True, BLACK)
                DISPLAYSURF.blit(text_surface, (input_box.x + 5, input_box.y + 5))
                input_box.w = max(200, text_surface.get_width() + 10)
                pygame.display.flip()
            
            # Save the score and exit
            player.save_score(score, name)
            sys.exit()
            pygame.quit()
            break
    
    # Update the display
    pygame.display.update()
    FramePerSec.tick(FPS)