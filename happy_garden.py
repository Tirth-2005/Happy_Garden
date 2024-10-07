import pygame
from random import randint
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Happy Garden")

cow_img = pygame.image.load('Happy Garden/resources/images/cow.png')
cow = cow_img.get_rect(topleft=(100, 500))
garden_img = pygame.image.load('Happy Garden/resources/images/garden.png')
flower_img = pygame.image.load('Happy Garden/resources/images/flower.png')
wilted_flower_img = pygame.image.load('Happy Garden/resources/images/flower-wilt.png')
fangflower_img = pygame.image.load('Happy Garden/resources/images/fangpink.png')

CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
cow = cow_img.get_rect(topleft=(100, 500))
flower_list = []
wilted_list = []
fangflower_list = []
fangflower_vy_list = []
fangflower_vx_list = []

game_over = False
finalized = False
garden_happy = True
fangflower_collision = False

start_time = time.time()
time_elapsed = 0

def new_flower():
  flower_rect = flower_img.get_rect(
    center = (randint(50, WIDTH - 50), randint(150, HEIGHT - 100))
  )
  flower_list.append(flower_rect)
  wilted_list.append("happy")

def add_flowers():
  if not game_over:
    new_flower()

def wilt_flower():
    if not game_over and flower_list:
        rand_flower = randint(0, len(flower_list) - 1)
        if wilted_list[rand_flower] == "happy":
            wilted_list[rand_flower] = time.time()

def check_flower_wilted_time():
    global game_over
    current_time = time.time()
    for index, wilted_time in enumerate(wilted_list):
        if wilted_time != "happy":
            if current_time - wilted_time > 5:  
                game_over = True

def check_flower_collision():
    keys = pygame.key.get_pressed()
    for index, flower in enumerate(flower_list):
        if cow.colliderect(flower) and wilted_list[index] != "happy" and keys[pygame.K_SPACE]:
            wilted_list[index] = "happy"

def mutate():
    if not game_over and flower_list:
        rand_flower = randint(0, len(flower_list) - 1)
        flower_rect = flower_list.pop(rand_flower)
        fangflower_list.append(flower_rect)
        fangflower_vx_list.append(randint(2, 3))
        fangflower_vy_list.append(randint(2, 3))

def check_flower_collision():
    for index, flower in enumerate(flower_list):
        if cow.colliderect(flower) and wilted_list[index] != "happy":
            wilted_list[index] = "happy"

def mutate():
    if not game_over and flower_list:
        rand_flower = randint(0, len(flower_list) - 1)
        flower_rect = flower_list.pop(rand_flower)
        fangflower_list.append(flower_rect)
        fangflower_vx_list.append(randint(2, 3))
        fangflower_vy_list.append(randint(2, 3))
 
def update_fangflowers():
    for i, fangflower in enumerate(fangflower_list):
        fangflower.move_ip(fangflower_vx_list[i], fangflower_vy_list[i])

        if fangflower.left < 0 or fangflower.right > WIDTH:
            fangflower_vx_list[i] = -fangflower_vx_list[i]
        if fangflower.top < 150 or fangflower.bottom > HEIGHT:
            fangflower_vy_list[i] = -fangflower_vy_list[i]  

        if cow.colliderect(fangflower):
            game_over = True

def game_loop():
    global time_elapsed, game_over
    clock = pygame.time.Clock()

    flower_timer = pygame.USEREVENT + 1
    wilt_timer = pygame.USEREVENT + 2
    mutate_timer = pygame.USEREVENT + 3

    pygame.time.set_timer(flower_timer, 3000)
    pygame.time.set_timer(wilt_timer, 3000)
    pygame.time.set_timer(mutate_timer, 20000)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == flower_timer:
                add_flowers()
            elif event.type == wilt_timer:
                wilt_flower()
            elif event.type == mutate_timer:
                mutate()
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and cow.left > 0:
            cow.x -= 5
        if keys[pygame.K_RIGHT] and cow.right < WIDTH:
            cow.x += 5
        if keys[pygame.K_UP] and cow.top > 150:
            cow.y -= 5
        if keys[pygame.K_DOWN] and cow.bottom < HEIGHT:
            cow.y += 5

        check_flower_collision()
        update_fangflowers() 
        check_flower_wilted_time() 
        time_elapsed = int(time.time() - start_time)

        screen.blit(garden_img, (0, 0))
        screen.blit(cow_img, cow.topleft)  

        update_fangflowers()
        time_elapsed = int(time.time() - start_time)

        screen.blit(garden_img, (0, 0))
        screen.blit(cow_img, cow.topleft)

        for flower in flower_list:
            screen.blit(flower_img if wilted_list[flower_list.index(flower)] == "happy" else wilted_flower_img, flower.topleft)
        for fangflower in fangflower_list:
            screen.blit(fangflower_img, fangflower.topleft)

        font = pygame.font.SysFont(None, 36)
        time_text = font.render(f"Garden happy for: {time_elapsed} seconds", True, (0, 0, 0))
        screen.blit(time_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(game_over_text, (CENTER_X - 150, CENTER_Y - 50))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()

game_loop()