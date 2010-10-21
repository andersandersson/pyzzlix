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
import random
import block

from scene_dialogyesno import *
import scene_maingame
import scene_mainmenu
from levelboard import *
from hourglass import *
import marker

def createBlockGroup(posx, posy, types, size):
    blocks = []
    for i in range(size):
        for j in range(size):
            b = Block(j, i, types[i*size + j], (posx, posy))
            blocks.append(b)
    return blocks
                 
def getBlock(blocks, x, y, size):
    return blocks[y * size + x]

def setBlock(blocks, x, y, size, block):
    blocks[y * size + x] = block
   
def rotateBlocksInGroup(blocks, blockx, blocky, size, currentTime, left=True):
    block1 = getBlock(blocks, blockx - 1, blocky - 1, size) 
    block2 = getBlock(blocks, blockx, blocky - 1, size)
    block3 = getBlock(blocks, blockx - 1, blocky, size)
    block4 = getBlock(blocks, blockx, blocky, size)
             
    if (left == True):
        block1.moveToBoardCoord(block1.boardx,
                                block1.boardy + 1, currentTime)
        block2.moveToBoardCoord(block2.boardx - 1,
                                block2.boardy, currentTime)
        block3.moveToBoardCoord(block3.boardx + 1,
                                block3.boardy, currentTime)
        block4.moveToBoardCoord(block4.boardx,
                                block4.boardy - 1, currentTime)
    else:
        block1.moveToBoardCoord(block1.boardx + 1,
                                block1.boardy, currentTime)
        block2.moveToBoardCoord(block2.boardx,
                                block2.boardy + 1, currentTime)
        block3.moveToBoardCoord(block3.boardx,
                                block3.boardy - 1, currentTime)
        block4.moveToBoardCoord(block4.boardx - 1,
                                block4.boardy, currentTime)
        
    setBlock(blocks, block1.boardx, block1.boardy, size, block1)
    setBlock(blocks, block2.boardx, block2.boardy, size, block2)
    setBlock(blocks, block3.boardx, block3.boardy, size, block3)
    setBlock(blocks, block4.boardx, block4.boardy, size, block4)

    
class Page(Sprite):
    def __init__(self, x, y, page, pageCount):
        Sprite.__init__(self)
        
        self.titlefont = Font("font_fat.png", 8, 8);
        self.textfont = Font("font_clean.png", 4, 8);
   
        self.background = Sprite()
        self.background.setImage(loadImage("splashbg.png"))
        self.setPos((x, y))
        self.width = 196
        self.height = 166
        self.center = (self.width/2, self.height/2)
        
        self.subSprites.append(self.background)

        self.entertext = Text(self.width/2, self.height - 12, self.textfont, "Press Enter to start the game") 
        self.entertext.setAnchor("center")
        
        self.subSprites.append(self.entertext)

        self.leftarrow = Text(4, self.height/2 - 4, self.titlefont, "<")
        self.rightarrow = Text(self.width - 12, self.height/2 - 4, self.titlefont, ">")
        
        self.subSprites.append(self.leftarrow)
        self.subSprites.append(self.rightarrow)


        self.pagetext = Text(self.width - 6, self.height - 12, self.titlefont, "%d/%d" % (page, pageCount))
        self.pagetext.setAnchor("right")

        self.subSprites.append(self.pagetext)

        def fadeInEnterText(sprite):
            self.entertext.fadeTo((1.0,1.0,1.0,1.0), self.currentTime, 0.5, fadeOutEnterText)    

        def fadeOutEnterText(sprite):    
            self.entertext.fadeTo((0.0,0.0,0.0,0.0), self.currentTime, 0.5, fadeInEnterText)    

        self.entertext.fadeTo((0.0,0.0,0.0,0.0), 0, 0.5, fadeInEnterText)    
        self.setCol((1.0,1.0,1.0,0.0))

        
