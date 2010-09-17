from globals import *

import pygame
from pygame.locals import *

class Image(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        self.timeatlastframe = 0
        self.frameDelay = 0.1
        self.frame = 0

    def loadSheet(self, name, width, height):
        self.images = loadImageSheet(name, width, height)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def update(self, deltaTime):
        if len(self.images):
            self.timeatlastframe += deltaTime
            while (self.timeatlastframe >= self.frameDelay):
                self.timeatlastframe -= self.frameDelay
                if self.frame >= len(self.images):
                    self.frame = 0
                    self.image = self.images[self.frame]
                    self.frame += 1

    def draw(self, surf):
        surf.blit(self.image, (self.rect.x, self.rect.y), ((0, 0) , (self.rect.width, self.rect.height)))
