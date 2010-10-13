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
            self.center = (251 / 2, 73 / 2)
            self.setPos((x, y))
            
            
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
    
        self.menu = Sprite()
        self.menu.setPos((160, 100))
        self.menuitems = [ MenuItem(0, 0, self.menufont, "Start Game", self.menu_start), 
                                    MenuItem(0, 16, self.menufont, "Options", self.menu_options), 
                                    MenuItem(0, 32, self.menufont, "High Scores", self.menu_highscores), 
                                    MenuItem(0, 48, self.menufont, "Help", self.menu_help), 
                                    MenuItem(0, 64, self.menufont, "Quit", self.menu_quit) ]
                                
        self.menucount = len(self.menuitems)
        self.menufocus = 0
        
        for sprite in self.menuitems:
            self.menu.subSprites.append(sprite)
            
        self.sprites.add(self.menu)    
        self.menu.setPos((160, 260))
            
        self.startmenu = MenuItem(160, 160, self.menufont, "Press Enter", self.menu_enter)
        self.sprites.add(self.startmenu)

        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240),0,0)
        self.background.fadeTo((0.0,0.0,0.0, 0.7),0,0)
        self.background._layer = 0
        
        self.logo = Logo(170, 100)
        self.logo.setTextColor((1.0, 0.0, 0.0, 1.0), 0, 1.0)
        self.sprites.add(self.logo)    

        self.music = None
        self.movesound = None
        self.selectsound = None
        self.startsound = None
        self.state = "menu"
        self.state = "transition"
        self.state = "entrance"
                
    def preload(self):        
        self.music =  Mixer().loadAudioStream("menumusic.ogg")
        pygame.event.post(pygame.event.Event(EVENT_PRELOADED_PART, count=2))
        self.movesound =  Mixer().loadAudioFile("menumove.ogg") 
        pygame.event.post(pygame.event.Event(EVENT_PRELOADED_PART, count=2))
        self.selectsound =  Mixer().loadAudioFile("menuselect.ogg") 
        pygame.event.post(pygame.event.Event(EVENT_PRELOADED_PART, count=2))
        self.startsound =  Mixer().loadAudioFile("menustart.ogg") 
        pygame.event.post(pygame.event.Event(EVENT_PRELOADED_PART, count=2))
        
    def tick(self):
        self.ticker += 1
        self.sprites.update(self.currentTime)

    def show(self):
        print self, "is showing"
        self.state = "entrance"
        Mixer().playSound(self.music, loops=-1)
        self.startmenu.setPos((160, 160))
        self.startmenu.setCol((1.0,1.0,1.0,0.0))
        self.startmenu.fadeTo((1.0,1.0,1.0,1.0), self.currentTime, 0.3)
        self.startmenu.focus(self.currentTime)
        
    def hide(self):
        print self, "is hiding"
        Mixer().stopSound(self.music) 
        
    def handleEvent(self, event):
        if event.type == KEYDOWN:
            key = event.key

            if (self.state == "menu"):
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
                    self.menuitems[self.menufocus].select()
                     
                if (self.newmenufocus != self.menufocus):
                    Mixer().playSound(self.movesound)
                    self.menuitems[self.menufocus].unfocus(self.currentTime)
                    self.menuitems[self.newmenufocus].focus(self.currentTime)
                    self.menufocus = self.newmenufocus
                
            elif (self.state == "entrance"):   
                if (key == K_RETURN):
                    self.startmenu.select()
            

    def menu_enter(self):
        self.state = "transition"
        Mixer().playSound(self.startsound)
        self.startmenu.moveTo((160, 260), self.currentTime, 0.4, self.menu_enter2)
        self.logo.moveTo((170, 50), self.currentTime, 0.4)
        pass

    def menu_enter2(self, sprite):  
        self.menu.setPos((160, 260))
        self.menu.moveTo((160, 100), self.currentTime, 0.4, self.menu_enter3)
 
    def menu_enter3(self, sprite):  
        print "HORRAY"
        self.menuitems[self.menufocus].focus(self.currentTime)
        self.state = "menu"
 

    def menu_start(self):
        Mixer().playSound(self.startsound)
        SceneHandler().removeScene(self)
        Scene_MainGame().run()
        pass
    
    def menu_options(self):
        pass
        
    def menu_highscores(self):
        Mixer().playSound(self.selectsound)
        SceneHandler().pushScene(Scene_Highscore())

    def menu_help(self):
        Mixer().playSound(self.selectsound)
        SceneHandler().pushScene(Scene_Help())
        
    def menu_quit(self):
        Mixer().playSound(self.selectsound)
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