class Page_Welcome(Page):
    def __init__(self, x, y, page, pageCount):
        Page.__init__(self, x, y, page, pageCount)

        dposx = self.width/2
        dposy = 10

        self.welcometext = Text(dposx, dposy, self.titlefont, "WELCOME\nTO\n")
        self.welcometext.setAnchor("center")
        self.welcometext.setScale((1.5, 1.5))

        self.logo = scene_mainmenu.Logo(self.width/2, 46)
        self.logo.setScale((0.5, 0.5))
        self.logo.cycling = False
        
        self.subSprites.append(self.welcometext)
        self.subSprites.append(self.logo)
        
        dposy += 60

        self.infotext = []
        self.infotext.append(Text(dposx, dposy, self.textfont,
                                  "This tutorial will explain how to play\n" +
                                  "Pyzzlix! If this is your first time\n" +
                                  "playing, skip this at your own peril..."))

        dposy += 32

        self.infotext.append(Text(dposx, dposy, self.textfont,
                                  "Use the left and right ARROW keys to\n" + 
                                  "navigate the pages of this tutorial."))
                  
        dposy += 24                        
                                  
        self.infotext.append(Text(dposx, dposy, self.textfont,
                                  "You can choose whether or not to display\n" +
                                  "this tutorial from the options menu."))   
        for t in self.infotext:
            t.setAnchor("center")
            self.subSprites.append(t)
        
    def show(self, currentTime):
        pass

    def hide(self):
        pass
        
class Page_Controls(Page):
    def __init__(self, x, y, page, pageCount):
        Page.__init__(self, x, y, page, pageCount)

        dposx = self.width/2
        dposy = 10

        
        self.titletext = Text(dposx, dposy, self.titlefont, "BASIC CONTROLS")
        self.titletext.setAnchor("center")
        self.titletext.setScale((1.5, 1.5))
        self.subSprites.append(self.titletext)

        dposy += 15
        
        self.infotext = []
        self.infotext.append(Text(dposx, dposy, self.textfont,
                             "When playing the game, use the\n" +
                             "ARROW keys to move the marker."))

        dposy += 35
        
        self.marker = Marker()
        self.marker.setPos((dposx - 16, dposy - 16))
        self.subSprites.append(self.marker)


        dposy += 18        
        self.infotext.append(Text(dposx, dposy, self.textfont,
                             "The Z and X keys rotates the blocks\n" +
                                  "beneath the marker."))

        dposy += 36


        self.blocktypes = [0, 1,
                      2, 0]
        self.blockspos = (dposx - 8, dposy - 8)          

        
        self.marker2 = Marker()
        self.marker2.setPos((dposx - 16, dposy -16))


        dposy += 18
        
        self.infotext.append(Text(dposx, dposy, self.textfont,
                                  "Z rotates counter-clockwise\n" +
                                  "and X rotates clockwise."))
        
        for t in self.infotext:
            t.setAnchor("center")
            self.subSprites.append(t)
            
    def showInit(self):        
        self.blocks = createBlockGroup(self.blockspos[0], self.blockspos[1], self.blocktypes, 2)
        for b in self.blocks:
            self.subSprites.append(b)
            
        self.subSprites.append(self.marker2)

    def show(self, currentTime):
        self.showInit()
     
        def turnLeft(sprite):
            rotateBlocksInGroup(self.blocks, 1, 1, 2, self.currentTime, True)
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.0, turnRight)

            
        def turnRight(sprite):
            rotateBlocksInGroup(self.blocks, 1, 1, 2, self.currentTime, False)
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.0, turnLeft) 

        self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), currentTime, 1.0, turnLeft)    

    def hide(self):
        self.marker2.clearColCallbacks()
        for b in self.blocks:
            self.subSprites.remove(b)
        
        self.subSprites.remove(self.marker2)
        pass
            
        
