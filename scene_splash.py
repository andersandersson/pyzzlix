import os, pygame, board
from pygame.locals import *
from pygame.sprite import *

from math import *

from scene import *
from scenehandler import *
from font import *
from text import *
from sprite import *
from image import *
import random

from scene_maingame import *
from scene_highscore import *

from menuitem import *

class Scene_Splash(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        self.renderBlocker = True
        self.updateBlocker = True
    
        self.splash = Sprite()
        self.splash.setImage(loadImage("splash.png"))
        self.splash.setPos((160, 80))
        self.splash.center = (128, 128)
        self.splash._layer = 0
        
        self.font = Font("font_clean.png", 4, 8)
        self.text1 = Text(160, 140, self.font, "Grumpy Entertainment presents")
        self.text1.setAnchor("center")
        self.text1.setCol((0.0, 0.0, 0.0, 0.0))
        self.text1._layer = 1
        
        self.text2 = Text(160, 140, self.font, "A Game Design Course Project")
        self.text2.setAnchor("center")
        self.text2.setCol((0.0, 0.0, 0.0, 0.0))
        self.text2._layer = 2

        self.sprites.add(self.text1)
        self.sprites.add(self.text2)    
        self.sprites.add(self.splash)
        
    def tick(self):
        self.sprites.update(self.currentTime)
    

    def show(self):
        print self, "is showing"
        self.presents_logofadein(None)
        
    def presents_logofadein(self, sprite) :   
        self.splash.setCol((0.0, 0.0, 0.0, 0.0))
        self.splash.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 4.0, self.presents_textfadein)
        print "logofadein1"
    def presents_textfadein(self, sprite):
        self.text1.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 2.0, self.production_logofadein)
        print "textfadein1"
    def production_logofadein(self, sprite):
        self.text1.fadeTo((1.0, 1.0, 1.0, 0.0), self.currentTime, 4.0, self.production_logofadein)
        self.splash.fadeTo((1.0, 0.0, 0.0, 1.0), self.currentTime, 2.0, self.production_textfadein)
        print "logofadein2"
    def production_textfadein(self, sprite):
        print "textfadein2"
        self.text2.fadeTo((1.0, 0.0, 0.0, 1.0), self.currentTime, 4.0, self.done)
        
    def done(self):  
        self.done = True
  
    def hide(self):
        print self, "is hiding"
        
    def handleEvent(self, event):
        if event.type == KEYDOWN:
            key = event.k
            
            if (key == K_RETURN):
                if (self.done):
                    self.splash.fadeTo((1.0, 0.0, 0.0, 0.0), 0, 5.0)

        return True        
       