from globals import *

from mixer import *

from sprite import *
from animation import *

mixer = Mixer()

class Marker(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.setAnimation(Animation("marker.png", 32, 32))
        
        self.boardx = 0
        self.boardy = 0
        
        self.offset_x = 0
        self.offset_y = 0

        self.scale_x = 16
        self.scale_y = 16
        
        self.setPos((self.boardx * self.scale_x + self.offset_x, self.boardy * self.scale_y + self.offset_y))

        self.movesound = Resources().getSound("markermove")  
        self.turnsound = Resources().getSound("markerturn")  
        self.failsound = Resources().getSound("markerfail")  
        
    def moveToBoardCoord(self, boardx, boardy, currentTime):
        self.boardx = boardx
        self.boardy = boardy
        self.moveTo((self.boardx * self.scale_x + self.offset_x, self.boardy * self.scale_y + self.offset_y), currentTime, 0.0)

    def move(self, dx, dy, currentTime):
        mixer.playSound(self.movesound)
        self.moveToBoardCoord(self.boardx + dx, self.boardy + dy, currentTime)
              
    def turn(self):
        mixer.playSound(self.turnsound)
        
    def fail(self):
        mixer.playSound(self.failsound)
        