import os, pygame, board
from pygame.locals import *

from scene import *
from board import *
from block import *
from font import *
from text import *
from marker import *
import random

class Scene_MainGame(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        self.state = "running"
        self.board = Board(20, 15)
        self.blocks = pygame.sprite.Group()
        self.blockcount = 0
        self.font = Font("font_normal.bmp", 8, 8);
        self.scoretext = Text(0, 0, self.font, "SCORE: 1234567890")
        self.scoretext._layer = 2
        self.marker = Marker(0,0)
        self.marker._layer = 2
        self.sprites.add(self.scoretext)
        self.sprites.add(self.marker)
        self.blocks.add(self.marker)
        self.ticker = 0
   
    def tick(self, deltaTime):
        self.ticker += 1
        if (self.state == "creating") or self.ticker == 100:
            self.ticker = 0
            c = 0
            while True:
                c += 1
                if c > 100:
                    break
                
                x = random.randint(0, self.board.width-1)
                y = 0

                if not self.board.grid[x][y]:
                    break;                
            
            if c < 100:                
                self.createBlock(x, y, random.randint(0, 7))

            self.blockcount+=1
        
        self.board.update()
        self.blocks.update(deltaTime)
    
    def createBlock(self, x, y, type):
        block = Block(x, y, type)
        block._layer = 1
        self.board.add(x, y, type, block)
        self.blocks.add(block)
        self.sprites.add(block)
        
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def handleEvent(self, event):
        if event.type == board.EVENT_CIRCLE_FOUND:
            for block in event.blocks:
                print block.x, block.y
                self.board.clear(block.x, block.y)
                self.blocks.remove(block)
                self.sprites.remove(block)

        if event.type == KEYDOWN or event.type == KEYUP:
            state = event.type
            key = event.key

            if (key == K_RETURN):
                if state == KEYDOWN:
                    if (self.state == "running"):
                        self.state = "creating"
                else:
                    if (self.state == "creating"):
                        self.state = "running"                     
                        print self.blockcount
                return True

            if key == K_p:
                print self.board

            if (key == K_RIGHT):
                if state == KEYDOWN:
                    self.marker.move(1,0)
            if (key == K_LEFT):
                if state == KEYDOWN:
                    self.marker.move(-1,0)
            if (key == K_UP):
                if state == KEYDOWN:
                    self.marker.move(0,-1)
            if (key == K_DOWN):
                if state == KEYDOWN:
                    self.marker.move(0,1)

            if (key == K_x):
                if state == KEYDOWN:
                    self.board.rotate(self.marker.x, self.marker.y, 1, 2)
            if (key == K_z):
                if state == KEYDOWN:
                    self.board.rotate(self.marker.x, self.marker.y, -1, 2)

        return False
        
