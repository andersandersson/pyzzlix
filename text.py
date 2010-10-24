from font import *

from sprite import *

import math

class Text(Sprite):
    def __init__(self, x, y, font, text):
        Sprite.__init__(self)
        self.font = font
        self.text = ""
        self.setPos([x, y])
        self.anchor = "left"
        self.setText(text)

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
        
    def setText(self, newtext):
        if self.text == newtext:
           return
        else:
            self.text = newtext

        splittext = newtext.split('\n')    
        self.subSprites = []

        drawposx = 0
        drawposy = 0
        for text in splittext:
            chars = list(text)
            length = len(chars)
            width = self.font.width * length
            height = self.font.height

            if (self.anchor == "left"):
                drawposx = 0
            elif (self.anchor == "right"):
                drawposx = -length * self.font.width
            #self.center = ((self.length * self.font.width), 0)
            elif (self.anchor == "center"):
            #self.center = ((self.length * self.font.width) / 2, 0)
                drawposx = -(length * self.font.width) / 2
                
            for char in chars:
                glyph = self.font.getGlyph(char)
                sprite = Sprite()
                sprite.setImage(glyph)
                sprite.setPos((drawposx, drawposy))
                self.subSprites.append(sprite)
                drawposx += self.font.width
                         
            drawposy += self.font.height
                
