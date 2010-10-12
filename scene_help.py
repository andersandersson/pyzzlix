import os, pygame, board
from pygame.locals import *
from pygame.sprite import *

from scene import *
from scenehandler import *
from board import *
from block import *
from font import *
from text import *
from sprite import *
from marker import *
import random
import json
import zlib
import os.path

class Scene_Help(Scene):
    def _runOnce(self):
        Scene._runOnce(self)

        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240),0,0)
        self.background.fadeTo((0.0,0.0,0.0, 0.8),0,0)
        self.background._layer = 0
        
        self.anders = Sprite()
        self.anders.setImage(loadImage("anders.png"))
        self.anders.center = (30,40)
        self.anders.setPos((162,96))
        self.anders._layer = 3

        self.angle = 360.0
        def rotate(sprite):
            self.anders.rotateTo(self.angle, self.currentTime, 1.0, rotate)
            self.angle += 360.0
            
        rotate(None)

        def scale_to(sprite):
            self.help.scaleTo((1.05,1.05),self.currentTime, 4.0, scale_from)
            
        def scale_from(sprite):
            self.help.scaleTo((0.95,0.95),self.currentTime, 4.0, scale_to)

        self.help = Sprite()
        self.help.setImage(loadImage("help.png"))
        scale_from(None)
        self.help._layer = 1

        self.sprites.add(self.background)
        self.sprites.add(self.help)
        self.sprites.add(self.anders)

        self.updateBlocker = True
        
    def tick(self):
        self.sprites.update(self.currentTime)        
        
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def handleEvent(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                SceneHandler().removeScene(self)            

        return True
        
