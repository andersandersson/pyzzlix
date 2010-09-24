from globals import *

import pygame
from pygame.locals import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.subSprites = []
        self.images = []
        self.frameDelays = []
        self.currentImage = 0
        self.frame = 0
        self.frameTimer = 0
        self.frameCount = 0
        self.x = 0
        self.y = 0
       
        
    def loadSheet(self, name, width, height):
        self.images = loadImageSheet(name, width, height)
        self.frameCount = len(self.images)
        self.frameDelays = self.frameCount * [0.1]
        self.currentImage = self.images[0]
        self.width = self.currentImage.width
        self.height = self.currentImage.height

    def update(self, deltaTime):
        if (self.frameCount > 0):
            self.frameTimer += deltaTime
            while (self.frameTimer >= self.frameDelays[self.frame]):
                self.frameTimer -= self.frameDelays[self.frame]
                self.currentImage = self.images[self.frame]
                self.frame += 1
                if self.frame >= self.frameCount:
                    self.frame = 0
    
    def draw(self, surf):
        #surf.blit(self.image, (self.rect.x, self.rect.y), ((0, 0) , (self.rect.width, self.rect.height)))
        pass
        