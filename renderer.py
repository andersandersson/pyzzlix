import scene
from scene import *

import singleton
from singleton import *

class Renderer(Singleton):
    def _runOnce(self):
        self.screen = 0
        
    def setScreen(self, screen):
        self.screen = screen
                
    def render(self, scene):
        if (self.screen != 0):
            scene.sprites.draw(self.screen)

