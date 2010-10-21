from math import *
from resources import *

from scene import *
from scenehandler import *
from scene_dialogyesno import *
from scene_highscore import *
from font import *
from text import *
from sprite import *
from image import *
import random

from menu import *
from menuitem import *
from options import *

class Scene_Options(Scene):
    def _runOnce(self):
        def create_scale_menu(font, size=VOLUME_STEPS, width=13, scale_x=1.0, scale_y=1.0, name="", callback=None, update_callback=None):
            menu = Menu()
            for i in range(0, size+1):
                def menu_callback(value):
                    def _callback():
                        if update_callback:
                            update_callback(name, value)
                            
                        if callback:
                            callback()
                            
                    return _callback
                    
                item = MenuItem(i*width, 0, font, str(i), menu_callback(i), "left")
                item.focusScale = (scale_x, scale_y)
                item.unfocusScale = (scale_x, scale_y)
                menu.add(item)

            return menu

        def create_on_off_menu(font, size=VOLUME_STEPS, width=13, scale_x=1.0, scale_y=1.0, name="", callback=None, update_callback=None):
            menu = Menu()

            def menu_callback_on():
                if update_callback:
                    update_callback(name, True)
                
                if callback:
                    callback()
                
            def menu_callback_off():
                if update_callback:
                    update_callback(name, False)

                if callback:
                    callback()
                
            item = MenuItem(0, 0, font, "On", menu_callback_on, "left")
            item.focusScale = (scale_x, scale_y)
            item.unfocusScale = (scale_x, scale_y)

            menu.add(item)

            item = MenuItem(24, 0, font, "Off", menu_callback_off, "left")
            item.focusScale = (scale_x, scale_y)
            item.unfocusScale = (scale_x, scale_y)

            menu.add(item)

            return menu
        
        Scene._runOnce(self)
        
        self.font = Font("font_fat.png", 8, 8);

        self.menuSprite = Sprite()
        self.menuSprite.setPos((76, 70))
        
        self.menu = Menu()
        self.menu.add(MenuItem(0, 0, self.font, "Music volume", self.focusVolumeMusic, "left"))
        self.menu.add(MenuItem(0, 30, self.font, "Effects volume", self.focusVolumeSound, "left"))
        self.menu.add(MenuItem(0, 60, self.font, "Tutorial", self.focusTutorials, "left"))
        self.menu.add(MenuItem(0, 90, self.font, "Reset highscores", self.resetHighscores, "left"))
        self.menu.add(MenuItem(84, 140, self.font, "Exit", self.closeOptions, "center"))

        
        self.menuVolumeMusic = create_scale_menu(self.font, callback=self.focusTop, name="music_volume", update_callback=self.updateOptions)
        self.menuVolumeMusic.setPos((20, 13))
        self.menuVolumeMusic.focusItem(10)

        self.menuVolumeSound = create_scale_menu(self.font, callback=self.focusTop, name="sound_volume", update_callback=self.updateOptions)
        self.menuVolumeSound.setPos((20, 43))
        self.menuVolumeSound.focusItem(10)

        self.menuTutorials = create_on_off_menu(self.font, callback=self.focusTop, name="show_tutorials", update_callback=self.updateOptions)
        self.menuTutorials.setPos((20, 73))
        self.menuTutorials.focusItem(0)
        
        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240), 0, 0)
        self.background.setCol((0.0, 0.0, 0.0, 0.9))
        self.background._layer = 0

        self.title = Text(160, 30, self.font, "OPTIONS")
        self.title.setScale((2.0, 2.0))
        self.title.setAnchor("center")
        
        self.menuSprite.subSprites.append(self.menu)
        self.menuSprite.subSprites.append(self.menuVolumeMusic)
        self.menuSprite.subSprites.append(self.menuVolumeSound)
        self.menuSprite.subSprites.append(self.menuTutorials)
        self.sprites.add(self.background)
        self.sprites.add(self.menuSprite)
        self.sprites.add(self.title)

        self.movesound = Resources().getSound("menumove") 
        self.selectsound = Resources().getSound("menuselect")

        self.statelist = {"top": 1, "music": 2, "sound": 3, "tutorials": 4}
        self.state = self.statelist["top"]

        self.focusColors = {"submenu_focus": self.menu.items[0].focusColor,
                            "submenu_unfocus": self.menu.items[0].focusColor,
                            "topmenu_focus": self.menu.items[0].focusColor,
                            "topmenu_unfocus": self.menu.items[0].unfocusColor
                            }

        self.focusScales = {"submenu_focus": (1.2, 1.2),
                            "submenu_unfocus": self.menuVolumeMusic.items[0].focusScale,
                            "topmenu_focus": self.menu.items[0].focusScale,
                            "topmenu_unfocus": (1.3, 1.3)
                            }

        self.submenu = None

        music_volume = Options().get("music_volume")
        if music_volume:
            self.menuVolumeMusic.focusItem(music_volume)
        else:
            self.menuVolumeMusic.focusItem(VOLUME_STEPS)

        sound_volume = Options().get("sound_volume")
        if sound_volume:
            self.menuVolumeSound.focusItem(sound_volume)
        else:
            self.menuVolumeSound.focusItem(VOLUME_STEPS)

        if Options().get("show_tutorials"):
            self.menuTutorials.focusItem(0)
        else:
            self.menuTutorials.focusItem(1)
            
    def updateOptions(self, name, value):
        print name, value
        Options().set(name, value)
        
    def tick(self):
        pass

    def show(self):
        self.menu.focusItem(0)
        self.submenu = self.menuVolumeMusic
        pass
    
    def remove(self, callfunc=None):
        pass

    def focusVolumeMusic(self):
        self.menu.setFocusCol(self.focusColors["topmenu_unfocus"])
        self.menu.setFocusScale(self.focusScales["topmenu_unfocus"])
        self.menuVolumeMusic.setFocusCol(self.focusColors["submenu_focus"])
        self.menuVolumeMusic.setFocusScale(self.focusScales["submenu_focus"])
        self.state = self.statelist["music"]

    def focusVolumeSound(self):
        self.menu.setFocusCol(self.focusColors["topmenu_unfocus"])
        self.menu.setFocusScale(self.focusScales["topmenu_unfocus"])
        self.menuVolumeSound.setFocusCol(self.focusColors["submenu_focus"])
        self.menuVolumeSound.setFocusScale(self.focusScales["submenu_focus"])
        self.state = self.statelist["sound"]

    def focusTutorials(self):
        self.menu.setFocusCol(self.focusColors["topmenu_unfocus"])
        self.menu.setFocusScale(self.focusScales["topmenu_unfocus"])
        self.menuTutorials.setFocusCol(self.focusColors["submenu_focus"])
        self.menuTutorials.setFocusScale(self.focusScales["submenu_focus"])
        self.state = self.statelist["tutorials"]

    def focusTop(self):
        self.menuVolumeMusic.setFocusCol(self.focusColors["submenu_unfocus"])
        self.menuVolumeMusic.setFocusScale(self.focusScales["submenu_unfocus"])

        self.menuVolumeSound.setFocusCol(self.focusColors["submenu_unfocus"])
        self.menuVolumeSound.setFocusScale(self.focusScales["submenu_unfocus"])

        self.menuTutorials.setFocusCol(self.focusColors["submenu_unfocus"])
        self.menuTutorials.setFocusScale(self.focusScales["submenu_unfocus"])

        self.menu.setFocusCol(self.focusColors["topmenu_focus"])
        self.menu.setFocusScale(self.focusScales["topmenu_focus"])
        self.state = self.statelist["top"]

    def resetHighscores(self):
        dialog = Scene_DialogYesNo()
        
        def reset_yes():
            Scene_Highscore().resetHighscores()
            SceneHandler().removeScene(dialog)

        def reset_no():
            SceneHandler().removeScene(dialog)

        dialog.setQuery("Really reset highscores?", reset_yes, reset_no)
        SceneHandler().pushScene(dialog)
        pass

    def closeOptions(self):
        SceneHandler().removeScene(self)
    
    def handleEvent(self, event):
        if event.type == KEYDOWN:
            key = event.key

            if self.state == self.statelist["top"]:
                if (key == K_UP):
                    Mixer().playSound(self.movesound)
                    self.menu.prevItem()
                                           
                if (key == K_DOWN):
                    Mixer().playSound(self.movesound)
                    self.menu.nextItem()
            
                if (key == K_RETURN):
                    Mixer().playSound(self.selectsound)
                    self.menu.selectItem()

                #if (key == K_RIGHT):
                    #self.submenu.nextItem()
                    #Mixer().playSound(self.selectsound)
                    #self.menu.selectItem()
                                           
                #if (key == K_LEFT):
                    #self.submenu.prevItem()
                    #Mixer().playSound(self.selectsound)
                    #self.menu.selectItem()

                if (key == K_ESCAPE):
                    Mixer().playSound(self.selectsound)
                    self.closeOptions()
                    
            else:
                if (key == K_RIGHT):
                    Mixer().playSound(self.movesound)
                    self.submenu.nextItem()
                                           
                if (key == K_LEFT):
                    Mixer().playSound(self.movesound)
                    self.submenu.prevItem()
                    
                if (key == K_RETURN):
                    Mixer().playSound(self.selectsound)
                    self.submenu.selectItem()

                #if (key == K_UP):
                    #Mixer().playSound(self.selectsound)
                    #self.submenu.selectItem()
                                           
                #if (key == K_DOWN):
                    #self.menu.nextItem()
                    #Mixer().playSound(self.selectsound)
                    #self.submenu.selectItem()

                if (key == K_ESCAPE):
                    Mixer().playSound(self.selectsound)
                    self.submenu.selectItem()

        for item in self.menu.items:
            if item.inFocus and item == self.menu.items[0]:
                self.submenu = self.menuVolumeMusic
            if item.inFocus and item == self.menu.items[1]:
                self.submenu = self.menuVolumeSound
            if item.inFocus and item == self.menu.items[2]:
                self.submenu = self.menuTutorials
                
        return True
