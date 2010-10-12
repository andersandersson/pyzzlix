import os, pygame, board
from pygame.locals import *
from pygame.sprite import *

from math import *

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
from scene_help import *
from scene_dialogyesno import *

from menuitem import *

class MenuItem(Text):
    def __init__(self, x, y, font, label, callfunc):
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
        
        
        
        
class Logo(Sprite):
        class LogoLetter(Sprite):
            def __init__(self, x, y, sx, sy, w, h):
                Sprite.__init__(self)
                self.setImage(loadImage("logo.png", sx, sy, w, h))
                self.setPos((x, y))


        def __init__(self, x, y):
            Sprite.__init__(self)
            self.setImage(loadImage("logo.png", 0, 0, 251, 73))
            self.setPos((x - 251 / 2, y - 73 / 2))
            
            
            self.subSprites.append(self.LogoLetter(0, 0, 0, 80, 48, 80)) # P
            self.subSprites.append(self.LogoLetter(32, 16, 48, 96, 48, 48)) # y   
            self.subSprites.append(self.LogoLetter(48, 16, 96, 96, 80, 48)) # z   
            self.subSprites.append(self.LogoLetter(85, 16, 96, 96, 80, 48)) # z   
            self.subSprites.append(self.LogoLetter(128, 16, 176, 96, 64, 48)) # l   
            self.subSprites.append(self.LogoLetter(176, 0, 0, 160, 16, 64)) # i           
            self.subSprites.append(self.LogoLetter(160, 0, 16, 160, 96, 80)) # x

            self.lastColorChange = 0
            self.colorOrder = 0
      
        def cycleTextColor(self, order, currentTime, length):
            i = order % 25
            R = 0.5+sin((i*3.0+0.0)*1.3)*0.5
            G = 0.5+sin((i*3.0+1.0)*1.3)*0.5
            B = 0.5+sin((i*3.0+2.0)*1.3)*0.5
            color = (R, G, B, 1.0)
            self.setTextColor(color, currentTime, length)
            self.lastColorChange = currentTime
            
        def setTextColor(self, color, currentTime, length):
            for s in self.subSprites:
                s.fadeTo(color, currentTime, length)
 
        def update(self, currentTime):
            if (currentTime - self.lastColorChange > 3.0):
                self.colorOrder += 1
                self.cycleTextColor(self.colorOrder, currentTime, 3.0)
            pass
            
        

class Scene_MainMenu(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        self.menufont = Font("font_fat.png", 8, 8)
        self.textfont = Font("font_clean.png", 4, 8)
        
        self.renderBlocker = True
        self.updateBlocker = True
        
        self.crtext = Text(160, 220, self.textfont, "Copyright Anders Andersson and Joel Lennartsson")
        self.crtext.setAnchor("center")
        self.sprites.add(self.crtext)
    
        self.menuitems = [ MenuItem(160, 100, self.menufont, "Start Game", self.menu_start), 
                             #MenuItem(160, 116, self.menufont, "Options", self.menu_options), 
                             MenuItem(160, 132-16, self.menufont, "High Scores", self.menu_highscores), 
                             MenuItem(160, 148-16, self.menufont, "Help", self.menu_help), 
                             MenuItem(160, 164-16, self.menufont, "Quit", self.menu_quit) ]
                                
        self.menucount = len(self.menuitems)
        self.menufocus = 0
        
        for sprite in self.menuitems:
            self.sprites.add(sprite)

        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240),0,0)
        self.background.fadeTo((0.0,0.0,0.0, 0.7),0,0)
        self.background._layer = 0
        
        self.logo = Logo(170, 50)
        self.logo.setTextColor((1.0, 0.0, 0.0, 1.0), 0, 1.0)
        self.sprites.add(self.logo)        
                
    def preload(self):        
        self.music =  Mixer().loadAudiofile("menumusic.ogg") 
        pygame.event.post(pygame.event.Event(EVENT_PRELOADED_PART, count=2))
        self.movesound =  Mixer().loadAudiofile("menumove.ogg") 
        pygame.event.post(pygame.event.Event(EVENT_PRELOADED_PART, count=2))
        self.selectsound =  Mixer().loadAudiofile("menuselect.ogg") 
        pygame.event.post(pygame.event.Event(EVENT_PRELOADED_PART, count=2))
        
    def tick(self):
        self.ticker += 1
        self.sprites.update(self.currentTime)

    def show(self):
        print self, "is showing"
        self.menuitems[self.menufocus].focus(self.currentTime)
        Mixer().playMusic(self.music)
        
    def hide(self):
        print self, "is hiding"
        Mixer().stopMusic(self.music) 
        
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
            
            if (key == K_RETURN):
                Mixer().playSound(self.selectsound)
                self.menuitems[self.menufocus].select()
            
            if (self.newmenufocus != self.menufocus):
                Mixer().playSound(self.movesound)
                self.menuitems[self.menufocus].unfocus(self.currentTime)
                self.menuitems[self.newmenufocus].focus(self.currentTime)
                self.menufocus = self.newmenufocus

            if (key == K_1):
                Mixer().setVolume(self.music, 0.0, 0.0)
            
            if (key == K_2):
                Mixer().setVolume(self.music, 1.0, 0.0)
            

    def menu_start(self):
        SceneHandler().removeScene(self)
        Scene_MainGame().run()
        pass
    
    def menu_options(self):
        pass
        
    def menu_highscores(self):
        SceneHandler().pushScene(Scene_Highscore())

    def menu_help(self):
        SceneHandler().pushScene(Scene_Help())
        
    def menu_quit(self):
        Mixer().setVolume(self.music, 0.5, 0.5)
        Scene_DialogYesNo().setQuery("Do you want to quit?", self.quitGame, self.doNothing)
        SceneHandler().pushScene(Scene_DialogYesNo())
        #SceneHandler().clear()
        pass
        
    def quitGame(self):
        pygame.event.post(pygame.event.Event(QUIT))
        
        
    def doNothing(self):
        SceneHandler().removeScene(Scene_DialogYesNo())
        Mixer().setVolume(self.music, 1.0, 0.5)
        pass
