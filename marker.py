from globals import *

#import pygame
#from pygame.locals import *

from sprite import *

class Marker(Sprite):
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.loadSheet("marker.bmp", 32, 32)
        
        self.offset_x = 0
        self.offset_y = 0
        self.scale_x = 16
        self.scale_y = 16

        self.moveTo(x, y)
        
    def moveTo(self, x, y):
        self.x = x
        self.y = y
        self.x = self.x * self.scale_x + self.offset_x
        self.y = self.y * self.scale_y + self.offset_y

    def move(self, dx, dy):
        self.moveTo(self.x+dx, self.y+dy)
            