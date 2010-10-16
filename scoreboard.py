from globals import *

from sprite import *
from animation import *
from text import *

class Scoreboard(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        self.font = Font("font_fat.png", 8, 8)
        
        self.scorelabeltext = Text(4.0, 20, self.font, "SCORE:")
        self.scoretext = Text(92.0, 30, self.font, "0")
        self.scoretext.setAnchor("right")
        
        self.levellabeltext = Text(4.0, 42, self.font, "LEVEL:")        
        self.leveltext = Text(92.0, 52, self.font, "0")
        self.leveltext.setAnchor("right")
        
        self.scorebg = Sprite()
        self.scorebg.setImage(loadImage("pixel.png", 1, 1))
        self.scorebg.setPos((0.0, 16.0))
        self.scorebg.setScale((96.0, 56.0))
        self.scorebg.setCol((0.0, 0.0, 0.0, 0.3))
        
        self.subSprites.append(self.scorebg)
        self.subSprites.append(self.scorelabeltext)
        self.subSprites.append(self.scoretext)
        self.subSprites.append(self.levellabeltext)
        self.subSprites.append(self.leveltext)
        
        self.level = 0
        self.score = 0

    def updateScoreboard(self, level, score):
        self.level = level
        self.score = score
    
        self.scoretext.setText(str(self.score))
        self.leveltext.setText(str(self.level))