import sys
import pygame
from random import randint
from random import choice
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
    pygame.draw.rect(screen, (100, 40, 50), (0, 0, cfg.SCREENSIZE[0]//2, cfg.SCREENSIZE[1]))
    pygame.draw.rect(screen, (255, 105, 180), (cfg.SCREENSIZE[0]//2, 0, cfg.SCREENSIZE[0]//2, cfg.SCREENSIZE[1]))

    actor_1 = game_images['cow']
    actor_2 = game_images['pig']

    a_1 = pygame.transform.scale(actor_1, (100, 100))
    a_2 = pygame.transform.scale(actor_2, (80, 100)) 

    screen.blit(a_1, (150, 200))
    screen.blit(a_2, (550, 200))
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
                elif 400 <= mouse_pos[0] <= 650 and 100 <= mouse_pos[1] <= 300:
                    return 2
        
        pygame.display.update()

def game_loop():
    screen, game_images = initGame()
    clock = pygame.time.Clock()

    actor_selection, game_over = StartInterface(screen, game_images), False

    if actor_selection == 1:
        actor_img = game_images['cow']
        actor_img = pygame.transform.scale(actor_img, (100, 100))
        actor_water = game_images['cow_water']
        actor_water = pygame.transform.scale(actor_water, (100, 100))
        actor = actor_img.get_rect(topleft=(100, 500))
    elif actor_selection == 2:
        actor_img = game_images['pig']
        actor_img = pygame.transform.scale(actor_img, (75, 100))
        actor_water = game_images['pig_water']
        actor_water = pygame.transform.scale(actor_water, (85, 100))
        actor = actor_img.get_rect(topleft=(100, 500))
   
    # cow_img = game_images['cow']
    # cow = cow_img.get_rect(topleft=(100, 500))
    
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
            if actor.colliderect(flower) and wilted_list[index] != "happy" and keys[pygame.K_SPACE]:
                if actor_selection == 2:
                    water_offset = (-12, 0)
                else:
                    water_offset = (-3, 0)

                screen.blit(actor_water, (actor.left + water_offset[0], actor.top + water_offset[1]))
                pygame.display.flip()
                time.sleep(0.3)

                wilted_list[index] = "happy"
                screen.blit(actor_img, actor.topleft)

    def mutate():
        if not game_over and flower_list:
            rand_flower = randint(0, len(flower_list) - 1)
            flower_rect = flower_list.pop(rand_flower)

            fangflower = choice(['fang_pink',  'fang_red', 'fang_blue'])
            fangflower_img = game_images[fangflower]
            fangflower_img = pygame.transform.scale(fangflower_img, (80, 100))
            fangflower_rect = fangflower_img.get_rect(topleft=flower_rect.topleft)
            
            fangflower_list.append((fangflower_rect, fangflower_img))
            fangflower_vx_list.append(randint(2, 3))
            fangflower_vy_list.append(randint(2, 3))

    def update_fangflowers():
        for i, (fangflower_rect, fangflower_img) in enumerate(fangflower_list):
            fangflower_rect.move_ip(fangflower_vx_list[i], fangflower_vy_list[i])
            if fangflower_rect.left < 0 or fangflower_rect.right > cfg.SCREENSIZE[0]:
                fangflower_vx_list[i] = -fangflower_vx_list[i]
            if fangflower_rect.top < 150 or fangflower_rect.bottom > cfg.SCREENSIZE[1]:
                fangflower_vy_list[i] = -fangflower_vy_list[i]  
            if actor.colliderect(fangflower_rect):
                nonlocal game_over

                zap_img = game_images['zap']
                zap_x = actor.left + 10
               

    flower_timer = pygame.USEREVENT + 1
    wilt_timer = pygame.USEREVENT + 2
    mutate_timer = pygame.USEREVENT + 3

    pygame.time.set_timer(flower_timer, 3000)
    pygame.time.set_timer(wilt_timer, 4000)
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
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and actor.left > 0:
            actor.x -= 5
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and actor.right < cfg.SCREENSIZE[0]:
            actor.x += 5
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and actor.top > 150:
            actor.y -= 5
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and actor.bottom < cfg.SCREENSIZE[1]:
            actor.y += 5

        check_flower_collision()
        update_fangflowers()  
        check_flower_wilted_time()  

        screen.blit(game_images['garden'], (0, 0))
        screen.blit(actor_img, actor.topleft)

        for flower in flower_list:
            screen.blit(game_images['flower'] if wilted_list[flower_list.index(flower)] == "happy" else game_images['wilted_flower'], flower.topleft)
        for fangflower_rect, fangflower_img in fangflower_list:
            screen.blit(fangflower_img, fangflower_rect.topleft)

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
