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
from scene_mainmenu import *

from menuitem import *

class Scene_Splash(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        self.renderBlocker = True
        self.updateBlocker = True
    
        self.splash = Sprite()
        self.splash.setImage(loadImage("splash.png"))
        self.splash.setPos((160, 80))
        self.splash.center = (64, 64)
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
        
        self.fading_out = False
        
    def tick(self):
        self.sprites.update(self.currentTime)
    

    def show(self):
        print self, "is showing"
        self.fading_out = False
        self.presents_logofadein(None)
        
    def presents_logofadein(self, sprite) :   
        self.splash.setCol((0.0, 0.0, 0.0, 0.0))
        self.splash.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 4.0, self.presents_textfadein)
        print "logofadein1"
    def presents_textfadein(self, sprite):
        self.text1.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 4.0, self.production_logofadein)
        print "textfadein1"
    def production_logofadein(self, sprite):
        self.text1.fadeTo((1.0, 1.0, 1.0, 0.0), self.currentTime, 4.0)
        self.splash.fadeTo((1.0, 0.0, 0.0, 1.0), self.currentTime, 3.0, self.production_textfadein)
        print "logofadein2"
    def production_textfadein(self, sprite):
        print "textfadein2"
        self.text2.fadeTo((1.0, 0.0, 0.0, 1.0), self.currentTime, 4.0, self.donefading)
        
    def donefading(self, sprite):
        print "done"
        self.text2.fadeTo((1.0, 0.0, 0.0, 1.0), self.currentTime, 4.0, self.fadeout)
        
    def fadeout(self, sprite):
        print "fadeout"
        self.fading_out = True
        self.text2.fadeTo((0.0, 0.0, 0.0, 1.0), self.currentTime, 4.0)
        self.splash.fadeTo((0.0, 0.0, 0.0, 1.0), self.currentTime, 4.0, self.cleanup)
    
    def cleanup(self, sprite):
        SceneHandler().removeScene(self)
        SceneHandler().pushScene(Scene_MainMenu())
    
    def hide(self):
        print self, "is hiding"
        
    def handleEvent(self, event):
        if event.type == KEYDOWN:
            key = event.key
            
            if (key == K_RETURN):
                if (self.fading_out == False):
                    self.cleanup(None)

        return True        
       