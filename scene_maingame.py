import os, pygame
from pygame.locals import *

import scene
from scene import *

class Scene_MainGame(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        self.state = "running"
   
    def tick(self):
        if (self.state == "running"):
            print self, "is running"
            
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def handleKeyInput(self, key, state):
        if state == KEYDOWN:
            if (key == K_RETURN):
                if (self.state == "stopped"):
                    self.state = "running"
                else:
                    self.state = "stopped"
                return True
        return False
        