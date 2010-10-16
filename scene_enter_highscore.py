from scene import *
from scenehandler import *
from board import *
from block import *
from font import *
from text import *
from sprite import *
import random

import scene_highscore

class Scene_EnterHighscore(Scene):
    def _runOnce(self):
        Scene._runOnce(self)

        self.font = Font("font_normal.png", 8, 8);

        self.scoretext = Text(160, 80, self.font, "NEW HIGH SCORE: ")
        self.nametext = Text(160, 100, self.font, "ENTER YOUR INITIALS")
        self.initialstext = Text(160, 120, self.font, "...")
        self.scoretext.setAnchor("center")
        self.nametext.setAnchor("center")
        self.initialstext.setAnchor("center")

        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png"))
        self.background.scaleTo((320,240),0,0)
        self.background.fadeTo((0.0,0.0,0.0, 0.7),0,0)
        self.background._layer = 0

        self.sprites.add(self.background)
        self.sprites.add(self.scoretext)
        self.sprites.add(self.nametext)
        self.sprites.add(self.initialstext)

        self.updateBlocker = True

        self.initials = ""
        self.initials_counter = 0
        self.current_initial = "A"
        
        self.ticker = 0
        self.highscore = 0
        self.level = 0

    ## TODO: Hmm, shouold scenes really have callable functions like this, handle with events?
    def setHighscore(self, highscore, level):
        self.highscore = highscore
        self.level = level
        self.initials = ""
        self.initials_counter = 0
        self.current_initial = "A"
        self.scoretext.setText("NEW HIGH SCORE: "+str(highscore))

    def tick(self):
        text = self.initials

        if self.initials_counter < 3:
            if self.ticker in range(0,5):
                text = text + self.current_initial
            elif self.ticker in range(5, 9):
                text = text + "#"
            else:
                text = text + "#"
                self.ticker = 0
                
            self.ticker += 1

        self.initialstext.setText(text)
                    
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def handleEvent(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                c = ord(self.current_initial)-1
                if c < (ord("A")):
                    c = ord("Z")

                self.current_initial = chr(c)

            if event.key == K_DOWN:
                c = ord(self.current_initial)+1
                if c > (ord("Z")):
                    c = ord("A")

                self.current_initial = chr(c)

            if event.key == K_RETURN:
                if self.initials_counter < 3:
                    self.initials_counter += 1
                    self.initials += self.current_initial

                elif self.initials_counter >= 3:
                    scene_highscore.Scene_Highscore().addNewHighscore(self.initials, self.highscore, self.level)
                    SceneHandler().pushScene(scene_highscore.Scene_Highscore())
                    SceneHandler().removeScene(self)
            

        return True
        
