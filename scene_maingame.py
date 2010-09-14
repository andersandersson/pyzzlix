import os, pygame
from pygame.locals import *

from scene import *
from board import *

class Scene_MainGame(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        self.state = "running"
        self.board = Board(32, 20)
   
    def tick(self):
        if (self.state == "running"):
            print self, "is running"
        else:
            print self, "is stopped"
            
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
        
