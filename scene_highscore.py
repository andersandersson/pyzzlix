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
from menu import *
from menuitem import *
import random
import json
import zlib
import os.path

import scene_maingame

class Scene_Highscore(Scene):
    def _runOnce(self):
        Scene._runOnce(self)

        self.font = Font("font_fat.png", 8, 8);

        self.titletext = Text(160, 30, self.font, "HIGHSCORES")
        self.titletext.setAnchor("center")
        self.titletext.setScale((2.0, 2.0))

        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.setScale((320,240))
        self.background.setCol((0.0,0.0,0.0, 0.7))
        self.background._layer = 0

        self.updateBlocker = False
        self.highscores = []

        self.menu = Menu()
        self.menu.setPos((160, 180))
        self.menu.add(MenuItem(0, 0, self.font, "Play again", self.menu_playAgain))
        self.menu.add(MenuItem(0, 24, self.font, "Exit to menu", self.menu_quit))
        self.menu.setCol((1.0, 1.0, 1.0, 0.0))

        self.sprites.add(self.background)

        for i in range(0,10):            
            score = ["AAA", 0, 0, Text(160, 60+i*10, self.font, "---"), i]
            self.highscores.append(score)
            self.updateHighscore(score, "AAA", 0, 0)
            self.sprites.add(self.highscores[i][3])            

        self.statelist = {"showing" : 0, "fading" : 1}
        self.state = self.statelist["showing"]
        self.hasMenu = False

        self.sprites.add(self.titletext)
        self.sprites.add(self.menu)
        
        self.menumove = Resources().getSound("menumove")
        self.selectsound = Resources().getSound("menuselect")

        self.loadHighscores()

        self.replay_callback = None
        self.exit_callback = None

    def display(self, rollin=False, replay_callback=None, exit_callback=None):
        self.replay_callback = replay_callback
        self.exit_callback = exit_callback

        if not self.replay_callback and not self.exit_callback:
            self.menu.setCol((1.0, 1.0, 1.0, 0.0))
            self.hasMenu = False
        else:
            self.menu.setCol((1.0, 1.0, 1.0, 1.0))
            self.menu.focusItem(0)
            self.hasMenu = True

        SceneHandler().pushScene(self)
        self.fadeIn(0.5)

    def loadHighscores(self):
        hs = Resources().getData("highscores")

        if not hs:
            return

        print hs
        for obj in zip(hs, self.highscores):
            self.updateHighscore(obj[1], obj[0][0].encode(), obj[0][1], obj[0][2])

    def resetHighscores(self):
        for score in self.highscores:
            self.updateHighscore(score, "AAA", 0, 0)

        self.saveHighscores()
        
    def saveHighscores(self):
        data = []

        for score in self.highscores:
            data.append([score[0], score[1], score[2]])

        Resources().setData("highscores", data)
        Resources().saveData()
            
    def isNewHighscore(self, highscore):
        for score in self.highscores:
            if score[2] < highscore:
                return True

        return False

    def updateHighscore(self, scoreObj, name, highscore, level):
        scoreObj[0] = name
        scoreObj[1] = highscore
        scoreObj[2] = level
        scoreObj[3].setAnchor("center")
        scoreObj[3].setText("%2d. %3s: %10d LVL:%2d" % (scoreObj[4]+1, name, highscore, scoreObj[2]))


    def addNewHighscore(self, name, highscore, level):
        next_score = None

        for score in self.highscores:
            if score[1] < highscore and not next_score:
                next_score = score[:]
                self.updateHighscore(score, name, highscore, level)

            elif next_score:                
                tmp = score[:]

                self.updateHighscore(score, next_score[0], next_score[1], next_score[2])

                next_score = tmp

        self.saveHighscores()
                

    def tick(self):
        pass        
        
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def fadeIn(self, delay):
        self.state = self.statelist["fading"]
        self.updateBlocker = False

        def fade_done(s):
            self.state = self.statelist["showing"]
            self.updateBlocker = True

        self.background.fadeTo((0.0,0.0,0.0, 0.7), self.currentTime, delay, fade_done)
        self.titletext.fadeTo((1.0,1.0,1.0,1.0), self.currentTime, delay)

        for score in self.highscores:
            score[3].fadeTo((1.0,1.0,1.0,1.0), self.currentTime, delay)
        
        if self.hasMenu:
            self.menu.fadeTo((1.0,1.0,1.0,1.0), self.currentTime, delay)

    def fadeOutAndRemove(self):
        def fade_done(s):
            SceneHandler().removeScene(self)

        callback = fade_done
        for sprite in self.sprites:
            sprite.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.2, callback)
            callback = None

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

        if not self.hasMenu:
            if event.type == KEYDOWN:
                if (event.key == K_RETURN or event.key == K_ESCAPE):
                    SceneHandler().removeScene(self)

        if self.hasMenu:
            if event.type == KEYDOWN:
                if (event.key == K_UP):
                    self.menu.prevItem()
                    Mixer().playSound(self.menumove)
                    
                if (event.key == K_DOWN):
                    self.menu.nextItem()
                    Mixer().playSound(self.menumove)
                    
                if (event.key == K_RETURN):
                    Mixer().playSound(self.selectsound)
                    self.menu.selectItem()


                    
        return True
        
