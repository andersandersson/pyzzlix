from globals import *
from singleton import *

from sprite import *

class Font():
    def __init__(self, fontfile, gw, gh):
        self.width = gw
        self.height = gh
        self.glyphs = loadImageSheet(fontfile, gw, gh)    
    
    def getGlyph(self, c):
        frame = ord(c) - 32

        if frame >= len(self.glyphs):
            frame = 0

        return self.glyphs[frame]
