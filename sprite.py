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
        self._pos_callbacks = []
        self.scale = (1.0, 1.0)
        self._scale_lasttime = 0.0
        self._scale_ref = (1.0, 1.0)
        self._scale_reftime = 0.0
        self._scale_callbacks = []
        self.rot = 0.0
        self._rot_lasttime = 0.0
        self._rot_ref = 0.0
        self._rot_reftime = 0.0
        self.col = (1.0, 1.0, 1.0, 1.0)
        self._col_lasttime = 0
        self._col_ref = (1.0, 1.0, 1.0, 1.0)
        self._col_reftime = 0
        self._col_callbacks = []
        self._in_iter = False
                    
    def setImage(self, image):
        self.currentImage = image
                    
    def loadSheet(self, name, width, height, srcx = 0, srcy = 0, srcw = None, srch = None):
        self.images = loadImageSheet(name, width, height, srcx, srcy, srcw, srch)
        self.frameCount = len(self.images)
        self.frameDelays = self.frameCount * [0.2]
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
        if (self._col_reftime <= currentTime):                    
            if len(self._pos_callbacks):
                callbacks = self._pos_callbacks
                self._pos_callbacks = []
                
                for callback in callbacks:
                    callback=callback()

        self.pos = self.calcPos(currentTime)
        self._pos_lasttime = currentTime

    def calcCol(self, currentTime):
        if (self._col_reftime <= currentTime):                    
            return self._col_ref
        else:    
            factorT = (self._col_reftime - currentTime) / (self._col_reftime - self._col_lasttime)
            return (self._col_ref[0] - (self._col_ref[0] - self.col[0]) * factorT, self._col_ref[1] - (self._col_ref[1] - self.col[1]) * factorT, self._col_ref[2] - (self._col_ref[2] - self.col[2]) * factorT, self._col_ref[3] - (self._col_ref[3] - self.col[3]) * factorT)

    def updateCol(self, currentTime):
        if (self._col_reftime <= currentTime):                    
            if len(self._col_callbacks):
                callbacks = self._col_callbacks
                self._col_callbacks = []
                
                for callback in callbacks:
                    callback=callback()                

        self.col = self.calcCol(currentTime)
        self._col_lasttime = currentTime

    def calcScale(self, currentTime):
        if (self._scale_reftime <= currentTime):
            return self._scale_ref
        else:    
            factorT = (self._scale_reftime - currentTime) / (self._scale_reftime - self._scale_lasttime)
            return (self._scale_ref[0] - (self._scale_ref[0] - self.scale[0]) * factorT, self._scale_ref[1] - (self._scale_ref[1] - self.scale[1]) * factorT)

    def updateScale(self, currentTime):
        if (self._scale_reftime <= currentTime):                    
            if len(self._scale_callbacks):
                callbacks = self._scale_callbacks
                self._scale_callbacks = []
                 
                for callback in callbacks:
                    callback()
                
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

        for sprite in self.subSprites:
            sprite.update(currentTime)
    
    def moveTo(self, pos, currentTime, duration, callback=None):
        self.updatePos(currentTime)
        self._pos_ref = pos
        self._pos_reftime = currentTime + duration

        if callback:
            self._pos_callbacks.append(callback)
        
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
     
    def scaleTo(self, scale, currentTime, duration, callback=None):
        self.updateScale(currentTime)
        self._scale_ref = scale
        self._scale_reftime = currentTime + duration

        if callback:
            self._scale_callbacks.append(callback)
        
    def setScale(self, scale):
        self._scale_ref = scale
        self.scale = scale
        self._scale_reftime = 0
    
    def fadeTo(self, col, currentTime, duration, callback=None):
        self.updateCol(currentTime)
        self._col_ref = col
        self._col_reftime = currentTime + duration
        
        if callback:
            self._col_callbacks.append(callback)
        
    def setCol(self, col):
        self._col_ref = col
        self.col = col
        self._col_reftime = 0
    
    def setFrame(self, frame):
        self.frame = frame
        self.currentImage = self.images[self.frame]
