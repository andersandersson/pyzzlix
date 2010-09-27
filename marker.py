from globals import *

#import pygame
#from pygame.locals import *

from sprite import *

class Marker(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.loadSheet("marker.png", 32, 32)
        
        self.boardx = x
        self.boardy = y
        
        self.offset_x = 16
        self.offset_y = -BOARD_HEIGHT*16+16

        self.scale_x = 16
        self.scale_y = 16
        
        self.setPos((self.boardx * self.scale_x + self.offset_x, self.boardy * self.scale_y + self.offset_y))

    def moveToBoardCoord(self, boardx, boardy, currentTime):
        self.boardx = boardx
        self.boardy = boardy
        self.moveTo((self.boardx * self.scale_x + self.offset_x, self.boardy * self.scale_y + self.offset_y), currentTime, 0.0)

    def move(self, dx, dy, currentTime):
        self.moveToBoardCoord(self.boardx + dx, self.boardy + dy, currentTime)
            
