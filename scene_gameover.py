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
from image import *
import random

import scene_maingame

class Scene_GameOver(Scene):
    def _runOnce(self):
        Scene._runOnce(self)

        self.font = Font("font_normal.png", 8, 8);

        self.gameovertext = Text(160, 100, self.font, "GAME OVER!")
        self.gameovertext._layer = 2
        self.gameovertext.setAnchor("center")

        self.gameovertext_2 = Text(160, 120, self.font, "PRESS ANY KEY TO RESTART")
        self.gameovertext_2._layer = 2
        self.gameovertext_2.setAnchor("center")

        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240),0,0)
        self.background.fadeTo((0.0,0.0,0.0, 0.7),0,0)
        self.background._layer = 0

        self.sprites.add(self.background)
        self.sprites.add(self.gameovertext)
        self.sprites.add(self.gameovertext_2)

        self.updateBlocker = True
        self.ready_check = 2
   
    def tick(self):
        self.ticker += 1

        if self.ready_check > 0:
            self.ready_check -= 1
    
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def handleEvent(self, event):
        if event.type == KEYDOWN and self.ready_check == 0:
            scene_maingame.Scene_MainGame().resetGame()
            SceneHandler().removeScene(self)
            

        return True
        
