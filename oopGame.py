import pygame
import random
import math
from pygame import mixer

class Player:
    def __init__(self):
        self.image = pygame.image.load('spaceship.png')
        self.x = 370
        self.y = 480
        self.x_change = 0

    def move_left(self):
        self.x_change = -4

    def move_right(self):
        self.x_change = 4

    def stop_movement(self):
        self.x_change = 0

    def update(self):
        self.x += self.x_change

        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736

class Enemy:
    def __init__(self):
        self.image = pygame.image.load('invaders.png')
        self.x = random.randint(0, 736)
        self.y = random.randint(50, 150)
        self.x_change = 3
        self.y_change = 30

    def update(self):
        self.x += self.x_change

        if self.x <= 0:
            self.x_change = 2
            self.y += self.y_change
        elif self.x >= 736:
            self.x_change = -2
            self.y += self.y_change

class Bullet:
    def __init__(self):
        self.image = pygame.image.load('bullet.png')
        self.x = 0
        self.y = 480
        self.x_change = 0
        self.y_change = 7
        self.state = "ready"

    def fire(self, player_x):
        if self.state == "ready":
            self.x = player_x
            self.state = "fire"

    def update(self):
        if self.state == "fire":
            self.y -= self.y_change

        if self.y <= 0:
            self.y = 480
            self.state = "ready"

class Game:
    def __init__(self):
        pygame.init()

        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Space Guardian")

        self.clock = pygame.time.Clock()

        self.background = pygame.image.load('space_stars_sky_116649_800x600.png')
        mixer.music.load('background.wav')
        mixer.music.play(-1)

        self.player = Player()
        self.num_of_enemies = 7
        self.enemies = [Enemy() for _ in range(self.num_of_enemies)]
        self.bullet = Bullet()

        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text_x = 10
        self.text_y = 10

        

    def show_score(self):
        score_display = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_display, (self.text_x, self.text_y))

    def game_over_text(self):
        game_over_font = pygame.font.Font('freesansbold.ttf', 64)
        game_over_display = game_over_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(game_over_display, (200, 250))

    def collision(self, enemy, bullet):
        distance = math.sqrt((enemy.x - bullet.x) ** 2 + (enemy.y - bullet.y) ** 2)
        return distance < 27

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.player.move_right()
                    if event.key == pygame.K_SPACE:
                        self.bullet.fire(self.player.x)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.stop_movement()

            self.player.update()

            for enemy in self.enemies:
                if enemy.y > 440:
                    self.game_over_text()
                    pygame.display.update()
                    pygame.time.delay(2000)
                    running = False

                enemy.update()

                if self.collision(enemy, self.bullet):
                    explosion_sound = mixer.Sound('explosion.wav')
                    explosion_sound.play()
                    self.bullet.y = 480
                    self.bullet.state = "ready"
                    self.score += 1
                    enemy.x = random.randint(0, 736)
                    enemy.y = random.randint(50, 150)

            self.bullet.update()

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.player.image, (self.player.x, self.player.y))

            for enemy in self.enemies:
                self.screen.blit(enemy.image, (enemy.x, enemy.y))

            if self.bullet.state == "fire":
                self.screen.blit(self.bullet.image, (self.bullet.x + 16, self.bullet.y + 10))

            self.show_score()
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        quit()

if __name__ == "__main__":
    game = Game()
    game.run()


