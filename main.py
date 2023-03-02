import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT

pygame.init()
FPS = pygame.time.Clock()
screen = width, height = 800, 600

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
YELLOW = 255, 255, 0
BLUE = 0, 0, 255

font = pygame.font.SysFont("Verdana", 20)

main_surface = pygame.display.set_mode(screen)

#create hero
ball = pygame.Surface((20, 20))
ball.fill(WHITE)
ball_rect = ball.get_rect()
ball_speed = 5


# function create enemy
def create_enemy():
    enemy = pygame.Surface((20, 20))
    enemy.fill(RED)
    enemy_rect = pygame.Rect(width, random.randint(0, height),
                             *enemy.get_size())
    enemy_speed = random.randint(4, 6)
    return [enemy, enemy_rect, enemy_speed]


# function create enemy
def create_benefit():
    benefit = pygame.Surface((10, 10))
    benefit.fill(YELLOW)
    benefit_rect = pygame.Rect(random.randint(0, width), 0,
                               *benefit.get_size())
    benefit_speed = random.randint(4, 6)
    return [benefit, benefit_rect, benefit_speed]


# timer for create enemy
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

# timer for create benefit
CREATE_BENEFIT = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_BENEFIT, 2500)

scores = 0

# list og enemies
enemies = []
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

    # listen pressed key
    pressed_keys = pygame.key.get_pressed()

    #refill screen
    main_surface.fill(BLACK)

    #draw hero
    main_surface.blit(ball, ball_rect)

    #draw font
    main_surface.blit(font.render(str(scores), True, WHITE), width - 30, 0)
    #draw and move enemies
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        #delete enemy when it is behind screen
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(enemy[1]):
            is_working = False

    #draw and move benefits
    for benefit in benefits:
        benefit[1] = benefit[1].move(0, benefit[2])
        main_surface.blit(benefit[0], benefit[1])

        #delete benefit when it is behind screen
        if benefit[1].bottom > height:
            benefits.pop(benefits.index(benefit))

        if ball_rect.colliderect(benefit[1]):
            benefits.pop(benefits.index(benefit))
            scores += 1

    # if ball_rect.bottom >= heights or ball_rect.top <= 0:
    #     ball_speed[1] = -ball_speed[1]
    #     ball.fill(BLUE)

    # if ball_rect.left <= 0 or ball_rect.right >= width:
    #     ball_speed[0] = -ball_speed[0]
    #     ball.fill(YELLOW)

    if pressed_keys[K_DOWN] and not ball_rect.bottom >= height:
        ball_rect = ball_rect.move(0, ball_speed)

    if pressed_keys[K_UP] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move(0, -ball_speed)

    if pressed_keys[K_RIGHT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed, 0)

    if pressed_keys[K_LEFT] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move(-ball_speed, 0)

    print(len(benefits))
    pygame.display.flip()
