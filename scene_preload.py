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
import thread


from scene_splash import *
from scene_mainmenu import *
from scene_highscore import *


class Scene_Preload(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        self.maingameLoading = False
        self.maingameLoaded = False
        self.mainmenuLoading = False
        self.mainmenuLoaded = False

        self.font = Font("font_normal.png", 8, 8);

        self.gameovertext = Text(160, 100, self.font, "")
        self.gameovertext._layer = 2
        self.gameovertext.setAnchor("center")
        self.gameovertext.setText("LOADING: 0%")

        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240),0,0)
        self.background.fadeTo((0.0,0.0,0.0, 0.7),0,0)
        self.background._layer = 0

        self.sprites.add(self.background)
        self.sprites.add(self.gameovertext)
        
        self.progress = 0
        self.show_progress = 0
        self.done = False
        self.fading = False
        self.timeDone = 0.0
    
    def tick(self):
        perc = int(float(self.show_progress) / 66.0 * 100.0)
        perc = min(perc, 100)
        
        if self.show_progress < self.progress:
            self.show_progress += ((self.progress - self.show_progress + 10.0) / 40.0)
        
        self.gameovertext.setText("LOADING: %d%%" % (perc))
        
        if not self.maingameLoading:
            self.maingameLoading = True
            Scene_MainGame()
            
            def f():
                Scene_MainGame().preload()
                self.maingameLoaded = True
            
            thread.start_new_thread(f, ())
             
        if not self.mainmenuLoading:
            self.mainmenuLoading = True
            Scene_MainMenu()
            
            def f():
                Scene_MainMenu().preload()
                self.mainmenuLoaded = True
            
            thread.start_new_thread(f, ())
        
        if self.maingameLoaded and self.mainmenuLoaded and not self.done:
            self.done = True
            self.timeDone = self.currentTime
        
        if perc >= 100 and not self.fading:
            self.fading = True
            
            def text_fade_done(sprite):
                SceneHandler().removeScene(self)
                SceneHandler().pushScene(Scene_Splash())
                
            self.gameovertext.fadeTo([0.0, 0.0, 0.0, 0.0], self.currentTime, 2.0, text_fade_done)
        
        self.sprites.update(self.currentTime)

    def show(self):
        print self, "is showing"

    def hide(self):
        print self, "is hiding"
        
    def handleEvent(self, event):
        if event.type == EVENT_PRELOADED_PART:
            self.progress += event.count

        
        