class Page_Goal(Page):
    def __init__(self, x, y, page, pageCount):
        Page.__init__(self, x, y, page, pageCount)

        dposx = self.width/2
        dposy = 10

        
        self.titletext = Text(dposx, dposy, self.titlefont, "THE GOAL")
        self.titletext.setAnchor("center")
        self.titletext.setScale((1.5, 1.5))
        self.subSprites.append(self.titletext)

        dposy += 15
        
        self.infotext = []
        self.infotext.append(Text(dposx, dposy, self.textfont,
                             "The goal of the game is to get a high\n" +
                             "score before the time runs out."))

        dposy += 24
        
        self.infotext.append(Text(dposx, dposy, self.textfont,
                             "Score and extended time are awarded by\n" +
                             "removing blocks. Remove blocks by\n" +
                             "creating loops of same-colored blocks!"))

        dposy += 56

        self.blocktypes = [0, 0, 1,
                      0, 2, 0,
                      2, 1, 2]
        self.blockspos = (dposx - 16, dposy - 16)         
                      

        self.marker2 = Marker()
        self.marker2.setPos((dposx - 8, dposy - 8))


        dposy += 30
        
        self.infotext.append(Text(dposx, dposy, self.textfont,
                                  "The simplest loop is a 2x2 square.\n"))
 
                                         
        for t in self.infotext:
            t.setAnchor("center")
            self.subSprites.append(t)

    def showInit(self):  
        self.blocks = createBlockGroup(self.blockspos[0], self.blockspos[1], self.blocktypes, 3)

        for b in self.blocks:
            self.subSprites.append(b)
        
        self.subSprites.append(self.marker2)

    def show(self, currentTime):
        self.showInit()
 
        for b in self.blocks:
                b.doNormal()

        
        def turnLeft(sprite):
            rotateBlocksInGroup(self.blocks, 2, 2, 3, self.currentTime, True)
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.5, doBlink)

            
        def turnRight(sprite):
            for i in range(3):
                for j in range(3):
                    self.blocks[i * 3 + j].doNormal()
                    
            rotateBlocksInGroup(self.blocks, 2, 2, 3, self.currentTime, False)
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.0, turnLeft)

        def doBlink(sprite):
            getBlock(self.blocks, 0, 0, 3).doBlink()
            getBlock(self.blocks, 1, 0, 3).doBlink()
            getBlock(self.blocks, 0, 1, 3).doBlink()            
            getBlock(self.blocks, 1, 1, 3).doBlink()

            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.5, turnRight)
            
            
        self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), currentTime, 1.0, turnLeft)    

    def hide(self):
        self.marker2.clearColCallbacks()
        
        for b in self.blocks:
            self.subSprites.remove(b)
        
        self.subSprites.remove(self.marker2)
        pass


        
