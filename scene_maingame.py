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
from hourglass import *
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
        self.board = Board(BOARD_WIDTH, BOARD_HEIGHT)
        self.blocks = pygame.sprite.Group()
        self.blockcount = 0
        self.font = Font("font_normal.bmp", 8, 8);
        self.background = Image()
        self.background.loadSheet("maingame.bmp", 320, 240)
        self.scoretext = Text(224, 16, self.font, "SCORE: 0")
        self.scoretext._layer = LAYER_GUI
        self.leveltext = Text(224, 38, self.font, "SCORE: 0")
        self.leveltext._layer = LAYER_GUI
        self.score = 0
        self.marker = Marker(2,14)
        self.marker._layer = LAYER_MARKER
        self.sprites.add(self.scoretext)
        self.sprites.add(self.leveltext)
        self.sprites.add(self.marker)
        self.sprites.add(self.background)
        self.ticker = 20
        self.init_counter = 0
        self.init_x = 0
        self.init_x_dir = 0
        self.init_y = 0
        self.init_y_dir = 0
        self.level = 0
        
        self.usable_blocks = [8,9,10,11]#range(0,8)
        
        self.hourglass = Hourglass()
        self.sprites.add(self.hourglass)
        
        self.resetGame()

    def resetGame(self):
        self.level = 1
        self.score = 0
        self.board.reset()
        self.hourglass.reset(HOURGLASS_DEFAULT)
        self.init_x = 0
        self.init_y = BOARD_HEIGHT*2-1
        self.init_x_dir = 1
        self.init_y_dir = -1

        self.init_counter = BOARD_WIDTH*BOARD_HEIGHT
        self.sprites.remove_sprites_of_layer(LAYER_BLOCKS)
        self.blocks.empty()


    def showGameOver(self):
        game_over = Scene_GameOver()
        SceneHandler().pushScene(game_over)

    def fillZigZag(self):
        for i in range(0,4):
            if self.init_counter > 0:
                self.init_counter -= 1
                   
                self.addRandom(self.init_x, self.init_y)
                        
                self.init_x += self.init_x_dir
                        
                if self.init_x >= BOARD_WIDTH:
                    self.init_x_dir = -1
                    self.init_x -= 1
                    self.init_y -= 1
                            
                if self.init_x < 0:
                    self.init_x_dir = 1
                    self.init_x += 1                   
                    self.init_y -= 1
                            
    def tick(self, deltaTime):
        self.ticker += 1

        if not self.board.full():
            if self.init_counter > 0:
                self.fillZigZag()
                   
            else:
                for x in range(0, BOARD_WIDTH):
                    for y in range(0, BOARD_HEIGHT):
                        if not self.board.grid[x][y]:
                            self.addRandom(x, y)
        

        self.scoretext.setText("SCORE: "+str(self.score))
        self.leveltext.setText("LEVEL: "+str(self.level))
        self.board.update()
        self.marker.update(deltaTime)
        self.blocks.update(deltaTime)
        self.background.update(deltaTime)
        self.hourglass.update(deltaTime)
    
    def addRandom(self, x, y):
        if y < BOARD_HEIGHT*2-1:
            type = self.usable_blocks[random.randint(0,len(self.usable_blocks)-1)]
                    
            while(self.board.grid[x][y+1] and self.board.grid[x][y+1].type == type):
                type = self.usable_blocks[random.randint(0,len(self.usable_blocks)-1)]
        else:
            type = self.usable_blocks[random.randint(0,len(self.usable_blocks)-1)]
                
        self.createBlock(x, y, type)
        
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

    def addScore(self, blocks):
        self.score += pow(2,len(blocks)-2)
        self.hourglass.value += pow(len(blocks),2)*10

    def newLevel(self):
        self.level += 1
        print (pow(0.9, self.level-1)*HOURGLASS_DEFAULT)
        self.hourglass.reset(pow(0.9, self.level-1)*HOURGLASS_DEFAULT)

    def handleEvent(self, event):
        if event.type == board.EVENT_CIRCLE_FOUND:
            self.addScore(event.blocks)
            
            for block in event.blocks:
                print block.x, block.y
                block.kill()
                self.board.clear(block.x, block.y)
                self.blocks.remove(block)
                self.sprites.remove(block)

        if event.type == board.EVENT_GAME_OVER:
            self.showGameOver()

        if event.type == board.EVENT_LEVEL_UP:
            self.newLevel()
            
        if event.type == KEYDOWN or event.type == KEYUP:
            state = event.type
            key = event.key

            if key == K_p:
                print self.board

            if key == K_r:
                self.resetGame()
                
            if key == K_n:
                self.newLevel()
                
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
        
