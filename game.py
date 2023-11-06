import pygame
import random 
import math
from pygame import mixer

pygame.init()

#creating the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))   #(width, height) the screen only pops up for few sec and it closes because the code only runs till this line no other commands are give to keep the screen 
clock = pygame.time.Clock()
# background
background = pygame.image.load('space_stars_sky_116649_800x600.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)


# game name and Logo
pygame.display.set_caption("Space Gardian")



# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480  # these are the coordinates, to where to place the player image
playerX_change = 0   


# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy =  7

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('invaders.png'))
    enemyX.append(random.randint(0, 736)) 
    enemyY.append(random.randint(50, 150))        #to randomly place the enemy 
    enemyX_change.append(0.3)  
    enemyY_change.append(40) 

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480        
bulletX_change = 0 
bulletY_change = 0.5
bullet_state = "ready"          #ready = can't see the bullet on the screen /  fire = bullet is currently moving

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10
#  game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def draw_start_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('arial', 40)
    title = font.render('Space Guardian', True, (255, 255, 255))
    start_button = font.render('Start', True, (255, 255, 255))
    screen.blit(title, (screen_width/2 - title.get_width()/2, screen_height/2 - title.get_height()/2))
    screen.blit(start_button, (screen_width/2 - start_button.get_width()/2, screen_height/2 + start_button.get_height()/2))

def draw_restart_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('arial', 40)
    title = font.render('Game Over', True, (255, 255, 255))
    restart_button = font.render('Restart', True, (255, 255, 255))
    screen.blit(title, (screen_width/2 - title.get_width()/2, screen_height/2 - title.get_height()/2))
    screen.blit(restart_button, (screen_width/2 - restart_button.get_width()/2, screen_height/2 + restart_button.get_height()/2))




def show_score(x, y):
    score = font.render("Score :"+ str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER :", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))   # blit basically draws the image on the screen and to make the player always visible we added the player function the insdie thewhile loop



def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))



def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))    #adding because we to make the bullet from the top of the spaceship


def collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX,2) + (math.pow(enemyY - bulletY,2))))
    if distance < 27:
        return True
    else:
        return False


# game loop (to keep the screen running)
running = True

while running:

    screen.fill((0, 0, 0))   # R, G, B (red, green, blue)  to change the color of the screen

    #background img
    screen.blit(background,(0, 0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False               # the screen keep on running until we close it 

        # Keys usage
        if event.type == pygame.KEYDOWN:            #KEYDOWN means that a key is pressed 
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":         # get the current x-coordinate of the spaceship 
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:          # KEYUP means that a key is released 
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736           # to make the boundry for the spaceship so that it does not cross the bound



# enemy movement
    for i in range(num_of_enemy):

        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemy):
                enemyY[j] = 2000

            game_over_text()
            break 

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2          
            enemyY[i] += enemyY_change[i]

        #  collision
        Thecollision = collision(enemyX[i], enemyY[i], bulletX , bulletY)
        if Thecollision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)  

        enemy(enemyX[i], enemyY[i], i)       


    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"


    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY) 
    show_score(textX, textY)
    pygame.display.update()
