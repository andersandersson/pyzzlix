from globals import *
from singleton import *

from sprite import *

class Font():
    def __init__(self, fontfile, gw, gh):
        self.glyphs = Sprite()
        self.width = gw
        self.height = gh
        self.c = 0
        self.glyphs.loadSheet(fontfile, gw, gh)    
    
    def getGlyph(self, c):
        glyph = self.glyphs
        glyph.setFrame(ord(c))
        return glyph
