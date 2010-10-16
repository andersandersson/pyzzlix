from globals import *

class Animation():
    def __init__(self, name, width, height, srcx = 0, srcy = 0, srcw = None, srch = None, currentTime = 0.0, frameLength = 0.1, mode = "loop", reverse = False):
        self.images = loadImageSheet(name, width, height, srcx, srcy, srcw, srch)
        if (mode == "loop" or mode == "pingpong" or mode == "normal"):
            self.mode = mode
        else:
            self.mode = "normal"
        
        self.reverse = reverse
        self.reset(currentTime)    
        self.frameLengths = self.frameCount * [frameLength]
        
    def reset(self, currentTime):
        self.frameTimer = currentTime
        self.frameCount = len(self.images)
            
        if (self.reverse == True):
            self.direction = -1
            self.frame = self.frameCount - 1
        else:
            self.direction = 1
            self.frame = 0
        
    def getFrameImage(self, currentTime):
        if (self.frameCount > 0):
            while (self.frameTimer + self.frameLengths[self.frame] <= currentTime):
                self.frameTimer += self.frameLengths[self.frame]
                self.frame += 1 * self.direction
                if self.frame >= self.frameCount:
                    if (self.mode == "loop"):
                        self.frame = 0
                    elif (self.mode == "pingpong"):
                        self.frame = self.frameCount - 1
                        self.direction = -1
                    else:
                        self.frameCount = 0
                        self.frame = self.frameCount - 1
                elif self.frame < 0:
                    if (self.mode == "loop"):
                        self.frame = self.frameCount - 1
                    elif (self.mode == "pingpong"):
                        self.frame = 0
                        self.direction = 1
                    else:
                        self.frameCount = 0
                        self.frame = 0
                   
        return self.images[self.frame]       
       