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
from scene_highscore import *
import random

import scene_maingame
import scene_input_text

from menuitem import *
from menu import *

class Scene_GameOver(Scene):
    def _runOnce(self):
        Scene._runOnce(self)

        self.font = Font("font_fat.png", 8, 8);

        self.gameovertext = Text(160, 90, self.font, "GAME OVER")
        self.gameovertext._layer = 2
        self.gameovertext.setAnchor("center")
        self.gameovertext.setScale((3.0,2.0))

        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240),0,0)
        self.background.fadeTo((0.0,0.0,0.0, 0.7),0,0)
        self.background._layer = 0

        self.menu = Menu()
        self.menu.setPos((160, 120))
        self.menu.add(MenuItem(0, 0, self.font, "Play again", self.menu_playAgain))
        self.menu.add(MenuItem(0, 24, self.font, "Exit to menu", self.menu_quit))
        self.menu.setCol((1.0, 1.0, 1.0, 0.0))

        self.highscore_caption = Text(104, 120, self.font, "New highscore!")
        self.highscore_caption.setCol((1.0, 1.0, 1.0, 0.0))

        self.highscore_name = Text(104, 136, self.font, "Initials:")
        self.highscore_name.setCol((1.0, 1.0, 1.0, 0.0))

        self.sprites.add(self.background)
        self.sprites.add(self.gameovertext)
        self.sprites.add(self.menu)
        self.sprites.add(self.highscore_caption)
        self.sprites.add(self.highscore_name)

        self.updateBlocker = True

        self.replay_callback = None
        self.exit_callback = None

        self.statelist = {"showing" : 0, "fading" : 1}
        self.state = self.statelist["showing"]

        self.level = 0
        self.score = 0
        
    def tick(self):
        pass

    def display(self, level=0, score=0, replay_callback=None, exit_callback=None):
        self.menu.setCol((1.0, 1.0, 1.0, 0.0))
        self.highscore_caption.setCol((1.0, 1.0, 1.0, 0.0))
        self.highscore_name.setCol((1.0, 1.0, 1.0, 0.0))        

        self.replay_callback = replay_callback
        self.exit_callback = exit_callback

        self.level = level
        self.score = score

        SceneHandler().pushScene(self)
   
    def showEnterHighscore(self):
        self.highscore_caption.setCol((1.0, 1.0, 1.0, 1.0))
        self.highscore_name.setCol((1.0, 1.0, 1.0, 1.0))

        def text_entered(text):            
            highscore = Scene_Highscore()
            highscore.addNewHighscore(text, self.score, self.level)
            highscore.display(replay_callback=self.replay_callback, exit_callback=self.exit_callback)
            SceneHandler().removeScene(self)

        enter_text = scene_input_text.Scene_InputText()
        enter_text.display(x=180, y=136, length=3, callback=text_entered)

    def showGameOverMenu(self):
        self.menu.setCol((1.0, 1.0, 1.0, 0.0))
        self.menu.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.5)

    def show(self):
        enter_highscore = False

        def fade_done(s):
            self.updateBlocker = True
            self.state = self.statelist["showing"]

            if enter_highscore:
                self.showEnterHighscore()     

        highscore = Scene_Highscore()
        if highscore.isNewHighscore(self.score):
            enter_highscore = True
        else:
            self.showGameOverMenu()
            
        self.menu.focusItem(0)
        self.background.setCol((0.0, 0.0, 0.0, 0.0))
        self.background.fadeTo((0.0, 0.0, 0.0, 0.8), self.currentTime, 0.5, fade_done)
        self.gameovertext.setCol((1.0, 1.0, 1.0, 0.0))
        self.gameovertext.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.5)
        self.state = self.statelist["fading"]
        self.updateBlocker = False
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def fadeOutAndRemove(self):
        def fade_done(s):
            SceneHandler().removeScene(self)
            
        self.menu.fadeTo((1.0, 0.0, 0.0, 0.0), self.currentTime, 0.2)
        self.gameovertext.fadeTo((1.0, 0.0, 0.0, 0.0), self.currentTime, 0.2)
        self.background.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.5, fade_done)
        self.state = self.statelist["fading"]
        self.updateBlocker = False

    def menu_playAgain(self):
        self.fadeOutAndRemove()

        if self.replay_callback:
            self.replay_callback()

    def menu_quit(self):
        self.fadeOutAndRemove()

        if self.exit_callback:
            self.exit_callback()

    def handleEvent(self, event):
        if self.state == self.statelist["fading"]:
            return

        if event.type == KEYDOWN:
            key = event.key

            if (key == K_UP):
                self.menu.prevItem()
                                           
            if (key == K_DOWN):
                self.menu.nextItem()
            
            if (key == K_RETURN):
                Mixer().playSound(self.selectsound)
                self.menu.selectItem()
            
        return True
        
