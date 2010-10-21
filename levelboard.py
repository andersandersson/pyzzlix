from globals import *

from sprite import *
from animation import *
from text import *
from block import *

class Levelboard(Sprite):
    def __init__(self):
        Sprite.__init__(self)
    
        self.font = Font("font_fat.png", 8, 8)

        self.leveltext = Text(44.0, 12, self.font, "LEVEL 00")      
        self.leveltext.setAnchor("center")
            
        self.blockposx = 20
        self.blockposy = 30
        self.block = None

        self.blockcounttext = Text(self.blockposx + 8, self.blockposy - 4, self.font, ":99/99")
         
   
        self.scorebg = Sprite()
        self.scorebg.setImage(loadImage("pixel.png", 1, 1))
        self.scorebg.setPos((8.0, 8.0))
        self.scorebg.setScale((72.0, 32.0))
        self.scorebg.setCol((0.0, 0.0, 0.0, 0.5))

        self.border = Sprite()
        self.border.setImage(loadImage("windowframes.png", 208, 80, 88, 48))
        self.border.setPos((0.0,0.0))
        
        self.glow = Sprite()
        self.glow.setImage(loadImage("windowglows.png", 208, 80, 88, 48))
        self.glow.setPos((0.0,8.0))
        self.glow.setCol((0.0, 0.0, 0.0, 0.0))
        
        self.subSprites.append(self.scorebg)
        self.subSprites.append(self.blockcounttext)
        self.subSprites.append(self.leveltext)
        self.subSprites.append(self.border)
        self.subSprites.append(self.glow)
        
        self.level = 0

        self._glow_col = (0.0, 0.0, 0.0, 0.0)
        self._glow_duration = 0.0

        self.completed = False

    def doBlink(self):
        
        def fadeIn(sprite):
            self.blockcounttext.fadeTo((1.0,1.0,1.0,1.0), self.currentTime, 0.05, fadeOut)       
        def fadeOut(sprite):
            self.blockcounttext.fadeTo((0.0,0.0,0.0,1.0), self.currentTime, 0.05, fadeIn)
        
        fadeOut(None)

    def updateLevelboard(self, currentblocks):
    
        if (self.currentblocks != currentblocks):
            self.block.doPulse()   
            
            if (self.completed == False):
                self.currentblocks = currentblocks
                    
                if (self.currentblocks >= self.goalblocks):
                    self.currentblocks = self.goalblocks
                    self.completed = True
                    self.doBlink()
    
                self.blockcounttext.setText(":%2d/%2d" % (self.currentblocks, self.goalblocks))
           
        
    def setNewLevel(self, level, block, goalblocks):
        self.level = level
    
        self.leveltext.setText("LEVEL %2d" % (self.level))   
        
        self.goalblocks = goalblocks
        self.currentblocks = 0
            
        self.completed = False
        self.blockcounttext.clearColCallbacks()
        self.blockcounttext.setCol((1.0,1.0,1.0,1.0)) 
        self.blockcounttext.setText(":%2d/%2d" % (self.currentblocks, self.goalblocks))
        
        oldblock = self.block
        self.block = Block(0, 0, block)
        self.block.setPos((self.blockposx, self.blockposy))
        self.block.setCol((1.0, 1.0, 1.0, 0.0))
        self.block.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.3)
        self.subSprites.append(self.block)
        
        if (oldblock != None):     
            def removeOldblock(sprite):
                self.subSprites.remove(oldblock)

            oldblock.fadeTo((1.0, 1.0, 1.0, 0.0), self.currentTime, 0.3, removeOldblock)
        
             
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
