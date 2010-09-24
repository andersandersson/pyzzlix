from globals import *

import pygame
from pygame.locals import *
from image import *

class Hourglass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([90, 150])
        self.rect = self.image.get_rect()
        self.rect.x = BOARD_WIDTH*16+3*16
        self.rect.y = (240 - 150 - 16)
        self.value = 0
        self.max = 0
        
        self.timeatlastframe = 0
        self.frameDelay = 0.1
        self.frame = 0
        
        self.reset(1000)

    def reset(self, value):
        self.value = value*0.5
        self.max = value

    def update(self, deltaTime):
        if self.value <= 0:
            pygame.event.post(pygame.event.Event(EVENT_GAME_OVER))
            return
        if self.value > self.max:
            pygame.event.post(pygame.event.Event(EVENT_LEVEL_UP))
            return

            
        self.value -= 1
        self.image.fill([0,0,0])
        self.image.set_alpha(200);
        p = float(self.value) / self.max

        pygame.draw.rect(self.image, [(1-p)*255,p*255,0], [0,(1-p)*150,90,150])
            
    def draw(self, surf):
        surf.blit(self.image, (self.rect.x, self.rect.y), ((0, 0) , (self.rect.width, self.rect.height)))
