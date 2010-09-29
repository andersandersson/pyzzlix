from globals import *

#import pygame
#from pygame.locals import *

import random
from sprite import *

STATUS_NONE = 0
STATUS_MOVING = 1
STATUS_WEIGHTLESS = 2
STATUS_IN_CIRCLE = 4
STATUS_OFFSCREEN = 8

DEFAULT_GRAVITY_DELAY = 5

class Block(Sprite):
    def __init__(self, boardx, boardy, type):
        Sprite.__init__(self)
        self.type = type
        #self.loadSheet("new_block" + str(self.type) + ".png", 16, 16)
        self.loadSheet("blocks.png", 16, 16, type * 16, 0, 16, 8 * 16)
    
        self.boardx = boardx
        self.boardy = boardy

        self.gravityDelay = 0
        self.type = type
        self.status = STATUS_NONE
        
        self.size = (16, 16)
        self.center = (self.size[0] / 2, self.size[1] / 2)
        self.offset_x = self.center[0]
        self.offset_y = -BOARD_HEIGHT*16 + self.center[1]

        self.layer = type

        Sprite.setPos(self, (self.boardx * self.size[0] + self.offset_x, self.boardy * self.size[1] + self.offset_y))

    def moveToBoardCoord(self, boardx, boardy, currentTime):
        self.boardx = boardx
        self.boardy = boardy
        self.moveTo((self.boardx * self.size[0] + self.offset_x, self.boardy * self.size[1] + self.offset_y), currentTime, 0.15)

    def animatePopup(self, currentTime):
        self.setCol((0.1, 0.1, 0.1, 1.0))
        self.fadeTo((1.0, 1.0, 1.0, 1.0), currentTime, 1.0)
        self.setScale((0.0, 0.0))
        self.scaleTo((1.0, 1.0), currentTime, 0.15)
        self.setRot(180.0)
        self.rotateTo(0, currentTime, 0.3)

    def kill(self):
        self.images = loadImageSheet("block" + str(9) + ".bmp", 16, 16)
        self.image = self.images[0]

    def update(self, deltaTime):
        Sprite.update(self, deltaTime)
     