class Page_Level(Page):
    def __init__(self, x, y, page, pageCount):
        Page.__init__(self, x, y, page, pageCount)

        dposx = self.width/2
        dposy = 10

        
        self.titletext = Text(dposx, dposy, self.titlefont, "LEVELS")
        self.titletext.setAnchor("center")
        self.titletext.setScale((1.5, 1.5))
        self.subSprites.append(self.titletext)

        dposy += 15
        
        self.infotext = []
        self.infotext.append(Text(dposx, dposy, self.textfont,
                             "Each level has a Special Block color.\n" +     
                             "In order to advance to the next level\n" +
                             "a specific number of Special Blocks\n" +
                             "needs to be removed."))

        dposy += 36
        
        self.infotext.append(Text(dposx, dposy, self.textfont,
                             "The Special Block and the progress of\n" +
                             "the current level is displayed in the\n" +
                             "level board."))
 
        dposy += 26

        self.level = 1
        self.levelwindow = Levelboard()
        self.levelwindow.setPos((dposx - 44, dposy))
        self.subSprites.append(self.levelwindow)

        dposy += 50

        self.infotext.append(Text(dposx, dposy, self.textfont,
                             "You will score more points for each removed\n" +
                             "block on higher levels!"))
        
        for t in self.infotext:
            t.setAnchor("center")
            self.subSprites.append(t)
            
    def showInit(self):   
        self.level = 1
        self.levelwindow.setNewLevel(1, 0, 20)


    def show(self, currentTime):
        self.showInit()
        
        self.blocks = 0
        
        def nextLevel():
            self.level += 1
            if (self.level > 99):
                self.level = 1
                
            self.levelwindow.setNewLevel(self.level, self.level % 3, 20)    


        def addBlock1(sprite):
            self.blocks += 1
            self.levelwindow.updateLevelboard(self.blocks)
            self.levelwindow.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, addBlock2)
        def addBlock2(sprite):
            self.blocks += 1
            self.levelwindow.updateLevelboard(self.blocks)
            self.levelwindow.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, addBlock3)
        def addBlock3(sprite):
            self.blocks += 1
            self.levelwindow.updateLevelboard(self.blocks)
            self.levelwindow.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, addBlock4)
        def addBlock4(sprite):
            self.blocks += 1
            self.levelwindow.updateLevelboard(self.blocks)
            self.levelwindow.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, addBlock5)
        def addBlock5(sprite):
            self.blocks += 1
            self.levelwindow.updateLevelboard(self.blocks)
            self.levelwindow.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, addBlock6)
        def addBlock6(sprite):
            self.blocks += 1
            self.levelwindow.updateLevelboard(self.blocks)
            self.levelwindow.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, checkAndDelay)

            
        def checkAndDelay(sprite):
            if (self.blocks > 20):
                nextLevel()
                self.blocks = 0
                
            self.levelwindow.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.0, addBlock1)

        self.levelwindow.fadeTo((1.0, 1.0, 1.0, 1.0), currentTime, 0.6, addBlock1)
    
        
        pass
        
    def hide(self):
        self.levelwindow.clearColCallbacks()
        pass

class Page_Timer(Page):
    def __init__(self, x, y, page, pageCount):
        Page.__init__(self, x, y, page, pageCount)

        dposx = self.width/2
        dposy = 10

        
        self.titletext = Text(dposx, dposy, self.titlefont, "THE TIMER")
        self.titletext.setAnchor("center")
        self.titletext.setScale((1.5, 1.5))
        self.subSprites.append(self.titletext)

        dposy += 15
        
        self.infotext = []
        self.infotext.append(Text(dposx, dposy, self.textfont,
                             "If the hourglass on the timer board\n" +
                             "reaches zero the game is over."))

        dposy += 20

        self.infotext.append(Text(dposx, dposy, self.textfont,
                             "Before running out of time, the borders\n" +
                             "will flash red as a warning."))

        dposy += 20
        
        self.hourglass = Hourglass()
        self.hourglass.setPos((dposx - 22, dposy))
        self.hourglass.setScale((0.5, 0.5))
        self.hourglass.scaleValue(0.2)

        self.subSprites.append(self.hourglass)
        

        dposy += 50
        
        self.infotext.append(Text(dposx, dposy, self.textfont,
                             "When removing blocks, the timer will also\n" +
                             "be a short while. The timer can only be\n" +
                             "stopped a maximum of 5 seconds though.\n" +
                             "Use this pause to plan your next move!"))
 
        dposy += 36

        for t in self.infotext:
            t.setAnchor("center")
            self.subSprites.append(t)
            
    def show(self, currentTime):

        self.hourglass.reset(200)
        pass
        
    def hide(self):
        self.hourglass.clearColCallbacks()
        pass

    def setTimerState(self, state):
        if state == "low":
            def saveTheDay(sprite):
                self.hourglass.value += 100
                self.hourglass.addPause(1.0)
            
            self.hourglass.pulseBorder((1.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 1.0), 0.5)
            self.hourglass.fadeTo((1.0,1.0,1.0,1.0), self.currentTime, 2.5, saveTheDay)
            
        if state == "normal" or state == "high":
            self.hourglass.stopPulseBorder()
        
