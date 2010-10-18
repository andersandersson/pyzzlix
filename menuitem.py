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
    def __init__(self, x, y, font, label, callfunc):
        Text.__init__(self, x, y, font, label)
        self.callfunc = callfunc
        self._layer = 2
        self.setAnchor("center")
        
        self.setCol((0.6, 0.6, 0.6, 1.0))
        self.setScale((1.0, 1.0))
        self.timer = 0
        self.blinkcount = 0
        self.state = "normal"
    
    def update(self, currentTimer):
        Text.update(self, currentTimer)

        if (self.state == "normal"):
            pass
        elif (self.state == "blinking"):
            self.timer

    def reset(self):
        self.setCol((0.6, 0.6, 0.6, 1.0))
        self.setScale((1.0, 1.0))
            
    def focus(self, currentTime):
        self.fadeTo((1.0, 1.0, 1.0, 1.0), currentTime, 0.1)
        self.scaleTo((1.5, 1.5), currentTime, 0.05)
    
    def unfocus(self, currentTime):
        self.fadeTo((0.6, 0.6, 0.6, 1.0), currentTime, 0.3)
        self.scaleTo((1.0, 1.0), currentTime, 0.1)

    def select(self):
        self.timer = 0
        self.state = "blinking"
        
        if self.callfunc:
            self.callfunc()
        
    
