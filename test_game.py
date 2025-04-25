from game_classes import Player, GameObject, tree, cone, rock
from game_config import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
import unittest


class TestGameClasses(unittest.TestCase):
    def test_player_attributes(self):
        player = Player()
        self.assertEqual(player.name, "Player")
        self.assertEqual(player.speed, 5)

    def test_obstacle_initialization(self):
        obstacle = tree()
        self.assertEqual(obstacle.name, "tree")
        self.assertIsInstance(obstacle.image, pygame.Surface)
        self.assertEqual(obstacle.rect.center, (obstacle.x, obstacle.y))

    def test_obstacle_initialization(self):
        obstacle = rock()
        self.assertEqual(obstacle.name, "rock")
        self.assertIsInstance(obstacle.image, pygame.Surface)
        self.assertEqual(obstacle.rect.center, (obstacle.x, obstacle.y))
    
    def test_obstacle_initialization(self):
        obstacle = cone()
        self.assertEqual(obstacle.name, "cone")
        self.assertIsInstance(obstacle.image, pygame.Surface)
        self.assertEqual(obstacle.rect.center, (obstacle.x, obstacle.y))
    




if __name__ == '__main__':
    unittest.main()





