import sys
import pygame
from random import randint
import time
import cfg

def initGame():
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption("Happy Garden")
    
    game_images = {key: pygame.image.load(value) for key, value in cfg.IMAGE_PATH.items()}
    
    return screen, game_images

def StartInterface(screen, game_images):
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (255, 105, 180), (0, 0, cfg.SCREENSIZE[0]//2, cfg.SCREENSIZE[1]))
    pygame.draw.rect(screen, (0, 0, 255), (cfg.SCREENSIZE[0]//2, 0, cfg.SCREENSIZE[0]//2, cfg.SCREENSIZE[1]))

    actor_1 = game_images['cow']
    actor_2 = game_images['pig']
    screen.blit(actor_1, (100, 200))
    screen.blit(actor_2, (400, 200))
    font = pygame.font.Font(None, 50)
    select = font.render("Select a character:", True, (0, 255, 0))
    srect = select.get_rect()
    srect.midtop = (cfg.SCREENSIZE[0] // 2, 40)
    screen.blit(select, srect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 100 <= mouse_pos[0] <= 300 and 100 <= mouse_pos[1] <= 300:
                    return 1
                elif 400 <= mouse_pos[0] <= 600 and 100 <= mouse_pos[1] <= 300:
                    return 2
        
        pygame.display.update()

def game_loop():
    screen, game_images = initGame()
    clock = pygame.time.Clock()

    acter, game_over = StartInterface(screen, game_images), False

    cow_img = game_images['cow']
    cow = cow_img.get_rect(topleft=(100, 500))
    
    flower_list = []
    wilted_list = []
    fangflower_list = []
    fangflower_vy_list = []
    fangflower_vx_list = []

    start_time = time.time()

    def new_flower():
        flower_rect = game_images['flower'].get_rect(center=(randint(50, cfg.SCREENSIZE[0] - 50), randint(150, cfg.SCREENSIZE[1] - 100)))
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
        nonlocal game_over
        current_time = time.time()
        for index, wilted_time in enumerate(wilted_list):
            if wilted_time != "happy" and current_time - wilted_time > 5:
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
            fangflower_rect = game_images['fangflower'].get_rect(topleft=flower_rect.topleft)
            fangflower_list.append(fangflower_rect)
            fangflower_vx_list.append(randint(2, 3))
            fangflower_vy_list.append(randint(2, 3))

    def update_fangflowers():
        for i, fangflower in enumerate(fangflower_list):
            fangflower.move_ip(fangflower_vx_list[i], fangflower_vy_list[i])
            if fangflower.left < 0 or fangflower.right > cfg.SCREENSIZE[0]:
                fangflower_vx_list[i] = -fangflower_vx_list[i]
            if fangflower.top < 150 or fangflower.bottom > cfg.SCREENSIZE[1]:
                fangflower_vy_list[i] = -fangflower_vy_list[i]  
            if cow.colliderect(fangflower):
                nonlocal game_over
                game_over = True

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
                sys.exit()
            elif event.type == flower_timer:
                add_flowers()
            elif event.type == wilt_timer:
                wilt_flower()
            elif event.type == mutate_timer:
                mutate()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and cow.left > 0:
            cow.x -= 5
        if keys[pygame.K_RIGHT] and cow.right < cfg.SCREENSIZE[0]:
            cow.x += 5
        if keys[pygame.K_UP] and cow.top > 150:
            cow.y -= 5
        if keys[pygame.K_DOWN] and cow.bottom < cfg.SCREENSIZE[1]:
            cow.y += 5

        check_flower_collision()
        update_fangflowers()  
        check_flower_wilted_time()  

        screen.blit(game_images['garden'], (0, 0))
        screen.blit(cow_img, cow.topleft)

        for flower in flower_list:
            screen.blit(game_images['flower'] if wilted_list[flower_list.index(flower)] == "happy" else game_images['wilted_flower'], flower.topleft)
        for fangflower in fangflower_list:
            screen.blit(game_images['fangflower'], fangflower.topleft)

        time_elapsed = int(time.time() - start_time)
        font = pygame.font.SysFont(None, 36)
        time_text = font.render(f"Garden happy for: {time_elapsed} seconds", True, (0, 0, 0))
        screen.blit(time_text, (10, 10))

        pygame.display.flip()
        clock.tick(cfg.FPS)

    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(game_over_text, (cfg.SCREENSIZE[0] // 2 - 150, cfg.SCREENSIZE[1] // 2 - 50))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()

if __name__ == '__main__':
    game_loop()
