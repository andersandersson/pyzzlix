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
        self.frameTimer = 0.0
        self.frameCount = 0.0
        self.center = (0.0, 0.0)
        self.pos = (0.0, 0.0)
        self._pos_lasttime = 0.0
        self._pos_ref = (0.0, 0.0)
        self._pos_reftime = 0.0
        self.scale = (1.0, 1.0)
        self._scale_lasttime = 0.0
        self._scale_ref = (1.0, 1.0)
        self._scale_reftime = 0.0
        self.rot = 0.0
        self._rot_lasttime = 0.0
        self._rot_ref = 0.0
        self._rot_reftime = 0.0
        self.col = (1.0, 1.0, 1.0, 1.0)
        self._col_lasttime = 0
        self._col_ref = (1.0, 1.0, 1.0, 1.0)
        self._col_reftime = 0
                    
    def setImage(self, image):
        self.currentImage = image
                    
    def loadSheet(self, name, width, height):
        self.images = loadImageSheet(name, width, height)
        self.frameCount = len(self.images)
        self.frameDelays = self.frameCount * [0.1]
        self.currentImage = self.images[0]
        self.width = self.currentImage.width
        self.height = self.currentImage.height

    def calcPos(self, currentTime):
        if (self._pos_reftime <= currentTime):
            return self._pos_ref
        else:    
            factorT = (self._pos_reftime - currentTime) / (self._pos_reftime - self._pos_lasttime)
            return (self._pos_ref[0] - (self._pos_ref[0] - self.pos[0]) * factorT, self._pos_ref[1] - (self._pos_ref[1] - self.pos[1]) * factorT)

    def updatePos(self, currentTime):
        self.pos = self.calcPos(currentTime)
        self._pos_lasttime = currentTime

    def calcCol(self, currentTime):
        if (self._col_reftime <= currentTime):
            return self._col_ref
        else:    
            factorT = (self._col_reftime - currentTime) / (self._col_reftime - self._col_lasttime)
            return (self._col_ref[0] - (self._col_ref[0] - self.col[0]) * factorT, self._col_ref[1] - (self._col_ref[1] - self.col[1]) * factorT, self._col_ref[2] - (self._col_ref[2] - self.col[2]) * factorT, self._col_ref[3] - (self._col_ref[3] - self.col[3]) * factorT)

    def updateCol(self, currentTime):
        self.col = self.calcCol(currentTime)
        self._col_lasttime = currentTime

    def calcScale(self, currentTime):
        if (self._scale_reftime <= currentTime):
            return self._scale_ref
        else:    
            factorT = (self._scale_reftime - currentTime) / (self._scale_reftime - self._scale_lasttime)
            return (self._scale_ref[0] - (self._scale_ref[0] - self.scale[0]) * factorT, self._scale_ref[1] - (self._scale_ref[1] - self.scale[1]) * factorT)

    def updateScale(self, currentTime):
        self.scale = self.calcScale(currentTime)
        self._scale_lasttime = currentTime

    def calcRot(self, currentTime):
        if (self._rot_reftime <= currentTime):
            return self._rot_ref
        else:    
            factorT = (self._rot_reftime - currentTime) / (self._rot_reftime - self._rot_lasttime)
            return self._rot_ref - (self._rot_ref - self.rot) * factorT

    def updateRot(self, currentTime):
        self.rot = self.calcRot(currentTime)
        self._rot_lasttime = currentTime

    def update(self, currentTime): 
        self.updatePos(currentTime)
        self.updateRot(currentTime)
        self.updateCol(currentTime)
        self.updateScale(currentTime)
        
        if (self.frameCount > 0):
            while (self.frameTimer + self.frameDelays[self.frame] <= currentTime):
                self.frameTimer += self.frameDelays[self.frame]
                self.frame += 1
                if self.frame >= self.frameCount:
                    self.frame = 0
                   
            self.currentImage = self.images[self.frame]        
    
    def moveTo(self, pos, currentTime, duration):
        self.updatePos(currentTime)
        self._pos_ref = pos
        self._pos_reftime = currentTime + duration
        
    def setPos(self, pos):
        self._pos_ref = pos
        self.pos = pos
        self._pos_reftime = 0

    def rotateTo(self, rot, currentTime, duration):
        self.updateRot(currentTime)
        self._rot_ref = rot
        self._rot_reftime = currentTime + duration
        
    def setRot(self, rot):
        self._rot_ref = rot
        self.rot = rot
        self._rot_reftime = 0
     
    def scaleTo(self, scale, currentTime, duration):
        self.updateScale(currentTime)
        self._scale_ref = scale
        self._scale_reftime = currentTime + duration
        
    def setScale(self, scale):
        self._scale_ref = scale
        self.scale = scale
        self._scale_reftime = 0
    
    def fadeTo(self, col, currentTime, duration):
        self.updateCol(currentTime)
        self._col_ref = col
        self._col_reftime = currentTime + duration
        
    def setCol(self, col):
        self._col_ref = col
        self.col = col
        self._col_reftime = 0
    