class Page_Advanced(Page):
    def __init__(self, x, y, page, pageCount):
        Page.__init__(self, x, y, page, pageCount)

        dposx = self.width/2
        dposy = 10

        
        self.titletext = Text(dposx, dposy, self.titlefont, "ADVANCED")
        self.titletext.setAnchor("center")
        self.titletext.setScale((1.5, 1.5))
        self.subSprites.append(self.titletext)

        dposy += 15
        
        self.infotext = []
        self.infotext.append(Text(dposx, dposy, self.textfont,
                                  "The loops you create do not have to be\n" +
                                  "symmetric, they can have any shape as long\n" +
                                  "as all blocks in the loop are connected."))

        dposy += 58
                         
        self.blocktypes = [1, 0, 0, 0,
                      0, 0, 2, 0,
                      0, 1, 0, 0,
                      0, 0, 2, 0]
        self.blockspos = (dposx - 24, dposy - 24)              

        self.marker2 = Marker()
        self.marker2.setPos((dposx, dposy))
        
        dposy += 36
        
        self.infotext.append(Text(dposx, dposy, self.textfont,
                                  "When encircling other blocks in a loop,\n" +
                                  "they will also be removed. Large loops\n" +
                                  "gives more points than the blocks\n" +
                                  "individually."))
 
                                         
        for t in self.infotext:
            t.setAnchor("center")
            self.subSprites.append(t)
            
    def showInit(self):  
        self.blocks = createBlockGroup(self.blockspos[0], self.blockspos[1], self.blocktypes, 4)
        for b in self.blocks:
            self.subSprites.append(b)
                
        self.subSprites.append(self.marker2)

    def show(self, currentTime):
        self.showInit()
        
        # TODO, DOES NOTHING AT ALL THIS, FIX!:
        for i in range(4):
            for j in range(4):
                self.blocks[i * 4 + j].doNormal()
                self.blocks[i * 4 + j].setToBoardCoord(j, i)

        
        def turnLeft(sprite):
            rotateBlocksInGroup(self.blocks, 3, 3, 4, self.currentTime, True)
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.5, doBlink)
            
        def turnRight(sprite):
            for i in range(4):
                for j in range(4):
                    self.blocks[i * 4 + j].doNormal()
            
            rotateBlocksInGroup(self.blocks, 3, 3, 4, self.currentTime, False)
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.0, turnLeft)

        def doBlink(sprite):
            for b in self.blocks:
                b.doBlink()

            getBlock(self.blocks, 0, 0, 4).doNormal()
            getBlock(self.blocks, 2, 1, 4).doNormal()
            getBlock(self.blocks, 1, 2, 4).doNormal()            
            getBlock(self.blocks, 3, 3, 4).doNormal()

            def doWholeBlink(sprite):
                getBlock(self.blocks, 2, 1, 4).doBlink()
                getBlock(self.blocks, 1, 2, 4).doBlink()            
                
                self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.5, turnRight)
            
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.0, doWholeBlink)

            
            
            
        self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), currentTime, 1.0, turnLeft)    

    def hide(self):
        self.marker2.clearColCallbacks()
        
        for b in self.blocks:
            self.subSprites.remove(b)
                
        self.subSprites.remove(self.marker2)
        
        pass
 
