import random
import thread
from time import sleep
import sys

from mixer import *

from scene import *
from board import *
from block import *
from font import *
from text import *
from image import *
from marker import *
from hourglass import *
from scoreboard import *
from scene_gameover import *
from scene_enter_highscore import *
from scene_highscore import *
from background import *
from scene_dialogyesno import *
from scene_mainmenu import *
from scenehandler import *

from levelsplash import *

LAYER_EFFECTS = 4
LAYER_GUI = 3
LAYER_MARKER = 2
LAYER_BLOCKS = 1

class Scene_MainGame(Scene):
    def _runOnce(self):
        Scene._runOnce(self)
        self.renderBlocker = True
        self.updateBlocker = True
        
        self.board = Board(self, BOARD_WIDTH, BOARD_HEIGHT)
        self.board.setPos((8.0, 0.0))
        
        self.scoreboard = Scoreboard()
        self.scoreboard.setPos((208.0, 0.0))
        
        self.blocks = pygame.sprite.Group()
        self.blockcount = 0
        self.font = Font("font_fat.png", 8, 8)
                
        self.music =  []

        self.levelsplash = LevelSplash()
        self.background = Background() 

        self.hourbg = Sprite()
        self.hourbg.setImage(loadImage("pixel.png", 1, 1))
        self.hourbg.setPos((232.0, 119.0))
        self.hourbg.setScale((72.0, 96.0))
        self.hourbg.setCol((0.0, 0.0, 0.0, 0.3))
        self.sprites.add(self.hourbg)
        
        self.hourglass = Hourglass()
        self.hourglass.setPos((232, 119+96))

        self.sprites.add(self.background)
        self.sprites.add(self.hourglass)
        self.sprites.add(self.board)
        self.sprites.add(self.scoreboard)
        
        self.score = 0
        self.ticker = 20
        self.init_counter = 0
        self.init_x = 0
        self.init_x_dir = 0
        self.init_y = 0
        self.init_y_dir = 0
        self.level = 0
        self.block_count = 0
       
        self.usable_blocks = []
        self.all_blocks = [0, 1, 2, 3, 4, 5, 6]
        self.levelMusic = {}
        self.allMusic = []
        self.music_states = []

        self.tutorials = True

        self.statelist = {"idle":0, "running":1, "gameover":2, "levelsplash":3, "welcomesplash":4}
        self.state = self.statelist["idle"]
    
    def preload(self):
        lock = thread.allocate_lock()

        load_list = ["music1_chord.ogg", "music1_hh.ogg", "music1_bass.ogg","music1_kick.ogg","music1_lead2.ogg", "music1_lead.ogg"]
        
        self.allMusic = range(0, len(load_list))
        self.music_states = [0]*len(load_list)
        
        self.levelMusic[1] = [1,2]
        self.levelMusic[3] = [0,1,2]
        self.levelMusic[6] = [0,1,2,3]
        self.levelMusic[9] = [1,2,3,5]
        self.levelMusic[12] = [1,2,3,4,5]
        self.levelMusic[15] = [0,1,2,3,4,5]
        
        music = {}
        count = [0]
        max_count = 0
        
        def load(index, list, count):
            for filename in list:
                file = Mixer().loadAudioStream(filename)
                lock.acquire()
                music[index] = file
                index += 1
                lock.release()
                pygame.event.post(pygame.event.Event(EVENT_PRELOADED_PART, count=10))
                sleep(0.1)
            
            lock.acquire()
            count[0] += 1
            lock.release()
        
        num_threads = 2
        part_size = len(load_list)/num_threads
        for i in range(0,num_threads):
            if i < num_threads-1:
                part_list = load_list[i*part_size:(i+1)*part_size]
            else:
                part_list = load_list[i*part_size:]
            
            thread.start_new_thread(load, (i*part_size, part_list, count))        
            max_count += 1
        
        while count[0] < max_count:
            sleep(0.1)
            
        for m in music:
            self.music.append(music[m])

        self.board.preload()
                               
    def startGame(self):
        self.state = self.statelist["running"]

    def pauseGame(self):
        self.state = self.statelist["idle"]
        
    def show(self):
        print self, "is showing"
        for mus in self.music:
            Mixer().playSound(mus, volume=0.0, loops=-1)
        self.resetGame()
        self.newLevel()
            
    def hide(self):
        print self, "is hiding"
        self.pauseGame()
        for mus in self.music:
            Mixer().stopSound()
        
    def resetGame(self):
        self.level = 0
        self.score = 0
        self.block_count = 0
        self.board.reset()
        self.hourglass.reset(HOURGLASS_DEFAULT)
        self.init_x = 0
        self.init_y = BOARD_HEIGHT*2-1
        self.init_x_dir = 1
        self.init_y_dir = -1
        self.usable_blocks = self.all_blocks[0:3]
        self.init_counter = BOARD_WIDTH*BOARD_HEIGHT
        self.sprites.remove_sprites_of_layer(LAYER_BLOCKS)
        self.blocks.empty()

        self.state = self.statelist["idle"]
        self.playMusicForLevel()

    def showGameOver(self):
        game_over = Scene_GameOver()
        SceneHandler().pushScene(game_over)

    def showEnterHighscore(self):
        enter_highscore = Scene_EnterHighscore()
        enter_highscore.setHighscore(self.score, self.level)
        SceneHandler().pushScene(enter_highscore)

    def playMusicForLevel(self):
        close = self.allMusic[:]
        to_play = []
        for i in self.levelMusic:
            if self.level >= i:
                to_play = self.levelMusic[i]

        for key in to_play:
            if key in close:
                close.remove(key)
                Mixer().setVolume(self.music[key], 1.0, 3.1)
                self.music_states[key] = 1

        for key in close:
            Mixer().setVolume(self.music[key], 0.0, 3.1)
            self.music_states[key] = 0   
        
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
        if (self.state == self.statelist["running"]):
            if not self.board.full():
                if self.init_counter > 0:
                    self.fillZigZag()
                    
                else:
                    for x in range(0, BOARD_WIDTH):
                        for y in range(0, BOARD_HEIGHT):
                            if not self.board.grid[x][y]:
                                self.addRandom(x, y)
                                
            self.scoreboard.updateScoreboard(self.level, self.score)
                                
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

    def addBlockScore(self, block):
        self.score += self.level * POINTS_PER_LEVEL_FOR_BLOCK_SCORE

    def addCircleScore(self, blocks, falling=False):
        num_blocks = len(blocks)
        score = 0
        factor = blocks[0].comboCounter
        text_x = 0
        text_y = 0
        text_count = len(blocks)

        self.block_count += num_blocks

        while self.block_count >= self.level * NUM_BLOCKS_FOR_LEVEL:
            self.newLevel()

        if num_blocks >= MIN_BLOCKS_FOR_CIRCLE_SCORE or falling:
            score = num_blocks*POINTS_PER_LEVEL_FOR_CIRCLE_SCORE*self.level

            if factor:
                score *= factor
            
            self.score += score
        
        perc = (float(num_blocks)*PERCENTAGE_TIME_GIVEN_PER_BLOCK)
        
        self.hourglass.value += perc*self.hourglass.max;
              
        if not score:
            return

        for block in blocks:
            text_x += block._pos_ref[0]
            text_y += block._pos_ref[1]

        text_x = text_x/text_count + self.board.pos[0] - self.font.width/2*len(str(len(blocks)))
        text_y = text_y/text_count + self.board.pos[1] - self.font.height/2
        
        if factor >= 2.0:
            text = Text(text_x, text_y, self.font, str(score/factor) + "X%d" % int(factor))
        else:
            text = Text(text_x, text_y, self.font, str(score))

        text.setAnchor("center")
        text._layer = LAYER_EFFECTS
        
        def text_fade_done(sprite):
            self.sprites.remove(text)
                
        def text_scale_done(sprite):
            #text.scaleTo([20.0, 20.0], self.currentTime, 0.3)
            text.fadeTo([0.0, 0.0, 0.0, 0.0], self.currentTime, 0.3, text_fade_done)
                
        text.scaleTo([5.0,5.0], self.currentTime, 0.7, text_scale_done)
        #text.moveTo([320, -100], self.currentTime, 1.0)
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

        self.hourglass.addPause(len(blocks)*PAUSE_TIME_PER_BLOCK)
        self.hourglass.halt()

        delay = 0.7 / float(len(blocks))

        if delay > 0.08:
            delay = 0.08

        scale_blocks = blocks[:]
        
        def block_scale_done(block):
            if(scale_blocks): 
                Mixer().playSound(self.removeblocksound)
                self.addBlockScore(block)
                next_block = scale_blocks.pop()
                next_block.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, delay, block_scale_done)
                next_block.rotateTo(720.0, self.currentTime, delay)
                next_block.scaleTo((4.0, 4.0), self.currentTime, 0.5)
            else:
                for block in blocks:
                    self.board.clear(block.boardx, block.boardy)
                self.hourglass.unhalt()
                    
        def block_wait_done(block):
            block.scaleTo((1.0, 1.0), self.currentTime, 0.5, block_scale_done)

        for block in blocks[:-1]:
            block.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1)
            block.doBlink()

        blocks[-1].fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, block_wait_done)
        blocks[-1].doBlink()

    def showLevelSplash(self):
        self.sprites.add(self.levelsplash)
        self.levelsplash.display(self.level, self.currentTime, self.tutorials)
        if (self.tutorials):
            self.state = self.statelist["levelsplash"]
            
    def removeLevelSplash(self):
        
        def killSplash(sprite):
            self.sprites.remove(self.levelsplash)
            
        self.levelsplash.hide(self.currentTime, callfunc=killSplash)   
        
    def newLevel(self):
        self.level += 1

        maxblocks = int(4 + self.level/2)
        if maxblocks > len(self.all_blocks):
            maxblocks = len(self.all_blocks)

        self.usable_blocks = self.all_blocks[0:maxblocks]

        self.hourglass.scaleValue(0.8)

        self.showLevelSplash()
        
        #text = Text(160, 90, self.font, "LEVEL: "+str(self.level))

        #def text_fade_done(sprite):
        #    self.sprites.remove(text)

        #def text_scale_done(sprite):
        #    text.scaleTo((4.0, 4.0), self.currentTime, 0.5)
        #    text.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.5, text_fade_done)
            
        #text.setAnchor("center")
        #text._layer = LAYER_EFFECTS
        #text.scaleTo((2.0, 2.0), self.currentTime, 0.5, text_scale_done)
        #self.sprites.add(text)
        

        self.playMusicForLevel()

    def handleEvent(self, event):
        if event.type == EVENT_CIRCLE_FOUND:
            if event.fall_blocks:
                self.addCircleScore(event.fall_blocks, True)
                self.removeBlocks(event.fall_blocks)

            if event.rotation_blocks:
                self.addCircleScore(event.rotation_blocks)
                self.removeBlocks(event.rotation_blocks)

        if event.type == EVENT_GAME_OVER:
            if Scene_Highscore().isNewHighscore(self.score):
                self.showEnterHighscore()
            else:
                self.showGameOver()

        if event.type == EVENT_LEVEL_UP:
            self.newLevel()
        
        if event.type == KEYDOWN:
            state = event.type
            key = event.key

            if key == K_ESCAPE:
                def quit_game():
                    SceneHandler().removeScene(Scene_DialogYesNo())
                    SceneHandler().removeScene(self)

                def do_nothing():
                    SceneHandler().removeScene(Scene_DialogYesNo())
                    
                Scene_DialogYesNo().setQuery("Do you want to exit to the menu?", quit_game, do_nothing)
                SceneHandler().pushScene(Scene_DialogYesNo())

            if (self.state == self.statelist["running"]):
                print "BAD"
                if (key == K_RIGHT):
                    if (self.board.marker.boardx < self.board.width - 2):
                        self.board.marker.move(1, 0, self.currentTime)
                if (key == K_LEFT):
                    if (self.board.marker.boardx > 0):
                        self.board.marker.move(-1, 0, self.currentTime)
                if (key == K_UP):
                    if (self.board.marker.boardy >  self.board.height / 2):
                        self.board.marker.move(0, -1, self.currentTime)
                if (key == K_DOWN):
                    if (self.board.marker.boardy < self.board.height - 2):
                        self.board.marker.move(0, 1, self.currentTime)
                        
                if (key == K_x):
                    if (self.board.rotate(self.board.marker.boardx, self.board.marker.boardy, 1, 2)):
                        self.board.marker.turn()
                    else:
                        self.board.marker.fail()
                if (key == K_z):
                    if (self.board.rotate(self.board.marker.boardx, self.board.marker.boardy, -1, 2)):
                        self.board.marker.turn()
                    else:
                        self.board.marker.fail()
                    
            elif (self.state == self.statelist["levelsplash"]):
                print "LOLOLO"
                if (key == K_RETURN):
                    self.removeLevelSplash()
                    self.startGame()
            elif (self.state == self.statelist["welcomesplash"]):
                if (key == K_RETURN):
                    self.welcomesplash.hide()
                    self.newLevel()

            if key == K_q:
                self.board.pulseBorder((1.0, 0.0, 0.0, 1.0), 0.2)

            if key == K_w:
                self.board.stopPulseBorder()

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

        return True
        
