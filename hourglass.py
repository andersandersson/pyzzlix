from math import *
from globals import *

from sprite import *
from image import *
from font import *
from text import *

import scene_maingame

class Hourglass(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        self.font = Font("font_fat.png", 8, 8)

        self.bar = Sprite()
        self.bar.setImage(loadImage("pixel.png", 1, 1))        
        self.bar.setScale((72, -96))
        self.bar.setPos((8.0, 104.0))

        self.max = 0
        
        self.timeatlastframe = 0
        self.frameDelay = 0.1
        self.frame = 0
        self._value = 0
        self._pause = 0        
        self._halted = 0
        
        self.background = Sprite()
        self.background.setImage(loadImage("pixel.png", 1, 1))
        self.background.setScale((72.0, 96.0))
        self.background.setPos((8.0, 8.0))
        self.background.setCol((0.0, 0.0, 0.0, 0.3))
        
        self.border = Sprite()
        self.border.setImage(loadImage("hourglass_border.png"))
        self.border.setPos((0.0,0.0))
        
        self.pausebg = Sprite()
        self.pausebg.setImage(loadImage("pixel.png", 1, 1))
        self.pausebg.setScale((72.0, 96.0))
        self.pausebg.setPos((8.0, 8.0))
        self.pausebg.setCol((0.0, 0.0, 0.0, 0.0))

        self.stoptext = Text(44, 24, self.font, "STOP")
        self.stoptext.setScale((2.0, 2.0))
        self.stoptext.setAnchor("center")
        self.stoptext.setCol((0.0, 0.0, 0.0, 0.0))
                
        self.pausetext = Text(44, 48, self.font, "0")
        self.pausetext.setScale((2.0, 2.0))
        self.pausetext.setAnchor("center")
        self.pausetext.setCol((0.0, 0.0, 0.0, 0.0))

        self.glow = Sprite()
        self.glow.setImage(loadImage("hourglass_glow.png"))
        self.glow.setPos((0.0,0.0))
        self.glow.setCol((0.0, 0.0, 0.0, 0.0))

        self.pauseVisible = False

        self.subSprites.append(self.background)       
        self.subSprites.append(self.bar)
        self.subSprites.append(self.pausebg)
        self.subSprites.append(self.pausetext)
        self.subSprites.append(self.stoptext)
        self.subSprites.append(self.border)
        self.subSprites.append(self.glow)

        self._glow_col = (0.0, 0.0, 0.0, 0.0)
        self._glow_duration = 0.0

        self.statelist = {"low": 0, "normal": 1, "high": 2, "gameover": 3}
        self.state = self.statelist["high"]
    
        self.reset(1000)

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
        
    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value

        if self._value > self.max:
            self._value = self.max

    value = property(getValue, setValue)

    def reset(self, maxValue):
        self.max = maxValue
        self.value = maxValue
        self._halted = 0
        self._pause = 0
        self.state = self.statelist["high"]
        self.hidePause()

    def scaleValue(self, perc):
        self.value *= perc
        self.max *= perc

    def updatePauseTimer(self, time):
        temppause = ceil(self._pause)
        self._pause += time

        if self._pause > MAX_PAUSE_TIME_SEC:
            self._pause = MAX_PAUSE_TIME_SEC
        
        if self._pause > 0:
            self.showPause()
        else:
            self.hidePause()
            
        if (self._pause > 0):
            self.pausetext.setText("%.1f" % self._pause)
        
    def addPause(self, time):
        self.updatePauseTimer(time)
        self.pausetext.setScale((2.5, 2.5))
        self.pausetext.scaleTo((2.0, 2.0), self.currentTime, 0.3)

    def halt(self):
        self._halted += 1
        
    def unhalt(self):
        self._halted -= 1

    def showPause(self):
        if self.pauseVisible:
            return
        
        self.pauseVisible = True
        self.pausebg.fadeTo((0.0, 0.0, 0.0, 0.7), self.currentTime, 0.2)
        self.pausetext.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.2)
        self.stoptext.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.2)
        
    def hidePause(self):
        if not self.pauseVisible:
            return
        
        self.pauseVisible = False
        self.pausebg.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.2)
        self.pausetext.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.2)
        self.stoptext.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.2)
            
    def update(self, currentTime):
        Sprite.update(self, currentTime)

        if self.state == self.statelist["gameover"]:
            return

        if self.value <= 0:
            pygame.event.post(pygame.event.Event(EVENT_GAME_OVER))
            self.state = self.statelist["gameover"]
            return

        if self._pause <= 0 and self._halted <= 0:
            self.value -= 1
        elif self._halted <= 0:
            self.updatePauseTimer(-(self.currentTime - self.lastTime))

        #self.image.fill([0,0,0])
        #self.image.set_alpha(200);
        p = float(self.value) / self.max

        if p > 1.0:
            p = 1.0
            
        p = (exp(2.0*p) - 1.0)/(exp(2.0) - 1.0)

        if p < 0.2 and not self.state == self.statelist["low"]:
            self.state = self.statelist["low"]
            pygame.event.post(pygame.event.Event(EVENT_TIMER_STATE_CHANGED, state="low"))
        elif p >= 0.2 and p < 0.8 and not self.state == self.statelist["normal"]:
            self.state = self.statelist["normal"]
            pygame.event.post(pygame.event.Event(EVENT_TIMER_STATE_CHANGED, state="normal"))
        elif p >= 0.8 and not self.state == self.statelist["high"]:
            self.state = self.statelist["high"]
            pygame.event.post(pygame.event.Event(EVENT_TIMER_STATE_CHANGED, state="high"))

        self.bar.scaleTo((72, -p*96), currentTime, 0.1)
        self.bar.fadeTo((1 - p, p, 0.0, 1.0), currentTime, 0.1)
        #pygame.draw.rect(self.image, [(1-p)*255,p*255,0], [0,(1-p)*150,90,150])
        
