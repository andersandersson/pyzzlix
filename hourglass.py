from globals import *

from sprite import *
from image import *

class Hourglass(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.loadSheet("font_normal.bmp", 1, 1)
        
        self.setScale((90, -150))
        self.setPos((BOARD_WIDTH*16+3*16, 240 - 16))
        self.value = 0
        self.max = 0
        
        self.timeatlastframe = 0
        self.frameDelay = 0.1
        self.frame = 0
        
        self.reset(1000)

    def reset(self, value):
        self.value = value*0.5
        self.max = value

    def update(self, currentTime):
        if self.value <= 0:
            pygame.event.post(pygame.event.Event(EVENT_GAME_OVER))
            return
        if self.value > self.max:
            pygame.event.post(pygame.event.Event(EVENT_LEVEL_UP))
            return

            
        self.value -= 1
        #self.image.fill([0,0,0])
        #self.image.set_alpha(200);
        p = float(self.value) / self.max
        self.scaleTo((90, -p*150), currentTime, 0.1)
        self.fadeTo((1 - p, p, 0.0, 1.0), currentTime, 0.1)
        #pygame.draw.rect(self.image, [(1-p)*255,p*255,0], [0,(1-p)*150,90,150])
