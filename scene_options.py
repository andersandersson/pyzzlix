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

class Scene_Options(Scene):
    def _runOnce(self):
        def create_scale_menu(font, size=5, width=13, scale_x=1.0, scale_y=1.0, name="", callback=None, update_callback=None):
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

        def create_on_off_menu(font, size=5, width=13, scale_x=1.0, scale_y=1.0, name="", callback=None, update_callback=None):
            menu = Menu()

            def menu_callback_on():
                update_callback(name, "on")
                
            def menu_callback_off():
                update_callback(name, "off")
                
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
        self.menuSprite.setPos((80, 50))
        
        self.menu = Menu()
        self.menu.add(MenuItem(0, 0, self.font, "Music volume", self.focusVolumeMusic, "left"))
        self.menu.add(MenuItem(0, 30, self.font, "Effects volume", self.focusVolumeSound, "left"))
        self.menu.add(MenuItem(0, 60, self.font, "Tutorials", self.focusTutorials, "left"))
        self.menu.add(MenuItem(0, 90, self.font, "Reset highscores", self.resetHighscores, "left"))
        
        self.menuVolumeMusic = create_scale_menu(self.font, callback=self.focusTop, name="music", update_callback=self.updateOptions)
        self.menuVolumeMusic.setPos((20, 13))
        self.menuVolumeMusic.focusItem(10)

        self.menuVolumeSound = create_scale_menu(self.font, callback=self.focusTop, name="sound", update_callback=self.updateOptions)
        self.menuVolumeSound.setPos((20, 43))
        self.menuVolumeSound.focusItem(10)

        self.menuTutorials = create_on_off_menu(self.font, callback=self.focusTop, name="tutorials", update_callback=self.updateOptions)
        self.menuTutorials.setPos((20, 73))
        self.menuTutorials.focusItem(0)
        
        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240), 0, 0)
        self.background.setCol((0.0, 0.0, 0.0, 0.9))
        self.background._layer = 0

        self.menuSprite.subSprites.append(self.menu)
        self.menuSprite.subSprites.append(self.menuVolumeMusic)
        self.menuSprite.subSprites.append(self.menuVolumeSound)
        self.menuSprite.subSprites.append(self.menuTutorials)
        self.sprites.add(self.background)
        self.sprites.add(self.menuSprite)

        self.movesound = Resources().getSound("menumove") 
        self.selectsound = Resources().getSound("menuselect")

        self.statelist = {"top": 1, "music": 2, "sound": 3, "tutorials": 4}
        self.state = self.statelist["top"]

        self.focusColors = {"submenu_focus": self.menu.items[0].focusColor,
                            "submenu_unfocus": (1.0, 0.8, 0.8, 1.0),
                            "topmenu_focus": self.menu.items[0].focusColor,
                            "topmenu_unfocus": (0.8, 0.8, 0.8, 1.0)
                            }

        self.focusScales = {"submenu_focus": (1.2, 1.2),
                            "submenu_unfocus": self.menuVolumeMusic.items[0].focusScale,
                            "topmenu_focus": self.menu.items[0].focusScale,
                            "topmenu_unfocus": (1.3, 1.3)
                            }

        self.submenu = None
        self.options = Resources().getData("options")

        if self.options and "music" in self.options:
            self.menuVolumeMusic.focusItem(self.options["music"])

        if self.options and "sound" in self.options:
            self.menuVolumeSound.focusItem(self.options["sound"])

        if self.options and "tutorials" in self.options:
            if "on" == self.options["tutorials"]:
                self.menuTutorials.focusItem(0)
            else:
                self.menuTutorials.focusItem(1)

    def updateOptions(self, name, value):
        print name, value
        self.options = Resources().getData("options")

        if not self.options:
            self.options = {}

        self.options[name] = value

        Resources().setData("options", self.options)
        Resources().saveData()

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
        pass
    
    def handleEvent(self, event):
        if event.type == KEYDOWN:
            key = event.key

            if self.state == self.statelist["top"]:
                if (key == K_UP):
                    self.menu.prevItem()
                                           
                if (key == K_DOWN):
                    self.menu.nextItem()
            
                if (key == K_RETURN):
                    Mixer().playSound(self.selectsound)
                    self.menu.selectItem()

                if (key == K_RIGHT):
                    self.submenu.nextItem()
                    Mixer().playSound(self.selectsound)
                    self.menu.selectItem()
                                           
                if (key == K_LEFT):
                    self.submenu.prevItem()
                    Mixer().playSound(self.selectsound)
                    self.menu.selectItem()
            else:
                if (key == K_RIGHT):
                    self.submenu.nextItem()
                                           
                if (key == K_LEFT):
                    self.submenu.prevItem()
                    
                if (key == K_RETURN):
                    Mixer().playSound(self.selectsound)
                    self.submenu.selectItem()

                if (key == K_UP):
                    self.menu.prevItem()
                    Mixer().playSound(self.selectsound)
                    self.submenu.selectItem()
                                           
                if (key == K_DOWN):
                    self.menu.nextItem()
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
