from globals import *
from singleton import *

class Font():
    def __init__(self, fontfile, gw, gh):
        self.glyphs = 0
        self.width = gw
        self.height = gh
        self.glyphs = loadImageSheet(fontfile, gw, gh)
    
    
    def getGlyph(self, c):
        return self.glyphs[ord(c) - 32]