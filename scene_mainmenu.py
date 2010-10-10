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

from scene_maingame import *
from scene_highscore import *

class MenuItem(Text):
    def __init__(self, x, y, label, callfunc):
        font = Font("font_fat.png", 8, 8);
        Text.__init__(self, x, y, font, label)
        self.callfunc = callfunc
        self._layer = 2
        self.setAnchor("center")
        
        self.setCol((0.6, 0.6, 0.6, 1.0))
        self.setScale((1.0, 1.0))
    
    def focus(self, currentTime):
        self.fadeTo((1.0, 1.0, 1.0, 1.0), currentTime, 0.1)
        self.scaleTo((1.5, 1.5), currentTime, 0.1)    
    
    def unfocus(self, currentTime):
        self.fadeTo((0.6, 0.6, 0.6, 1.0), currentTime, 0.3)
        self.scaleTo((1.0, 1.0), currentTime, 0.3)

    def select(self):
        self.callfunc()

class Scene_MainMenu(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        
        self.renderBlocker = True
        self.updateBlocker = True
    
        self.menuitems = [ MenuItem(160, 100, "Start Game", self.menu_start), 
                             MenuItem(160, 116, "Options", self.menu_options), 
                             MenuItem(160, 132, "High Scores", self.menu_highscores), 
                             MenuItem(160, 148, "Credits", self.menu_credits), 
                             MenuItem(160, 164, "Quit", self.menu_quit) ]
                                
        self.menucount = len(self.menuitems)
        self.menufocus = 0
        
        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240),0,0)
        self.background.fadeTo((0.0,0.0,0.0, 0.7),0,0)
        self.background._layer = 0

        for sprite in self.menuitems:
            self.sprites.add(sprite)
        
   
    def tick(self):
        self.ticker += 1

    def show(self):
        print self, "is showing"
        self.menuitems[self.menufocus].focus(self.currentTime)
        
        
    def hide(self):
        print self, "is hiding"

    def handleEvent(self, event):
        if event.type == KEYDOWN:
            key = event.key

            self.newmenufocus = self.menufocus
            if (key == K_UP):
                self.newmenufocus -= 1
                if (self.newmenufocus < 0):
                    self.newmenufocus = 0
                                           
            if (key == K_DOWN):
                self.newmenufocus += 1
                if (self.newmenufocus >= self.menucount):
                    self.newmenufocus = self.menucount - 1
                print self.menufocus, self.newmenufocus
            
            if (key == K_RETURN):
                self.menuitems[self.menufocus].select()
            
            if (self.newmenufocus != self.menufocus):
                print self.menufocus
                self.menuitems[self.menufocus].unfocus(self.currentTime)
                self.menuitems[self.newmenufocus].focus(self.currentTime)
                self.menufocus = self.newmenufocus
        
            
    def menu_start(self):
        Scene_MainGame().resetGame()
        SceneHandler().removeScene(self)
        pass
    
    def menu_options(self):
        pass
        
    def menu_highscores(self):
        SceneHandler().pushScene(Scene_Highscore())
        pass

    def menu_credits(self):
        pass
        
    def menu_quit(self):
        SceneHandler().clear()
        pass
        
        
