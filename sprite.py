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
        self._updatetime = 0
        self._ref_x = 0
        self._ref_y = 0
        self._reftime_pos = 0
               
    def loadSheet(self, name, width, height):
        self.images = loadImageSheet(name, width, height)
        self.frameCount = len(self.images)
        self.frameDelays = self.frameCount * [0.1]
        self.currentImage = self.images[0]
        self.width = self.currentImage.width
        self.height = self.currentImage.height

    def updatePos(self, currentTime):
        if (self._reftime_pos <= currentTime):
            self.x = self._ref_x
            self.y = self._ref_y
        else:    
            factorT = (self._reftime_pos - self._updatetime) * (currentTime - self._updatetime)
            self.x = self.x + (self._ref_x - self.x) * factorT
            self.y = self.y + (self._ref_y - self.y) * factorT
        self._updatetime = currentTime

    def update(self, currentTime): 
        self.updatePos(currentTime)
        if (self.frameCount > 0):
            while (self.frameTimer + self.frameDelays[self.frame] <= currentTime):
                self.frameTimer += self.frameDelays[self.frame]
                self.frame += 1
                if self.frame >= self.frameCount:
                    self.frame = 0
                   
            self.currentImage = self.images[self.frame]        
    
    def moveTo(self, x, y, currentTime, duration):
        self.updatePos(currentTime)
        self._ref_x = x
        self._ref_y = y
        self._reftime_pos = currentTime + duration
        
    def setPos(self, x, y):
        self._ref_x = x
        self._ref_y = y
        self.x = x
        self.y = y
        self._reftime_pos = 0
        