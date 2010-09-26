from globals import *

#import pygame
#from pygame.locals import *

from sprite import *

STATUS_NONE = 0
STATUS_MOVING = 1
STATUS_WEIGHTLESS = 2
STATUS_IN_CIRCLE = 4
STATUS_OFFSCREEN = 8

DEFAULT_GRAVITY_DELAY = 30

class Block(Sprite):
    def __init__(self, boardx, boardy, type):
        Sprite.__init__(self)
        self.type = type
        self.loadSheet("block" + str(self.type) + ".bmp", 16, 16)

        self.boardx = boardx
        self.boardy = boardy

        self.gravityDelay = 0
        self.type = type
        self.status = STATUS_NONE
        
        self.offset_x = 16
        self.offset_y = -BOARD_HEIGHT*16 + 16
        self.scale_x = 16
        self.scale_y = 16

        self.move_ticker = 0

        self.timeatlastframe = 0
        self.frameDelay = 0.1
        self.frame = 0
        self.layer = type

        Sprite.setPos(self, self.boardx * self.scale_x + self.offset_x, self.boardy * self.scale_y + self.offset_y)

    def moveToBoardCoord(self, x, y, currentTime):
        self.boardx = x
        self.boardy = y
        self.moveTo(self.boardx * self.scale_x + self.offset_x, self.boardy * self.scale_y + self.offset_y, currentTime, 0.15)

    def kill(self):
        self.images = loadImageSheet("block" + str(9) + ".bmp", 16, 16)
        self.image = self.images[0]

    def update(self, deltaTime):
        Sprite.update(self, deltaTime)
     
