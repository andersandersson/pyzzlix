import os, pygame
from pygame.locals import *
from scene import *
from block import *
from font import *
from text import *
import random

class Scene_MainGame(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        self.state = "running"
        self.blocks = pygame.sprite.Group()
        self.blockcount = 0
        self.font = Font("font_normal.bmp", 8, 8);
        self.scoretext = Text(0, 0, self.font, "SCORE: 1234567890")
        self.sprites.add(self.scoretext);
   
    def tick(self, deltaTime):
        if (self.state == "creating"):
            self.createBlock(random.randint(-16, 320), random.randint(-16, 240), random.randint(0, 7))
            self.blockcount+=1
            
        self.blocks.update(deltaTime)
    
    def createBlock(self, x, y, type):
        block = Block(x, y, type)
        self.blocks.add(block)
        self.sprites.add(block)
        
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def handleKeyInput(self, key, state):
        
        if (key == K_RETURN):
            if state == KEYDOWN:
                if (self.state == "running"):
                    self.state = "creating"
            else:
                if (self.state == "creating"):
                    self.state = "running"                     
                    print self.blockcount
            return True
        return False
        