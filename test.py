
import unittest
import oopGame
from oopGame import Player, Enemy, Bullet, Game

class TestPlayer(unittest.TestCase):
    def test_movement(self):
        player = Player()

        # Testing moving left
        player.move_left()
        player.update()
        self.assertEqual(player.x, 366)  #  the player starts at x=370 and moves 4 units to the left

        # Testing moving right
        player.move_right()
        player.update()
        self.assertEqual(player.x, 370)  # The player now move 4 units to the right, back to the starting position

        # Testing stopping
        player.stop_movement()
        player.update()
        self.assertEqual(player.x, 370)  # The player does not move, so x should still be 370

class TestEnemy(unittest.TestCase):
    def test_movement(self):
        enemy = Enemy()

        # Testing initial position of enemy
        self.assertTrue(0 <= enemy.x <= 736)
        self.assertTrue(50 <= enemy.y <= 150)

        # Testing enemy movement
        enemy.update()
        self.assertTrue(0 <= enemy.x <= 736)
        self.assertTrue(50 <= enemy.y <= 180)  #  the enemy moves down by 30 units

class TestBullet(unittest.TestCase):
    def test_fire(self):
        bullet = Bullet()

        # Testing initial state
        self.assertEqual(bullet.state, "ready")

        # Testing firing
        bullet.fire(370)
        self.assertEqual(bullet.state, "fire")
        self.assertEqual(bullet.x, 370)

    def test_update(self):
        bullet = Bullet()
        bullet.fire(370)

        # Testing  bullet movement
        bullet.update()
        self.assertEqual(bullet.y, 473)  # the bullet starts at y=480 and moves up by 7 units

class TestGame(unittest.TestCase):
    def test_collision(self):
        game = Game()
        enemy = Enemy()
        bullet = Bullet()

        # Test no collision
        enemy.x = 100
        enemy.y = 100
        bullet.x = 200
        bullet.y = 200
        self.assertFalse(game.collision(enemy, bullet))

if __name__ == "__main__":
    unittest.main()

