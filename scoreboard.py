from globals import *

from sprite import *
from animation import *
from text import *

class Scoreboard(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        self.font = Font("font_fat.png", 8, 8)
        
        self.scorelabeltext = Text(12.0, 20, self.font, "SCORE:")
        self.scoretext = Text(100.0, 30, self.font, "0")
        self.scoretext.setAnchor("right")
        
        self.levellabeltext = Text(12.0, 42, self.font, "LEVEL:")        
        self.leveltext = Text(100.0, 52, self.font, "0")
        self.leveltext.setAnchor("right")
        
        self.scorebg = Sprite()
        self.scorebg.setImage(loadImage("pixel.png", 1, 1))
        self.scorebg.setPos((8.0, 16.0))
        self.scorebg.setScale((96.0, 56.0))
        self.scorebg.setCol((0.0, 0.0, 0.0, 0.5))

        self.border = Sprite()
        self.border.setImage(loadImage("scoreboard_border.png"))
        self.border.setPos((0.0,0.0))
        
        self.glow = Sprite()
        self.glow.setImage(loadImage("scoreboard_glow.png"))
        self.glow.setPos((0.0,8.0))
        self.glow.setCol((0.0, 0.0, 0.0, 0.0))
        
        self.subSprites.append(self.scorebg)
        self.subSprites.append(self.scorelabeltext)
        self.subSprites.append(self.scoretext)
        self.subSprites.append(self.levellabeltext)
        self.subSprites.append(self.leveltext)
        self.subSprites.append(self.border)
        self.subSprites.append(self.glow)
        
        self.level = 0
        self.score = 0

        self._glow_col = (0.0, 0.0, 0.0, 0.0)
        self._glow_duration = 0.0

    def updateScoreboard(self, level, score):
        self.level = level
        self.score = score
    
        self.scoretext.setText(str(self.score))
        self.leveltext.setText(str(self.level))
        
    def pulseBorder(self, col1, col2, duration):
        self._glow_duration = duration

        def fade_to_done(s):
            self._glow_col = col1
            self.glow.fadeTo(col1, self.currentTime, duration, fade_from_done)

        def fade_from_done(s):
            self._glow_col = col2
            self.glow.fadeTo(col2, self.currentTime, duration, fade_to_done)

        self.glow.clearColCallbacks()
        fade_from_done(None)

    def stopPulseBorder(self):
        from_col = (self._glow_col[0], self._glow_col[1], self._glow_col[2], 0.0)
        
        self.glow.clearColCallbacks()
        self.glow.fadeTo(from_col, self.currentTime, self._glow_duration)        
