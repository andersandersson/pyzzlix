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
from math import *
import random

import scene_maingame

class Scene_Background(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        self.softblend = True

        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png", 1, 1))
        self.background.setScale((320, 240))

        self.bg_image = loadImage("bg_square.png", 128, 128)
        self.squares = []
        for i in xrange(10):
            s = Sprite()
            s.setImage(self.bg_image)
            s.center = (64, 64)
            self.squares.append(s)
         
        for i in xrange(9):
            self.squares[i].subSprites.append(self.squares[i+1])
            self.squares[i+1].setScale((0.95, 0.95))
            self.squares[i+1].velx = 10 + (i % 2) * -20
            self.squares[i+1].vely = 6 + (i % 2) * -12
        
        
        self.squares[0].setScale((3.0, 3.0))
        self.squares[0].setPos((160, 120))
        
        
        self.svx = 40
        self.svy = 40

        self.sprites.add(self.background)
        self.sprites.add(self.squares[0])

        self.updateBlocker = True
        self.renderBlocker = True
      
        self.squares[0].fadeTo((0.2, 1.0, 0.01, 1.0), self.currentTime, 5.0)
        self.background.fadeTo((0.4, 1.0, 0.2, 1.0), self.currentTime, 5.0)
      
   
    def tick(self):
        sx, sy = self.squares[0].pos
        scalex, scaley = self.squares[0].scale
        rot = self.squares[0].rot
    
        if (sx > 240 and self.svx > 0):
            self.svx = -self.svx
            self.squares[0].rotateTo((rot - 360), self.currentTime, 15.0)
            self.squares[0].fadeTo((0.6, 1.0, 0.4, 1.0), self.currentTime, 10.0)
        if (sx < 80 and self.svx < 0):
            self.squares[0].rotateTo((rot - 360), self.currentTime, 15.0)
            self.squares[0].fadeTo((0.2, 1.0, 0.01, 1.0), self.currentTime, 10.0)
            self.svx = -self.svx
        if (sy > 160 and self.svy > 0):
            self.squares[0].rotateTo((rot + 360), self.currentTime, 15.0)
            self.background.fadeTo((0.05, 0.2, 0.01, 1.0), self.currentTime, 10.0)
            self.svy = -self.svy
        if (sy < 80 and self.svy < 0):
            self.squares[0].rotateTo((rot + 360), self.currentTime, 15.0)
            self.background.fadeTo((0.2, 0.6, 0.1, 1.0), self.currentTime, 10.0)
            self.svy = -self.svy
                       
        self.squares[0].moveTo((sx + self.svx, sy + self.svy), self.currentTime, 1.0)
        
        for i in xrange(9):
            j = i + 1
            square = self.squares[j]
            sx, sy = square.pos
            rot = self.squares[j].rot
        
            if (sx > 96 and square.velx > 0):
                square.velx = -square.velx
                square.rotateTo((rot - 360), self.currentTime, 30.0)
            if (sx < 32 and square.velx < 0):
                square.rotateTo((rot - 360), self.currentTime, 30.0)
                square.velx = -square.velx
            if (sy > 96 and square.vely > 0):
                square.rotateTo((rot + 360), self.currentTime, 30.0)
                square.vely = -square.vely
            if (sy < 32 and square.vely < 0):
                square.rotateTo((rot + 360), self.currentTime, 30.0)
                square.vely = -square.vely
                           
            square.moveTo((sx + square.velx, sy + square.vely), self.currentTime, 1.0)
            
            
        
        
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def handleEvent(self, event):
        

        return True
        
