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
        
        glyph.setPos([drawposx+self.currentChar*self.font.width, self.text_y])

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

#        counter = 0
#        for char in self.chars:
#            glyph = self.font.getGlyph(char)
#            sprite = Sprite()
#            sprite.setImage(glyph)
#            sprite.setPos((counter * self.font.width, 0))
#            self.subSprites.append(sprite)
#            counter += 1
                          
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
