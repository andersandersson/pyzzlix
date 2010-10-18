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
        self.gameovertext.setScale((3.0,2.0))

        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240),0,0)
        self.background.fadeTo((0.0,0.0,0.0, 0.7),0,0)
        self.background._layer = 0

        self.menu = Menu()
        self.menu.setPos((160, 120))
        self.menu.add(MenuItem(-70, 0, self.font, "Play again", self.menu_playAgain))
        self.menu.add(MenuItem(70, 0, self.font, "Exit to menu", self.menu_quit))

        self.sprites.add(self.background)
        self.sprites.add(self.gameovertext)
        self.sprites.add(self.menu)

        self.updateBlocker = True

        self.replay_callback = None
        self.exit_callback = None

        self.statelist = {"showing" : 0, "fading" : 1}
        self.state = self.statelist["showing"]
   
    def tick(self):
        pass
    
    def show(self):
        self.menu.focusItem(0)
        self.background.setCol((0.0, 0.0, 0.0, 0.0))
        self.background.fadeTo((0.0, 0.0, 0.0, 0.8), self.currentTime, 0.3)
        self.menu.setCol((1.0, 1.0, 1.0, 0.0))
        self.menu.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.2)
        self.gameovertext.setCol((1.0, 1.0, 1.0, 0.0))
        self.gameovertext.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.2)
        self.state = self.statelist["showing"]
        self.updateBlocker = True
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def menu_playAgain(self):
        def fade_done(s):
            SceneHandler().removeScene(self)
            
        self.menu.fadeTo((1.0, 0.0, 0.0, 0.0), self.currentTime, 0.2)
        self.gameovertext.fadeTo((1.0, 0.0, 0.0, 0.0), self.currentTime, 0.2)
        self.background.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.5, fade_done)
        self.state = self.statelist["fading"]
        self.updateBlocker = False

        if self.replay_callback:
            self.replay_callback()

    def menu_quit(self):
        def fade_done(s):
            SceneHandler().removeScene(self)
            
        self.menu.fadeTo((1.0, 0.0, 0.0, 0.0), self.currentTime, 0.2)
        self.gameovertext.fadeTo((1.0, 0.0, 0.0, 0.0), self.currentTime, 0.2)
        self.background.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.5, fade_done)
        self.state = self.statelist["fading"]
        self.updateBlocker = False

        if self.exit_callback:
            self.exit_callback()

    def handleEvent(self, event):
        if self.state == self.statelist["fading"]:
            return

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
        