class Page_Combos(Page):
    def __init__(self, x, y, page, pageCount):
        Page.__init__(self, x, y, page, pageCount)

        dposx = self.width/2
        dposy = 10

        
        self.titletext = Text(dposx, dposy, self.titlefont, "COMBOS")
        self.titletext.setAnchor("center")
        self.titletext.setScale((1.5, 1.5))
        self.subSprites.append(self.titletext)

        dposy += 15
        
        self.infotext = []
        self.infotext.append(Text(dposx, dposy, self.textfont,
                                  "If a loop is created as a result of blocks\n" +
                                  "landing on other blocks after a fall, \n" +
                                  "a combo is performed."))

        dposy += 58
                         
        self.blocktypes = [1, 2, 2, 0,
                      0, 1, 1, 2,
                      2, 1, 2, 1,
                      2, 2, 2, 2]
        self.blockspos = (dposx - 24, dposy - 24)       

        self.marker2 = Marker()
        self.marker2.setPos((dposx, dposy))


        dposy += 36
        
        self.infotext.append(Text(dposx, dposy, self.textfont,
                                  "Combos give an extra big score bonus.\n" +
                                  "Successive combos will give an increasingly\n" +
                                  "large score bonus for each combo.\n" +
                                  "Try to perform many combos!"))
 
                                         
        for t in self.infotext:
            t.setAnchor("center")
            self.subSprites.append(t)
            
    def showInit(self):        
        self.blocks = createBlockGroup(self.blockspos[0], self.blockspos[1], self.blocktypes, 4)
        for b in self.blocks:
            self.subSprites.append(b)
                
        self.subSprites.append(self.marker2)   
        
    def show(self, currentTime):
        self.showInit()
        
        # TODO, DOES NOTHING AT ALL THIS, FIX!:
        for i in range(4):
            for j in range(4):
                self.blocks[i * 4 + j].doNormal()
                self.blocks[i * 4 + j].setToBoardCoord(j, i)

        
        def turnLeft(sprite):
            rotateBlocksInGroup(self.blocks, 3, 3, 4, self.currentTime, True)
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.5, doBlink1)
            
        def turnRight(sprite):
            for i in range(4):
                for j in range(4):
                    self.blocks[i * 4 + j].doNormal()
            
            rotateBlocksInGroup(self.blocks, 3, 3, 4, self.currentTime, False)
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.5, turnLeft)

        def doBlink1(sprite):
            getBlock(self.blocks, 1, 1, 4).doBlink()
            getBlock(self.blocks, 1, 2, 4).doBlink()
            getBlock(self.blocks, 2, 1, 4).doBlink()
            getBlock(self.blocks, 2, 2, 4).doBlink()
            
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.0, removeBlocks)
            
        def removeBlocks(sprite):
            getBlock(self.blocks, 1, 1, 4).doNormal()
            getBlock(self.blocks, 1, 2, 4).doNormal()
            getBlock(self.blocks, 2, 1, 4).doNormal()
            getBlock(self.blocks, 2, 2, 4).doNormal()
  
            def remove1(sprite):
                getBlock(self.blocks, 1, 1, 4).fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.1, remove2)
            def remove2(sprite):
                getBlock(self.blocks, 2, 1, 4).fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.1, remove3)
            def remove3(sprite):
                getBlock(self.blocks, 1, 2, 4).fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.1, remove4)
            def remove4(sprite):
                getBlock(self.blocks, 2, 2, 4).fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.1, done)
                
            def done (sprite):
                self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.5, fallDown)
                
            remove1(None)
                
   
        def fallDown(sprite):

            b = getBlock(self.blocks, 1, 0, 4)
            b.moveToBoardCoord(b.boardx, b.boardy + 1, self.currentTime)
            b = getBlock(self.blocks, 1, 1, 4)
            b.moveToBoardCoord(b.boardx, b.boardy + 1, self.currentTime)   
            b = getBlock(self.blocks, 2, 0, 4)
            b.moveToBoardCoord(b.boardx, b.boardy + 1, self.currentTime)
            b = getBlock(self.blocks, 2, 1, 4)
            b.moveToBoardCoord(b.boardx, b.boardy + 1, self.currentTime)
                
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, fallDown2)
      
        def fallDown2(sprite):
            b = getBlock(self.blocks, 1, 0, 4)
            b.moveToBoardCoord(b.boardx, b.boardy + 1, self.currentTime)
            b = getBlock(self.blocks, 1, 1, 4)
            b.moveToBoardCoord(b.boardx, b.boardy + 1, self.currentTime)   
            b = getBlock(self.blocks, 2, 0, 4)
            b.moveToBoardCoord(b.boardx, b.boardy + 1, self.currentTime)
            b = getBlock(self.blocks, 2, 1, 4)
            b.moveToBoardCoord(b.boardx, b.boardy + 1, self.currentTime)
                
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.2, doBlink2)
                 
        def doBlink2(sprite):
            getBlock(self.blocks, 1, 0, 4).doBlink()
            getBlock(self.blocks, 1, 3, 4).doBlink()
            getBlock(self.blocks, 2, 0, 4).doBlink()
            getBlock(self.blocks, 2, 3, 4).doBlink()
            getBlock(self.blocks, 0, 2, 4).doBlink()
            getBlock(self.blocks, 0, 3, 4).doBlink()
            getBlock(self.blocks, 3, 2, 4).doBlink()
            getBlock(self.blocks, 3, 3, 4).doBlink()
            
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.5, fallUp)
            
        def fallUp(sprite):
            getBlock(self.blocks, 1, 0, 4).doNormal()
            getBlock(self.blocks, 1, 3, 4).doNormal()
            getBlock(self.blocks, 2, 0, 4).doNormal()
            getBlock(self.blocks, 2, 3, 4).doNormal()
            getBlock(self.blocks, 0, 2, 4).doNormal()
            getBlock(self.blocks, 0, 3, 4).doNormal()
            getBlock(self.blocks, 3, 2, 4).doNormal()
            getBlock(self.blocks, 3, 3, 4).doNormal()
        
            b = getBlock(self.blocks, 1, 0, 4)
            b.moveToBoardCoord(b.boardx, b.boardy - 1, self.currentTime)
            b = getBlock(self.blocks, 1, 1, 4)
            b.moveToBoardCoord(b.boardx, b.boardy - 1, self.currentTime)   
            b = getBlock(self.blocks, 2, 0, 4)
            b.moveToBoardCoord(b.boardx, b.boardy - 1, self.currentTime)
            b = getBlock(self.blocks, 2, 1, 4)
            b.moveToBoardCoord(b.boardx, b.boardy - 1, self.currentTime)
            
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, fallUp2)
            
        def fallUp2(sprite):
            b = getBlock(self.blocks, 1, 0, 4)
            b.moveToBoardCoord(b.boardx, b.boardy - 1, self.currentTime)
            b = getBlock(self.blocks, 1, 1, 4)
            b.moveToBoardCoord(b.boardx, b.boardy - 1, self.currentTime)   
            b = getBlock(self.blocks, 2, 0, 4)
            b.moveToBoardCoord(b.boardx, b.boardy - 1, self.currentTime)
            b = getBlock(self.blocks, 2, 1, 4)
            b.moveToBoardCoord(b.boardx, b.boardy - 1, self.currentTime)
            
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.5, addBlocks)
                      
        def addBlocks(sprite):
        
            def add1(sprite):
                getBlock(self.blocks, 2, 2, 4).fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, doBlink3)
            def add2(sprite):
                getBlock(self.blocks, 1, 2, 4).fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, add1)
            def add3(sprite):
                getBlock(self.blocks, 2, 1, 4).fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, add2)
            def add4(sprite):
                getBlock(self.blocks, 1, 1, 4).fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, add3)
                
            add4(None)
            
        def doBlink3(sprite):
            getBlock(self.blocks, 1, 1, 4).doBlink()
            getBlock(self.blocks, 1, 2, 4).doBlink()
            getBlock(self.blocks, 2, 1, 4).doBlink()            
            getBlock(self.blocks, 2, 2, 4).doBlink()
            
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.0, turnRight)   
                   
            
        self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), currentTime, 1.0, turnLeft)    

    def hide(self):
        self.marker2.clearColCallbacks()
        
        for b in self.blocks:
            self.subSprites.remove(b)
                
        self.subSprites.remove(self.marker2)   
        pass
            

           
    
