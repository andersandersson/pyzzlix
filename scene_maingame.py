from globals import *
import os, pygame, board
from pygame.locals import *

from scene import *
from board import *
from block import *
from font import *
from text import *
from image import *
from marker import *
from scene_gameover import *
from scenehandler import *
import random

LAYER_GUI = 3
LAYER_MARKER = 2
LAYER_BLOCKS = 1

class Scene_MainGame(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        self.state = "running"
        self.board = Board(12, 13)
        self.blocks = pygame.sprite.Group()
        self.blockcount = 0
        self.font = Font("font_normal.bmp", 8, 8);
        self.background = Image()
        self.background.loadSheet("maingame.bmp", 320, 240)
        self.scoretext = Text(224, 16, self.font, "SCORE: 0")
        self.scoretext._layer = LAYER_GUI
        self.score = 0
        self.marker = Marker(2,14)
        self.marker._layer = LAYER_MARKER
        self.sprites.add(self.scoretext)
        self.sprites.add(self.marker)
        self.sprites.add(self.background)
        self.ticker = 20
        self.init_done = False

    def resetGame(self):
        self.score = 0
        self.board.reset()
        self.sprites.remove_sprites_of_layer(LAYER_BLOCKS)
        self.blocks.empty()

    def showGameOver(self):
        game_over = Scene_GameOver()
        SceneHandler().pushScene(game_over)

    def tick(self, deltaTime):
        self.ticker += 1

        for i in range(1,4):
            if (self.state == "creating") or self.ticker > 5 or not self.init_done:
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
                    self.init_ticker -= 1
                    self.blockcount+=1

        self.scoretext.setText("SCORE: "+str(self.score))
        self.board.update()
        self.marker.update(deltaTime)
        self.blocks.update(deltaTime)
        self.background.update(deltaTime)
    
    def createBlock(self, x, y, type):
        block = Block(x, y, type)
        block._layer = LAYER_BLOCKS
        self.board.add(x, y, block)
        self.blocks.add(block)
        self.sprites.add(block)
        
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def handleEvent(self, event):
        if event.type == board.EVENT_CIRCLE_FOUND:
            self.score += pow(2,len(event.blocks)-2)

            for block in event.blocks:
                print block.x, block.y
                block.kill()
                self.board.clear(block.x, block.y)
                self.blocks.remove(block)
                self.sprites.remove(block)

        if event.type == board.EVENT_GAME_OVER:
            self.init_done = True
            #self.showGameOver()

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
        
