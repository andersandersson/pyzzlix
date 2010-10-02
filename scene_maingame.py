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
from scene_enter_highscore import *
from scene_highscore import *
from scenehandler import *
import random

LAYER_EFFECTS = 4
LAYER_GUI = 3
LAYER_MARKER = 2
LAYER_BLOCKS = 1

class Scene_MainGame(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        self.state = "running"
        self.board = Board(self, BOARD_WIDTH, BOARD_HEIGHT)
        self.board.setPos((16.0, 16.0))
        self.blocks = pygame.sprite.Group()
        self.blockcount = 0
        self.font = Font("font_normal.png", 8, 8)
        self.background = Sprite()
        self.background.setImage(loadImage("maingame.png", 320, 240))
        self.scorelabeltext = Text(220, 8, self.font, "SCORE:")
        self.scorelabeltext._layer = LAYER_GUI
        self.scoretext = Text(312, 18, self.font, "0")
        self.scoretext._layer = LAYER_GUI
        self.scoretext.setAnchor("right")
        self.levellabeltext = Text(220, 32, self.font, "LEVEL:")
        self.levellabeltext._layer = LAYER_GUI
        self.leveltext = Text(312, 42, self.font, "0")
        self.leveltext._layer = LAYER_GUI
        self.leveltext.setAnchor("right")
        
        self.score = 0
        self.marker = Marker(2,14)
        self.marker._layer = LAYER_MARKER
        self.hourglass = Hourglass()
        self.sprites.add(self.hourglass)
        self.sprites.add(self.board)
        self.sprites.add(self.background)
        self.sprites.add(self.scoretext)
        self.sprites.add(self.leveltext)
        self.sprites.add(self.scorelabeltext)
        self.sprites.add(self.levellabeltext)
        self.sprites.add(self.marker)
        self.ticker = 20
        self.init_counter = 0
        self.init_x = 0
        self.init_x_dir = 0
        self.init_y = 0
        self.init_y_dir = 0
        self.level = 0
        self.block_count = 0
        self.score_level = 0
       
        self.usable_blocks = []
        self.all_blocks = [0, 1, 2, 5, 4, 3]
        
        
        self.resetGame()

    def resetGame(self):
        self.level = 1
        self.score_level = 1
        self.score = 0
        self.block_count = 0
        self.board.reset()
        self.hourglass.reset(HOURGLASS_DEFAULT)
        self.init_x = 0
        self.init_y = BOARD_HEIGHT*2-1
        self.init_x_dir = 1
        self.init_y_dir = -1
        self.usable_blocks = self.all_blocks[0:4]

        self.init_counter = BOARD_WIDTH*BOARD_HEIGHT
        self.sprites.remove_sprites_of_layer(LAYER_BLOCKS)
        self.blocks.empty()

    def showGameOver(self):
        game_over = Scene_GameOver()
        SceneHandler().pushScene(game_over)

    def showEnterHighscore(self):
        enter_highscore = Scene_EnterHighscore()
        enter_highscore.setHighscore(self.score, self.level)
        SceneHandler().pushScene(enter_highscore)

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
                            
    def tick(self):
        self.ticker += 1
        if not self.board.full():
            if self.init_counter > 0:
                self.fillZigZag()
                   
            else:
                for x in range(0, BOARD_WIDTH):
                    for y in range(0, BOARD_HEIGHT):
                        if not self.board.grid[x][y]:
                            self.addRandom(x, y)
        

        self.scoretext.setText(str(self.score))
        self.leveltext.setText(str(self.level))
        
        self.board.updateBoard()
        self.sprites.update(self.currentTime)

    def addRandom(self, x, y):
        if y < self.board.height - 1:
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
        block.animatePopup(self.currentTime)
        
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def addBlockScore(self, block):
        self.score += self.score_level * POINTS_PER_LEVEL_FOR_BLOCK_SCORE

    def addCircleScore(self, blocks):
        num_blocks = len(blocks)
        text_x = 0
        text_y = 0
        text_count = len(blocks)

        self.block_count += num_blocks

        while self.block_count >= self.level * NUM_BLOCKS_FOR_LEVEL:
            self.newLevel()

        score = (num_blocks-MIN_BLOCKS_FOR_CIRCLE_SCORE)*POINTS_PER_LEVEL_FOR_CIRCLE_SCORE*self.score_level
        self.score += score
        self.hourglass.value += (float(num_blocks)*PERCENTAGE_TIME_GIVEN_PER_BLOCK)*self.hourglass.max;

        if not score:
            return

        for block in blocks:
            text_x += block._pos_ref[0]
            text_y += block._pos_ref[1]

        text_x = text_x/text_count + self.board.pos[0] - self.font.width/2*len(str(len(blocks)))
        text_y = text_y/text_count + self.board.pos[1] - self.font.height/2
        text = Text(text_x, text_y, self.font, str(score))
        text._layer = LAYER_EFFECTS
        
        def text_fade_done(sprite):
            self.sprites.remove(text)
                
        def text_scale_done(sprite):
            text.scaleTo([20.0, 20.0], self.currentTime, 0.3)
            text.fadeTo([0.0, 0.0, 0.0, 0.0], self.currentTime, 0.3, text_fade_done)
                
        text.scaleTo([10.0,10.0], self.currentTime, 0.7, text_scale_done)
        text.moveTo([320, -100], self.currentTime, 1.0)
        self.sprites.add(text)

    def sortBlocksZigZag(self, blocks):
        start_y = blocks[0].boardy

        def zig_zag_compare(left, right):
            if not left.boardy == right.boardy:
                return right.boardy - left.boardy

            if not left.boardx == right.boardx:
                if (left.boardy - start_y) % 2 == 0:
                    return right.boardx - left.boardx
                else:
                    return left.boardx - right.boardx

            return 0

        return sorted(blocks, cmp=zig_zag_compare)

    def removeBlocks(self, blocks):
        blocks = self.sortBlocksZigZag(blocks)

        self.hourglass.pause()

        delay = 0.7 / float(len(blocks))

        if delay > 0.08:
            delay = 0.08

        scale_blocks = blocks[:]
        
        def block_scale_done(block):
            if(scale_blocks): 
                self.addBlockScore(block)
                next_block = scale_blocks.pop()
                next_block.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, delay, block_scale_done)
                next_block.rotateTo(720.0, self.currentTime, delay)
                next_block.scaleTo((4.0, 4.0), self.currentTime, 0.5)
            else:
                for block in blocks:
                    self.board.clear(block.boardx, block.boardy)
                self.hourglass.unpause()
                self.score_level = self.level
                    
        def block_wait_done(block):
            block.scaleTo((1.0, 1.0), self.currentTime, 0.5, block_scale_done)

        for block in blocks[:]:
            #block.fadeTo((1.0, 0.0, 0.4, 1.0), self.currentTime, 0.1)
            block.doBlink()

        blocks[-1].fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.5, block_wait_done)

    def newLevel(self):
        self.level += 1

        maxblocks = int(4 + self.level/2)
        if maxblocks > len(self.all_blocks):
            maxblocks = len(self.all_blocks)

        self.usable_blocks = self.all_blocks[0:maxblocks]

        self.hourglass.scaleValue(0.8)
        
        text = Text(160, 90, self.font, "LEVEL: "+str(self.level))

        def text_fade_done(sprite):
            self.sprites.remove(text)

        def text_scale_done(sprite):
            text.scaleTo((4.0, 4.0), self.currentTime, 0.5)
            text.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.5, text_fade_done)
            
        text.setAnchor("center")
        text._layer = LAYER_EFFECTS
        text.scaleTo((2.0, 2.0), self.currentTime, 0.5, text_scale_done)

        self.sprites.add(text)

    def handleEvent(self, event):
        if event.type == board.EVENT_CIRCLE_FOUND:
            self.addCircleScore(event.blocks)
            self.removeBlocks(event.blocks)            

        if event.type == EVENT_GAME_OVER:
            if Scene_Highscore().isNewHighscore(self.score):
                self.showEnterHighscore()
            else:
                self.showGameOver()

        if event.type == EVENT_LEVEL_UP:
            self.newLevel()
        
        if event.type == KEYDOWN or event.type == KEYUP:
            state = event.type
            key = event.key

            if key == K_p:
                print self.board

            if key == K_r:
                self.resetGame()
                
            if key == K_g:
                self.showGameOver()
                
            if key == K_n:
                self.newLevel()

            if key == K_h:
                self.showEnterHighscore()
                
            if (key == K_RIGHT):
                if state == KEYDOWN:
                    if (self.marker.boardx < self.board.width - 2):
                        self.marker.move(1, 0, self.currentTime)
            if (key == K_LEFT):
                if state == KEYDOWN:
                    if (self.marker.boardx > 0):
                        self.marker.move(-1, 0, self.currentTime)
            if (key == K_UP):
                if state == KEYDOWN:
                    if (self.marker.boardy >  self.board.height / 2):
                        self.marker.move(0, -1, self.currentTime)
            if (key == K_DOWN):
                if state == KEYDOWN:
                    if (self.marker.boardy < self.board.height - 2):
                        self.marker.move(0, 1, self.currentTime)

            if (key == K_x):
                if state == KEYDOWN:
                    self.board.rotate(self.marker.boardx, self.marker.boardy, 1, 2)
            if (key == K_z):
                if state == KEYDOWN:
                    self.board.rotate(self.marker.boardx, self.marker.boardy, -1, 2)

        return False
        
