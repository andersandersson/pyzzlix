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
import marker

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

        self.entertext = Text(self.width/2, self.height - 16, self.textfont, "Press Enter to start game") 
        self.entertext.setAnchor("center")
        
        self.subSprites.append(self.entertext)

        self.leftarrow = Text(4, self.height/2 - 4, self.titlefont, "<")
        self.rightarrow = Text(self.width - 12, self.height/2 - 4, self.titlefont, ">")
        
        self.subSprites.append(self.leftarrow)
        self.subSprites.append(self.rightarrow)


        self.pagetext = Text(self.width - 4, self.height - 16, self.titlefont, "%d/%d" % (page, pageCount))
        self.pagetext.setAnchor("right")

        self.subSprites.append(self.pagetext)
        
class Page_1(Page):
    def __init__(self, x, y, page, pageCount):
        Page.__init__(self, x, y, page, pageCount)

        self.welcometext = Text(self.width/2, 20, self.titlefont, "WELCOME\nTO\nPYZZLIX!")
        self.welcometext.setAnchor("center")
        self.welcometext.setScale((2.5, 2.5))


        self.subSprites.append(self.welcometext)

    def show(self):
        pass
        
class Page_2(Page):
    def __init__(self, x, y, page, pageCount):
        Page.__init__(self, x, y, page, pageCount)

        self.titletext = Text(self.width/2, 10, self.titlefont, "BASIC CONTROLS")
        self.titletext.setAnchor("center")
        self.titletext.setScale((1.5, 1.5))
        self.subSprites.append(self.titletext)
        
        self.infotext = []
        self.infotext.append(Text(self.width/2, 25, self.textfont,
                             "Use the ARROW keys to move the marker"))

        self.marker = Marker()
        self.marker.setPos((self.width/2 - 16, 52 - 16))
        self.subSprites.append(self.marker)
        
        self.infotext.append(Text(self.width/2, 70, self.textfont,
                             "The Z and X keys rotates the blocks\n" +
                                  "beneath the marker"))
        mposx = self.width/2 - 16
        mposy = 108 - 16

        self.blocks = []
        self.blocks.append(Block(0, 0, 0, (mposx + 8, mposy + 8)))
        self.blocks.append(Block(0, 1, 1, (mposx + 8, mposy + 8)))
        self.blocks.append(Block(1, 1, 2, (mposx + 8, mposy + 8)))
        self.blocks.append(Block(1, 0, 3, (mposx + 8, mposy + 8)))


        for b in self.blocks:
            b.offset_x = self.width/2 - 16
            b.offset_y = 108 - 16                        
            self.subSprites.append(b)

        
        self.marker2 = Marker()
        self.marker2.setPos((mposx, mposy))
        self.subSprites.append(self.marker2)

                                         
        for t in self.infotext:
            t.setAnchor("center")
            self.subSprites.append(t)

    def show(self):
        def turnLeft(sprite):
            self.blocks[0].moveToBoardCoord(self.blocks[0].boardx,
                                            self.blocks[0].boardy + 1,
                                            self.currentTime)
            self.blocks[1].moveToBoardCoord(self.blocks[1].boardx + 1,
                                            self.blocks[1].boardy,
                                            self.currentTime)
            self.blocks[2].moveToBoardCoord(self.blocks[2].boardx,
                                            self.blocks[2].boardy - 1,
                                            self.currentTime)
            self.blocks[3].moveToBoardCoord(self.blocks[3].boardx - 1,
                                            self.blocks[3].boardy,
                                            self.currentTime)
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.0, turnRight)
                    
        def turnRight(sprite):
            self.blocks[0].moveToBoardCoord(self.blocks[0].boardx,
                                            self.blocks[0].boardy - 1,
                                            self.currentTime)
            self.blocks[1].moveToBoardCoord(self.blocks[1].boardx - 1,
                                            self.blocks[1].boardy,
                                            self.currentTime)
            self.blocks[2].moveToBoardCoord(self.blocks[2].boardx,
                                            self.blocks[2].boardy + 1,
                                            self.currentTime)
            self.blocks[3].moveToBoardCoord(self.blocks[3].boardx + 1,
                                            self.blocks[3].boardy,
                                            self.currentTime)
            self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.0, turnLeft) 

        self.marker2.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 1.0, turnLeft)    

    def hide():
        self.marker2.clearColCallbacks()
            

class Scene_Tutorial(Scene):
    def _runOnce(self):
        Scene._runOnce(self)

        self.updateBlocker = True
        self.renderBlocker = False
        
        self.titlefont = Font("font_fat.png", 8, 8);
        self.textfont = Font("font_clean.png", 8, 8);

        self.pageCount = 7
        self.pages = [Page_1(160, 120, 1, self.pageCount),
                      Page_2(160, 120, 2, self.pageCount),
                      Page_1(160, 120, 3, self.pageCount),
                      Page_2(160, 120, 4, self.pageCount),
                      Page_1(160, 120, 5, self.pageCount),
                      Page_2(160, 120, 6, self.pageCount),
                      Page_1(160, 120, 7, self.pageCount)
                      ]
        self.currentPage = 0
        self.sprites.add(self.pages[self.currentPage])

    def tick(self):
        self.sprites.update(self.currentTime)
        pass

    def turnToPage(self, page):
        self.newPage = page
        if (self.newPage >= self.pageCount):
            self.newPage = self.pageCount -1
        if (self.newPage < 0):
            self.newPage = 0

        if (self.newPage != self.currentPage):
            self.sprites.add(self.pages[self.newPage])
            self.pages[self.newPage].show()
            self.sprites.remove(self.pages[self.currentPage])
            

        self.currentPage = self.newPage    
        
    def show(self):
        print self, "is showing"
        
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

            if (key == K_LEFT):
                self.turnToPage(self.currentPage - 1)
                
            if (key == K_RIGHT):
                self.turnToPage(self.currentPage + 1)

                
        return True
        
