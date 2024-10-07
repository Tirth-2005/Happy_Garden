import math
from random import randint
import cfg
import pygame

class Actor(pygame.sprite.Sprite):
    def __init__(self, image, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 4

    def move(self, screensize, direction):
        if direction == 'left':
            self.rect.left = max(self.rect.left - self.speed, 0)
        elif direction == 'right':
            self.rect.left = min(self.rect.left + self.speed, screensize[0])
        elif direction == 'up':
            self.rect.top = max(self.rect.top - self.speed, 0)
        elif direction == 'down':
            self.rect.top = min(self.rect.top + self.speed, screensize[0])

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class flower(pygame.sprite.Sprite):
    def __init__(self, image, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        WIDTH,  HEIGHT = cfg.SCREEN_SIZE
        self.mask = pygame.transform.from_surface(self.image)
        self.rect.left, self.rect.top = randint(50, WIDTH-50), randint(150, HEIGHT-100)

    def  draw(self, screen):
        screen.blit(self.image, self.rect)

