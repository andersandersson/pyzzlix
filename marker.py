from globals import *

import pygame
from pygame.locals import *


class Marker(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.images = loadImageSheet("marker.bmp", 32, 32)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.offset_x = 0
        self.offset_y = 0
        self.scale_x = 16
        self.scale_y = 16

        self.moveTo(x, y)

        self.timeatlastframe = 0
        self.frameDelay = 0.1
        self.frame = 0
        self.layer = type
        
    def moveTo(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x * self.scale_x + self.offset_x
        self.rect.y = self.y * self.scale_y + self.offset_y

    def move(self, dx, dy):
        self.moveTo(self.x+dx, self.y+dy)

    def update(self, deltaTime):
        self.timeatlastframe += deltaTime
        while (self.timeatlastframe >= self.frameDelay):
            self.timeatlastframe -= self.frameDelay
            if self.frame >= len(self.images): 
                self.frame = 0
            self.image = self.images[self.frame]
            self.frame += 1
            
    def draw(self, surf):
        surf.blit(self.image, (self.rect.x, self.rect.y), ((0, 0) , (self.rect.width, self.rect.height)))
