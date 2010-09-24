from globals import *

#import pygame
#from pygame.locals import *

from sprite import *

class Block(Sprite):
    def __init__(self, x, y, type):
        Sprite.__init__(self)
        self.type = type
        self.loadSheet("block" + str(self.type) + ".bmp", 16, 16)

        self.boardx = x
        self.boardy = y

        self.offset_x = 16
        self.offset_y = 16
        self.scale_x = 16
        self.scale_y = 16

        self.move_ticker = 0
        self.old_x = self.x
        self.old_y = self.y
        self.new_x = self.x
        self.new_y = self.y

        self.timeatlastframe = 0
        self.frameDelay = 0.1
        self.frame = 0
        self.layer = type

        self.moveTo(x, y)

        
    def moveTo(self, x, y):
        self.old_x = self.x * self.scale_x + self.offset_x
        self.old_y = self.y * self.scale_y + self.offset_y
        self.move_ticker = 0
        
        self.x = x
        self.y = y

        self.new_x = self.x * self.scale_x + self.offset_x
        self.new_y = self.y * self.scale_y + self.offset_y

    def kill(self):
        self.images = loadImageSheet("block" + str(9) + ".bmp", 16, 16)
        self.image = self.images[0]

    def update(self, deltaTime):
        Sprite.update(self, deltaTime)

        if (self.move_ticker) < 1.0:
            self.x = (self.new_x - self.old_x)*self.move_ticker + self.old_x
            self.y = (self.new_y - self.old_y)*self.move_ticker + self.old_y
            self.move_ticker += deltaTime*9
        else:
            self.x = self.new_x
            self.y = self.new_y
            