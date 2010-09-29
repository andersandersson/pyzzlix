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
import random
import json
import zlib
import os.path

import scene_maingame

class Scene_Highscore(Scene):
    def _runOnce(self):
        Scene._runOnce(self)

        self.font = Font("font_normal.png", 8, 8);

        self.titletext = Text(80, 40, self.font, "HIGHSCORES")

        self.background = Sprite()
        self.background.loadSheet("pixel.png", 1, 1)
        self.background.scaleTo((320,240),0,0)
        self.background.fadeTo((0.0,0.0,0.0, 0.7),0,0)
        self.background._layer = 0

        self.sprites.add(self.background)
        self.sprites.add(self.titletext)

        self.updateBlocker = True
        self.highscores = []

        for i in range(0,10):
            self.highscores.append(["AAA", 0, Text(80, 60+i*10, self.font, "AAA: 0")])
            self.sprites.add(self.highscores[i][2])

        self.loadHighscores()

    def loadHighscores(self):
        if not os.path.isfile("pyzzlix.dat"):
            return

        fp = open("pyzzlix.dat", "r")

        try:
            string = zlib.decompress(fp.read())
        except zlib.error:
            string = ""

        if string:
            hs = json.loads(string)
            for obj in zip(hs, self.highscores):
                self.updateHighscore(obj[1], obj[0][0].encode(), obj[0][1])

        fp.close()

    def saveHighscores(self):
        data = []

        for score in self.highscores:
            data.append([score[0], score[1]])

        fp = open("pyzzlix.dat", "w")
        fp.write(zlib.compress(json.dumps(data)))
        fp.close()

    def isNewHighscore(self, highscore):
        for score in self.highscores:
            if score[1] < highscore:
                return True

        return False

    def updateHighscore(self, score, name, highscore):
        score[0] = name
        score[1] = highscore
        score[2].setText(name + ": " + str(highscore))

    def addNewHighscore(self, name, highscore):
        next_score = None

        for score in self.highscores:
            if score[1] < highscore and not next_score:
                next_score = score[:]
                self.updateHighscore(score, name, highscore)

            elif next_score:                
                tmp = score[:]

                self.updateHighscore(score, next_score[0], next_score[1])

                next_score = tmp

        self.saveHighscores()
                

    def tick(self):
        pass        
        
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def handleEvent(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                scene_maingame.Scene_MainGame().resetGame()
                SceneHandler().removeScene(self)            

        return True
        