from math import *
from resources import *

from scene import *
from scenehandler import *
from font import *
from text import *
from sprite import *
from image import *
import random

from menu import *
from menuitem import *

class Scene_DialogYesNo(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        
        self.renderBlocker = False
        self.updateBlocker = False
    
        self.query = "This should be a question?"
        self.yesCallback = None
        self.noCallback = None
        
        self.font = Font("font_fat.png", 8, 8);

        self.querytext = Text(0, -10, self.font, self.query)
        self.querytext.setAnchor("center")

        self.menu = Menu()
        self.menu.add(MenuItem(-20, 0, self.font, "Yes", self.yesCallback))
        self.menu.add(MenuItem(20, 0, self.font, "No", self.noCallback))
            
        self.menuSprite = Sprite()        
        self.menuSprite.subSprites.append(self.querytext)
        self.menuSprite.subSprites.append(self.menu)
        self.menuSprite._layer = 1
        self.menuSprite.setPos((160, 100))
            
        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240), 0, 0)
        self.background._layer = 0        
        self.sprites.add(self.background)
        self.sprites.add(self.menuSprite)
        
        self.movesound = Resources().getSound("menumove") 
        self.selectsound = Resources().getSound("menuselect")

        self.statelist = {"showing" : 0, "fading" : 1}
        self.state = self.statelist["showing"]
   
    def setQuery(self, query, yescall, nocall):
        self.query = query
        self.yesCallback = yescall
        self.noCallback = nocall
        self.querytext.setText(query)
        self.menu.items[0].callfunc = self.yesCallback
        self.menu.items[1].callfunc = self.noCallback
        
          
    def tick(self):
        pass

    def show(self):
        for item in self.menu.items:
            item.reset()
            
        self.menu.focusItem(1)
        self.background.setCol((0.0, 0.0, 0.0, 0.0))
        self.background.fadeTo((0.0, 0.0, 0.0, 1.0), self.currentTime, 0.3)
        self.menuSprite.setCol((1.0, 1.0, 1.0, 0.0))
        self.menuSprite.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.2)
        self.state = self.statelist["showing"]
        self.updateBlocker = True

        
    def remove(self, callfunc=None):
        self.menuSprite.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.2)
        self.background.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.5, callfunc)
        self.state = self.statelist["fading"]
        self.updateBlocker = False
        
    def handleEvent(self, event):
        if (self.state == self.statelist["fading"]):
            return False
            
        if event.type == KEYDOWN:
            key = event.key

            if (key == K_LEFT):
                self.menu.prevItem()
                                           
            if (key == K_RIGHT):
                self.menu.nextItem()
            
            if (key == K_RETURN):
                Mixer().playSound(self.selectsound)
                self.menu.selectItem()
                
            if (key == K_ESCAPE):
                Mixer().playSound(self.selectsound)
                self.menu.items[1].select()

        return True
