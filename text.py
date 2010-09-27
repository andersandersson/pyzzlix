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
        self.text = ""
        self.setPos([x, y])
        self.anchor = "left"
        self.setText(text)
        self.currentChar = 0

    def setAnchor(self, mode):
        if (mode == "right"):
            self.anchor = mode
        elif (mode == "center"):
            self.anchor = mode
        else:
            self.anchor = "left"

        text = self.text
        self.text = ""
        self.setText(text)
        
    def setText(self, text):
        if self.text == text:
           return
        else:
            self.text = text

        self.chars = list(text)
        self.length = len(self.chars)
        self.width = self.font.width*self.length
        self.height = self.font.height

        if (self.anchor == "left"):
            drawposx = 0
        elif (self.anchor == "right"):
            drawposx = -self.length * self.font.width
            print self.width, self.length, self.font.width
            #self.center = ((self.length * self.font.width), 0)
        elif (self.anchor == "center"):
            #self.center = ((self.length * self.font.width) / 2, 0)
            drawposx = -(self.length * self.font.width) / 2

        self.subSprites = []
        print drawposx
        for char in self.chars:
            glyph = self.font.getGlyph(char)
            sprite = Sprite()
            sprite.setImage(glyph)
            sprite.setPos((drawposx, 0))
            self.subSprites.append(sprite)
            drawposx += self.font.width
                         
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
