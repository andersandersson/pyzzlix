import os, pygame, board
from pygame.locals import *
from pygame.sprite import *

from math import *

from scene import *
from scenehandler import *
from font import *
from text import *
from sprite import *
from image import *
import random

from scene_maingame import *
from scene_highscore import *

from menuitem import *

class Scene_DialogYesNo(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        
        self.renderBlocker = False
        self.updateBlocker = True
    
        self.query = "This should be a question?"
        self.yesCallback = None
        self.noCallback = None
        
        font = Font("font_fat.png", 8, 8);
        self.querytext = Text(160, 90, font, self.query)
        self.querytext.setAnchor("center")
        self.querytext._layer = 1
        
        self.sprites.add(self.querytext)
        
        self.menuitems = [ MenuItem(140, 100, "Yes", self.yesCallback), 
                             MenuItem(180, 100, "No", self.noCallback)]                             
        self.menucount = len(self.menuitems)
        self.menufocus = 1
        
        for sprite in self.menuitems:
            self.sprites.add(sprite)
            sprite._layer = 1 

        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240), 0, 0)
        self.background._layer = 0        
        self.sprites.add(self.background)
        
        self.movesound =  Mixer().loadAudiofile("menumove.ogg") 
        self.selectsound =  Mixer().loadAudiofile("menuselect.ogg") 
   
    def setQuery(self, query, yescall, nocall):
        self.query = query
        self.yesCallback = yescall
        self.noCallback = nocall
        self.querytext.setText(query)
        self.menuitems[0].callfunc = self.yesCallback
        self.menuitems[1].callfunc = self.noCallback
        
          
    def tick(self):
        self.sprites.update(self.currentTime)

    def show(self):
        print self, "is showing"
        self.menuitems[self.menufocus].focus(self.currentTime)
        self.background.setCol((0.0, 0.0, 0.0, 0.0))
        self.background.fadeTo((0.0, 0.0, 0.0, 1.0), 0, 1.0)
            
    def hide(self):
        print self, "is hiding"
        
    def handleEvent(self, event):
        if event.type == KEYDOWN:
            key = event.key

            self.newmenufocus = self.menufocus
            if (key == K_LEFT):
                self.newmenufocus -= 1
                if (self.newmenufocus < 0):
                    self.newmenufocus = 0
                                           
            if (key == K_RIGHT):
                self.newmenufocus += 1
                if (self.newmenufocus >= self.menucount):
                    self.newmenufocus = self.menucount - 1
            
            if (key == K_RETURN):
                Mixer().playSound(self.selectsound)
                self.menuitems[self.menufocus].select()
                
            
            if (self.newmenufocus != self.menufocus):
                Mixer().playSound(self.movesound)
                self.menuitems[self.menufocus].unfocus(self.currentTime)
                self.menuitems[self.newmenufocus].focus(self.currentTime)
                self.menufocus = self.newmenufocus
        return True        
       