class Scene_Tutorial(Scene):
    def _runOnce(self):
        Scene._runOnce(self)

        self.updateBlocker = True
        self.renderBlocker = False
        
        self.titlefont = Font("font_fat.png", 8, 8);
        self.textfont = Font("font_clean.png", 8, 8);

        self.pageCount = 7
        self.page_welcome = Page_Welcome(160, 120, 1, self.pageCount)
        self.page_controls = Page_Controls(160, 120, 2, self.pageCount)
        self.page_goal = Page_Goal(160, 120, 3, self.pageCount)
        self.page_level = Page_Level(160, 120, 4, self.pageCount)
        self.page_timer = Page_Timer(160, 120, 5, self.pageCount)
        self.page_advanced = Page_Advanced(160, 120, 6, self.pageCount)
        self.page_combos = Page_Combos(160, 120, 7, self.pageCount)   
     
        self.pages = {0 : self.page_welcome,
                      1 : self.page_controls,
                      2 : self.page_goal,
                      3 : self.page_level,
                      4 : self.page_timer,
                      5 : self.page_advanced,
                      6 : self.page_combos}
        
        self.currentPage = 0
        self.sprites.add(self.pages[self.currentPage])
        self.pages[self.currentPage].fadeTo((1.0,1.0,1.0,1.0), 0, 0.2)
        
        self.statelist = {"normal" : 0, "transition" : 1}
        self.state = self.statelist["normal"]

    def tick(self):
        pass

    def turnToPage(self, page):

        if (page >= self.pageCount):
            page = self.pageCount -1
        if (page < 0):
            page = 0

        if (page != self.currentPage):
            self.state = self.statelist["transition"]
       
            self.pages[self.newPage].clearColCallbacks()
            self.pages[self.currentPage].clearColCallbacks()
            
            self.newPage = page
            
            def switchPage(sprite):
                self.sprites.remove(sprite)
                sprite.clearColCallbacks()
                sprite.hide()

                self.sprites.add(self.pages[self.newPage])
                self.pages[self.newPage].show(self.currentTime)
                self.pages[self.newPage].fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1)
                self.pages[self.newPage].moveTo((160, 120), self.currentTime, 0.1)
                self.state = self.statelist["normal"]

 
            self.pages[self.newPage].setPos((160 + (100 * (self.newPage - self.currentPage)), 120))
            self.pages[self.currentPage].moveTo((160 + (100 * -(self.newPage - self.currentPage)), 120), self.currentTime, 0.1)
            self.pages[self.currentPage].fadeTo((1.0, 1.0, 1.0, 0.0), self.currentTime, 0.1, switchPage)
            
        self.currentPage = self.newPage
        
    def show(self):
        print self, "is showing"
        self.state = self.statelist["normal"]
        
    def hide(self):
        print self, "is hiding"
        
    def handleEvent(self, event):
        if event.type == KEYDOWN:
            key = event.key

            if key == K_ESCAPE:
                def killDialog(sprite):
                    SceneHandler().removeScene(Scene_DialogYesNo())
                def quit_game():
                    SceneHandler().removeScene(Scene_DialogYesNo())
                    SceneHandler().removeScene(scene_maingame.Scene_MainGame())
                    SceneHandler().removeScene(self)
                def do_nothing():
                    Scene_DialogYesNo().remove(killDialog)
                    
                Scene_DialogYesNo().setQuery("Do you want to exit to the menu?", quit_game, do_nothing)
                SceneHandler().pushScene(Scene_DialogYesNo())
            
            if (key == K_RETURN):
                scene_maingame.Scene_MainGame().startGame()
                SceneHandler().removeScene(self)
            
            if (self.state == self.statelist["normal"]):
                if (key == K_LEFT):
                    self.turnToPage(self.currentPage - 1)
                    
                if (key == K_RIGHT):
                    self.turnToPage(self.currentPage + 1)

        if event.type == EVENT_TIMER_STATE_CHANGED:
            self.page_timer.setTimerState(event.state)
                
                
        return True
        
