import random
from os import listdir
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT

pygame.init()
FPS = pygame.time.Clock()
screen = width, height = 1200, 800

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
YELLOW = 255, 255, 0
BLUE = 0, 0, 255

font = pygame.font.SysFont("Verdana", 32)

main_surface = pygame.display.set_mode(screen)

#create hero
# player = pygame.Surface((20, 20))
# player.fill(WHITE)
player_imgs = [
    pygame.transform.scale(
        pygame.image.load('./assets/goose/' + file).convert_alpha(), (200, 80))
    for file in listdir("./assets/goose")
]

player = player_imgs[0]
# player = pygame.transform.scale(
#     pygame.image.load('./assets/player.png').convert_alpha(), (100, 40))

player_rect = player.get_rect()
player_speed = 5

background = pygame.transform.scale(
    pygame.image.load('./assets/background.png').convert(), screen)
backgroundX = 0
backgroundX2 = background.get_width()
background_speed = 3


# function create enemy
def create_enemy():
    # enemy = pygame.Surface((20, 20))
    # enemy.fill(RED)
    enemy = pygame.transform.scale(
        pygame.image.load('./assets/enemy.png').convert_alpha(), (60, 30))
    enemy_rect = pygame.Rect(width, random.randint(50, height - 50),
                             *enemy.get_size())
    enemy_speed = random.randint(4, 6)
    return [enemy, enemy_rect, enemy_speed]


# function create enemy
def create_benefit():
    # benefit = pygame.Surface((10, 10))
    # benefit.fill(YELLOW)
    benefit = pygame.transform.scale(
        pygame.image.load('./assets/benefit.png').convert_alpha(), (30, 60))
    benefit_rect = pygame.Rect(random.randint(30, width - 30), 0,
                               *benefit.get_size())
    benefit_speed = random.randint(2, 6)
    return [benefit, benefit_rect, benefit_speed]


# timer for create enemy
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 2500)

# timer for create benefit
CREATE_BENEFIT = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BENEFIT, 3500)

# change image for animation goose
CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

img_index = 0
scores = 0
life = 3

# list of enemies
enemies = []
# list of benefits
benefits = []

#run game
is_working = True
while is_working:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BENEFIT:
            benefits.append(create_benefit())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]

    # listen pressed key
    pressed_keys = pygame.key.get_pressed()

    #refill screen
    # main_surface.fill(WHITE)
    #static background
    # main_surface.blit(background, (0, 0))

    # dynamics background
    backgroundX -= background_speed
    backgroundX2 -= background_speed

    if backgroundX < -background.get_width():
        backgroundX = background.get_width()

    if backgroundX2 < -background.get_width():
        backgroundX2 = background.get_width()

    main_surface.blit(background, (backgroundX, 0))
    main_surface.blit(background, (backgroundX2, 0))

    #draw hero
    main_surface.blit(player, player_rect)

    #draw font
    main_surface.blit(font.render("life - " + str(life), True, RED), (10, 0))

    main_surface.blit(font.render("scores - " + str(scores), True, RED),
                      (width - 180, 0))

    #draw and move enemies
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        #delete enemy when it is behind screen
        if enemy[1].left < -61:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy))
            life -= 1
            if life <= 0:
                main_surface.blit(font.render("Game  over!", True, BLACK),
                                  (width / 2, height / 2))
                is_working = False

    #draw and move benefits
    for benefit in benefits:
        benefit[1] = benefit[1].move(0, benefit[2])
        main_surface.blit(benefit[0], benefit[1])

        #delete benefit when it is behind screen
        if benefit[1].bottom > height + 60:
            benefits.pop(benefits.index(benefit))

        if player_rect.colliderect(benefit[1]):
            benefits.pop(benefits.index(benefit))
            scores += 1

    # if player_rect.bottom >= heights or player_rect.top <= 0:
    #     player_speed[1] = -player_speed[1]
    #     player.fill(BLUE)

    # if player_rect.left <= 0 or player_rect.right >= width:
    #     player_speed[0] = -player_speed[0]
    #     player.fill(YELLOW)

    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)

    pygame.display.flip()
