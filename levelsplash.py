from sprite import *
from block import *
from font import *
from text import *

leveltextpos = 100

class LevelSplash(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.width = 160
        self.height = 200
        self.levelfont = Font("font_fat.png", 8, 8)
        self.infofont = Font("font_clean.png", 4, 8)
        self.leveltext = Text(self.width/2, leveltextpos, self.levelfont, "LEVEL 1")
        self.leveltext.setAnchor("center")

        self.infotext = Text(self.width/2, 140, self.infofont, "Two-by-two's are fun!")
        self.infotext.setAnchor("center")

        self.continuetext = Text(self.width/2, 190, self.infofont, "Press Enter to Continue...")
        self.continuetext.setAnchor("center")
                
        self.subSprites.append(self.leveltext)
        self.subSprites.append(self.infotext)
        self.subSprites.append(self.continuetext)
        
    def display(self, level, currentTime, tutorial=True):

        self.leveltext.setText("LEVEL " + str(level))
        
        self.leveltext.setCol((1.0, 1.0, 1.0, 0.0))
        self.leveltext.fadeTo((1.0, 1.0, 1.0, 1.0), currentTime, 0.8)
        
        self.leveltext.setPos((self.width/2, 0))
        self.leveltext.moveTo((self.width/2, leveltextpos), currentTime, 0.8)

    def hide(self, currentTime, callfunc=None):
        
        #self.levelText.setCol((0.0, 0.0, 0.0, 0.0))
        self.leveltext.fadeTo((1.0, 1.0, 1.0, 0.0), currentTime, 1.5)
        self.leveltext.moveTo((self.width/2, 0), currentTime, 1.5, callfunc)

        
