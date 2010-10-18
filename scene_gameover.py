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

from menuitem import *
from menu import *

class Scene_GameOver(Scene):
    def _runOnce(self):
        Scene._runOnce(self)

        self.font = Font("font_fat.png", 8, 8);

        self.gameovertext = Text(160, 90, self.font, "GAME OVER!")
        self.gameovertext._layer = 2
        self.gameovertext.setAnchor("center")

        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240),0,0)
        self.background.fadeTo((0.0,0.0,0.0, 0.7),0,0)
        self.background._layer = 0

        self.menu = Menu()
        self.menu.setPos((160, 120))
        self.menu.add(MenuItem(-50, 0, self.font, "Play again", self.menu_playAgain))
        self.menu.add(MenuItem(50, 0, self.font, "Quit", self.menu_quit))

        self.sprites.add(self.background)
        self.sprites.add(self.gameovertext)
        self.sprites.add(self.menu)

        self.updateBlocker = True

        self.callback = None
   
    def tick(self):
        pass
    
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"
        if self.callback:
            self.callback()

    def menu_playAgain(self):
        SceneHandler().removeScene(self)

    def menu_quit(self):
        self

    def handleEvent(self, event):
        if event.type == KEYDOWN:
            key = event.key

            if (key == K_LEFT):
                self.menu.prevItem()
                                           
            if (key == K_RIGHT):
                self.menu.nextItem()
            
            if (key == K_RETURN):
                Mixer().playSound(self.selectsound)
                self.menu.selectItem()
            
        return True
        
