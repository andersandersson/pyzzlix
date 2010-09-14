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
            for layer in scene.sprites.layers():
                for sprite in scene.sprites.get_sprites_from_layer(layer):
                    sprite.draw(self.screen)

