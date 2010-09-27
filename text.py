#import pygame
#from pygame import *
from font import *

from sprite import *

import math

class Text(Sprite):
    def __init__(self, x, y, font, text):
        Sprite.__init__(self)
        self.chars = list(text)
        self.font = font
        self.text_x = x
        self.text_y = y
        self.anchor = "left"
        self.setText(text)
        self.currentChar = 0

    def __iter__(self):
        self.currentChar = 0
        return self

    def next(self):
        if self.currentChar == len(self.chars):
            raise StopIteration

        if (self.anchor == "left"):
            drawposx = self.text_x
        elif (self.anchor == "right"):
            drawposx = self.text_x - self.length * self.font.width
        elif (self.anchor == "center"):
            drawposx = self.text_x - (self.length * self.font.width) / 2

        glyph = self.font.getGlyph(self.chars[self.currentChar])
        
        glyph.setPos(drawposx+self.currentChar*self.font.width, self.text_y)

        self.currentChar += 1

        return glyph
                
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
        self.setAnchor(self.anchor)
