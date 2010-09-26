#import pygame
#from pygame import *
from font import *

from sprite import *

import math

class Text(Sprite):
    def __init__(self, x, y, font, text):
        Sprite.__init__(self)
        self.chars = None
        self.font = font
        self.x = x
        self.y = y
        self.setAnchor("left")
        self.setText(text)
        
                
    def setAnchor(self, mode):
        if (mode == "right"):
            self.anchor = mode
        elif (mode == "center"):
            self.anchor = mode
        else:
            self.anchor = "left"
        
    def setText(self, text):
        self.chars = list(text)
        self.length = len(self.chars)
        counter = 0
        for char in self.chars:
            glyph = self.font.getGlyph(char)
            sprite = Sprite()
            sprite.setImage(glyph)
            sprite.setPos((counter * self.font.width, 0))
            self.subSprites.append(sprite)
            counter += 1
                          
    def draw(self, surf):
        if (self.anchor == "left"):
            drawposx = self.x
        elif (self.anchor == "right"):
            drawposx = self.x - self.length * self.font.width
        elif (self.anchor == "center"):
            drawposx = self.x - (self.length * self.font.width) / 2

        for c in self.chars:
            #surf.blit(self.font.getGlyph(c), (drawposx, self.y), ((0,0) , (self.font.width, self.font.height)))
            drawposx += self.font.width
