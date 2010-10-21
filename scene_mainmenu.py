from math import *

from resources import *
from scene import *
from scenehandler import *
from board import *
from block import *
from font import *
from text import *
from sprite import *
from image import *
import random
import scene_maingame
from scene_maingame import *
from scene_highscore import *
from scene_dialogyesno import *
from scene_options import *

from menu import *
from menuitem import *

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
    
        self.menu = Menu()
        self.menu.setPos((160, 100))
        self.menu.add(MenuItem(0, 0, self.menufont, "Start Game", self.menu_start))
        self.menu.add(MenuItem(0, 16, self.menufont, "High Scores", self.menu_highscores))
        self.menu.add(MenuItem(0, 32, self.menufont, "Options", self.menu_options))
        #self.menu.add(MenuItem(0, 48, self.menufont, "Help", self.menu_help))
        self.menu.add(MenuItem(0, 48, self.menufont, "Quit", self.menu_quit))

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
                
        self.music = Resources().getMusic("menumusic")
        self.menumove = Resources().getSound("menumove")
        self.selectsound = Resources().getSound("menuselect")
        print self.selectsound
        self.startsound = Resources().getSound("menustart")
        
    def tick(self):
        pass

    def show(self):
        print self, "is showing"
        self.state = "entrance"
        Mixer().playMusic(self.music, loops=-1)
        self.startmenu.setPos((160, 160))
        self.startmenu.setCol((1.0,1.0,1.0,0.0))
        self.startmenu.fadeTo((1.0,1.0,1.0,1.0), self.currentTime, 0.3)
        self.startmenu.focus(self.currentTime)
        
    def hide(self):
        print self, "is hiding"
        Mixer().stopMusic(self.music) 
        
    def handleEvent(self, event):
        if event.type == KEYDOWN:
            key = event.key

            if key == K_ESCAPE:
                self.menu_quit()
                
            if (self.state == "menu"):
                if (key == K_UP):
                    Mixer().playSound(self.menumove)
                    self.menu.prevItem()
                                 
                if (key == K_DOWN):
                    Mixer().playSound(self.menumove)
                    self.menu.nextItem()
                    
                    
                if (key == K_RETURN):
                    self.menu.selectItem()
                    
                
            elif (self.state == "entrance"):   
                if (key == K_RETURN):
                    self.startmenu.select()
                    
            

    def menu_enter(self):
        self.state = "transition"
        self.startmenu.moveTo((160, 260), self.currentTime, 0.4, self.menu_enter2)
        self.logo.moveTo((170, 50), self.currentTime, 0.4)
        pass

    def menu_enter2(self, sprite):  
        self.menu.setPos((160, 260))
        self.menu.moveTo((160, 100), self.currentTime, 0.4, self.menu_enter3)
 
    def menu_enter3(self, sprite):  
        self.menu.focusItem(0)
        #self.menuitems[self.menufocus].focus(self.currentTime)
        self.state = "menu" 

    def menu_start(self):
        Mixer().playSound(self.startsound)
        Mixer().stopMusic(self.music)
        SceneHandler().pushScene(scene_maingame.Scene_MainGame())
        pass
    
    def menu_options(self):
        Mixer().playSound(self.selectsound)
        SceneHandler().pushScene(Scene_Options())

    def menu_highscores(self):
        Mixer().playSound(self.selectsound)
        SceneHandler().pushScene(Scene_Highscore())

    def menu_help(self):
        Mixer().playSound(self.selectsound)
        SceneHandler().pushScene(Scene_Help())
        
    def menu_quit(self):
        Mixer().playSound(self.selectsound)
        Mixer().setMusicVolume(self.music, 0.5, 0.5)
        Scene_DialogYesNo().setQuery("Do you want to quit?", self.quitGame, self.doNothing)
        SceneHandler().pushScene(Scene_DialogYesNo())
        pass
      

  
    def quitGame(self):
        pygame.event.post(pygame.event.Event(QUIT))
        
        
    def doNothing(self):
        def killDialog(sprite):
            SceneHandler().removeScene(Scene_DialogYesNo())
        
        Scene_DialogYesNo().remove(killDialog)
        Mixer().setMusicVolume(self.music, 1.0, 0.5)
        pass
