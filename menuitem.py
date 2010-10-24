from math import *

from scene import *
from scenehandler import *
from text import *
from sprite import *
from image import *
import random

from scene_maingame import *
from scene_highscore import *

class MenuItem(Text):
    def __init__(self, x, y, font, label, callfunc, anchor="center"):
        Text.__init__(self, x, y, font, label)
        self.callfunc = callfunc
        self._layer = 2

        self.setAnchor(anchor)
        
        self.timer = 0
        self.blinkcount = 0
        self.state = "normal"

        self.inFocus = False
        self.focusScale = (1.5, 1.5)
        self.focusColor = (1.0, 1.0, 1.0, 1.0)

        self.unfocusScale = (1.0, 1.0)
        self.unfocusColor = (0.6, 0.6, 0.6, 1.0)

        self.setCol(self.unfocusColor)
        self.setScale(self.unfocusScale)
        
    def update(self, currentTimer):
        Text.update(self, currentTimer)

        if (self.state == "normal"):
            pass
        elif (self.state == "blinking"):
            self.timer

    def reset(self):
        self.inFocus = False
        self.setCol(self.unfocusColor)
        self.setScale(self.unfocusScale)
            
    def focus(self, currentTime):
        self.inFocus = True
        self.fadeTo(self.focusColor, currentTime, 0.1)
        self.scaleTo(self.focusScale, currentTime, 0.05)
    
    def unfocus(self, currentTime):
        self.inFocus = False
        self.fadeTo(self.unfocusColor, currentTime, 0.3)
        self.scaleTo(self.unfocusScale, currentTime, 0.1)

    def select(self):
        self.timer = 0
        self.state = "blinking"
        
        if self.callfunc:
            self.callfunc()
        
    
