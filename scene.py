import pygame
from pygame.locals import *
from singleton import *

class Scene(Singleton):
    def _runOnce(self):
        self.currentTime = 0
        self.renderTime = 0
        self.state = 0
        self.done = False
        self.renderBlocker = False
        self.updateBlocker = False
        self.focusable = True
        self.softblend = False
       
        self.sprites = pygame.sprite.LayeredUpdates()
        
    def updateTimer(self, deltaTime):    
        self.currentTime += deltaTime
        self.renderTime = self.currentTime

    def handleEvent(self, event):
        return False
        
    def focus(self):
        #print "Focus not implemented!"
        pass
    def unfocus(self):
        #print "Unfocus not implemented!"
        pass
    def hide(self):
        #print "Hide not implemented!"
        pass
    def show(self):
        #print "Show not implemented!"
        pass
    def isDone(self):
        return self.done == True
        
    def canBeFocused(self):    
        return self.focuable == True
        
    def isBlockingUpdates(self):
        return self.updateBlocker == True
    
    def isBlockingRendering(self):
        return self.renderBlocker == True
