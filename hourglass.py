from math import *
from globals import *

from sprite import *
from image import *
from font import *
from text import *

class Hourglass(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        self.font = Font("font_fat.png", 8, 8)

        self.bar = Sprite()
        self.bar.setImage(loadImage("pixel.png", 1, 1))        
        self.bar.setScale((72, -96))

        self.max = 0
        
        self.timeatlastframe = 0
        self.frameDelay = 0.1
        self.frame = 0
        self._value = 0
        self._pause = 0        
        self._halted = 0
        
        self.reset(1000)

        self.pausebg = Sprite()
        self.pausebg.setImage(loadImage("pixel.png", 1, 1))
        self.pausebg.setScale((72, -96))
        self.pausebg.setCol((0.0, 0.0, 0.0, 0.0))
        self.pausetext = Text(36, -60, self.font, "0")
        self.pausetext.setScale((3.0, 3.0))
        self.pausetext.setAnchor("center")
        self.pausetext.setCol((0.0, 0.0, 0.0, 0.0))

        self.pauseVisible = False

        self.subSprites.append(self.bar)
        self.subSprites.append(self.pausebg)
        self.subSprites.append(self.pausetext)

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

    def scaleValue(self, perc):
        self.value *= perc
        self.max *= perc

    def addPause(self, time):
        self._pause += time
        
        if self._pause > MAX_PAUSE_TIME_SEC:
            self._pause = MAX_PAUSE_TIME_SEC

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

    def hidePause(self):
        if not self.pauseVisible:
            return
        
        self.pauseVisible = False
        self.pausebg.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.2)
        self.pausetext.fadeTo((0.0, 0.0, 0.0, 0.0), self.currentTime, 0.2)
    
    def update(self, currentTime):
        Sprite.update(self, currentTime)

        if self.value <= 0:
            pygame.event.post(pygame.event.Event(EVENT_GAME_OVER))
            return

        if self._pause <= 0 and self._halted <= 0:
            self.value -= 1
        elif self._halted <= 0:
            self._pause -= (self.currentTime - self.lastTime)

        if self._pause > 0:
            self.pausetext.setText("%d" % ceil(self._pause))
            self.showPause()
        else:
            self.hidePause()

        #self.image.fill([0,0,0])
        #self.image.set_alpha(200);
        p = float(self.value) / self.max

        if p > 1.0:
            p = 1.0

        self.bar.scaleTo((72, -p*96), currentTime, 0.1)
        self.bar.fadeTo((1 - p, p, 0.0, 1.0), currentTime, 0.1)
        #pygame.draw.rect(self.image, [(1-p)*255,p*255,0], [0,(1-p)*150,90,150])
        