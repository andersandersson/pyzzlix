from math import *

from scene import *
from scenehandler import *
from font import *
from text import *
from sprite import *
from image import *
import random

from menuitem import *

class Scene_DialogYesNo(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        
        self.renderBlocker = False
        self.updateBlocker = True
    
        self.query = "This should be a question?"
        self.yesCallback = None
        self.noCallback = None
        
        self.font = Font("font_fat.png", 8, 8);

        self.menu = Sprite()
        self.menu.setPos((160, 100))
        self.menu._layer = 1

        self.querytext = Text(0, -10, self.font, self.query)
        self.querytext.setAnchor("center")
        self.querytext._layer = 1

        self.menu.subSprites.append(self.querytext)    
        
        self.menuitems = [ MenuItem(-20, 0, "Yes", self.yesCallback), 
                             MenuItem(20, 0, "No", self.noCallback)]                             
        self.menucount = len(self.menuitems)
        self.menufocus = 1
        
        for item in self.menuitems:
            self.menu.subSprites.append(item)
            item._layer = 1
            
        self.sprites.add(self.menu)
            
        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240), 0, 0)
        self.background._layer = 0        
        self.sprites.add(self.background)
        
        self.movesound =  Mixer().loadAudioFile("menumove.ogg") 
        self.selectsound =  Mixer().loadAudioFile("menuselect.ogg") 
   
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
        for item in self.menuitems:
            item.reset()
            
        self.menufocus = 1
        self.menuitems[self.menufocus].focus(self.currentTime)
        self.background.setCol((0.0, 0.0, 0.0, 0.0))
        self.background.fadeTo((0.0, 0.0, 0.0, 1.0), self.currentTime, 0.3)
        self.menu.setCol((1.0, 1.0, 1.0, 0.0))
        self.menu.fadeTo((1.0, 0.0, 0.0, 1.0), self.currentTime, 0.3)

        
    def remove(self, callfunc=None):
        print self, "is hiding"
        self.background.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.5, callfunc)
        self.menu.fadeTo((1.0, 1.0, 1.0, 0.0), self.currentTime, 0.5)
        
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
                
            if (key == K_ESCAPE):
                Mixer().playSound(self.selectsound)
                self.menuitems[1].select()
                
            if (self.newmenufocus != self.menufocus):
                Mixer().playSound(self.movesound)
                self.menuitems[self.menufocus].unfocus(self.currentTime)
                self.menuitems[self.newmenufocus].focus(self.currentTime)
                self.menufocus = self.newmenufocus
        return True        
       
