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

        self.help = Sprite()
        self.help.setImage(loadImage("help.png"))
        self.help._layer = 1

        self.sprites.add(self.background)
        self.sprites.add(self.help)

        self.updateBlocker = True
        
    def tick(self):
        pass        
        
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def handleEvent(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                SceneHandler().removeScene(self)            

        return True
        
