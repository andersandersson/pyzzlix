from globals import *

from sprite import *
from animation import *
from text import *

class Scoreboard(Sprite):
    def __init__(self):
        Sprite.__init__(self)
    
        self.font = Font("font_fat.png", 8, 8)
            
        self.highscorelabeltext = Text(12.0, 12, self.font, "HISCORE:")        
        self.highscoretext = Text(76.0, 22, self.font, "0")
        self.highscoretext.setAnchor("right")
        
        self.scorelabeltext = Text(12.0, 32, self.font, "SCORE:")
        self.scoretext = Text(76.0, 42, self.font, "0")
        self.scoretext.setAnchor("right")
        
        self.scorebg = Sprite()
        self.scorebg.setImage(loadImage("pixel.png", 1, 1))
        self.scorebg.setPos((8.0, 8.0))
        self.scorebg.setScale((72.0, 48.0))
        self.scorebg.setCol((0.0, 0.0, 0.0, 0.5))

        self.border = Sprite()
        self.border.setImage(loadImage("windowframes.png", 208, 8, 88, 64))
        self.border.setPos((0.0,0.0))
        
        self.glow = Sprite()
        self.glow.setImage(loadImage("windowglows.png", 208, 8, 88, 64))
        self.glow.setPos((0.0,8.0))
        self.glow.setCol((0.0, 0.0, 0.0, 0.0))
        
        self.subSprites.append(self.scorebg)
        self.subSprites.append(self.scorelabeltext)
        self.subSprites.append(self.scoretext)
        self.subSprites.append(self.highscorelabeltext)
        self.subSprites.append(self.highscoretext)
        self.subSprites.append(self.border)
        self.subSprites.append(self.glow)
        
        self.level = 0
        self.score = 0

        self._glow_col = (0.0, 0.0, 0.0, 0.0)
        self._glow_duration = 0.0
        
    def setHighscore(self, highscore):
        self.highscore = highscore
        self.highscoretext.setText(str(self.highscore))
                
    def updateScoreboard(self, score):
        if (score != self.score):
            self.score = score
            self.scoretext.setText(str(self.score))
            if (score > self.highscore):
                self.highscoretext.setText(str(self.score))
                
        
    def pulseBorder(self, col, duration):
        self._glow_col = col
        self._glow_duration = duration
        from_col = (self._glow_col[0], self._glow_col[1], self._glow_col[2], 0.0)
        
        def fade_to_done(s):
            self.glow.fadeTo(from_col, self.currentTime, duration, fade_from_done)
            
        def fade_from_done(s):
            self.glow.fadeTo(col, self.currentTime, duration, fade_to_done)

        self.glow.clearColCallbacks()
        fade_from_done(None)

    def stopPulseBorder(self):
        from_col = (self._glow_col[0], self._glow_col[1], self._glow_col[2], 0.0)
        
        self.glow.clearColCallbacks()
        self.glow.fadeTo(from_col, self.currentTime, self._glow_duration)
