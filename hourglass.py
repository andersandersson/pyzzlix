from globals import *

from sprite import *
from image import *

class Hourglass(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.setImage(loadImage("pixel.png", 1, 1))
        
        self.setScale((72, -96))
        self.setPos((232, 119 + 96))
        self.max = 0
        
        self.timeatlastframe = 0
        self.frameDelay = 0.1
        self.frame = 0
        self._value = 0
        self._pause = 0
        
        self.reset(1000)

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

    def pause(self, time):
        self._pause += time
    
    def update(self, currentTime):
        if self.value <= 0:
            pygame.event.post(pygame.event.Event(EVENT_GAME_OVER))
            return

        if self._pause <= currentTime:
            self.value -= 1
            self._pause = currentTime

        #self.image.fill([0,0,0])
        #self.image.set_alpha(200);
        p = float(self.value) / self.max

        if p > 1.0:
            p = 1.0

        self.scaleTo((72, -p*96), currentTime, 0.1)
        self.fadeTo((1 - p, p, 0.0, 1.0), currentTime, 0.1)
        #pygame.draw.rect(self.image, [(1-p)*255,p*255,0], [0,(1-p)*150,90,150])
