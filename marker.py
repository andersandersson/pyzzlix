from globals import *

#import pygame
#from pygame.locals import *

from sprite import *

class Marker(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.loadSheet("marker.bmp", 32, 32)
        
        self.boardx = 0
        self.boardy = 0
        
        self.offset_x = 16
        self.offset_y = -BOARD_HEIGHT*16+16

        self.scale_x = 16
        self.scale_y = 16
        
        self.moveTo(x, y)
        
    def moveTo(self, x, y):
        self.boardx = x
        self.boardy = y
        self.x = self.boardx * self.scale_x + self.offset_x
        self.y = self.boardy * self.scale_y + self.offset_y

    def move(self, dx, dy):
        self.moveTo(self.boardx + dx, self.boardy + dy)
            
