from globals import *

from sprite import *

class Menu(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        
        self.items = []
        self.focus = 0
        self.count = 0
        
    def add(self, item):
        self.subSprites.append(item)
        self.items.append(item)
        self.count = len(self.items)

    def setFocusCol(self, col):
        for item in self.items:
            item.focusColor = col
            if item.inFocus:
                item.focus(self.currentTime)
        
    def setUnfocusCol(self, col):
        for item in self.items:
            item.unfocusColor = col
            if not item.inFocus:
                item.unfocus(self.currentTime)
        
    def setFocusScale(self, scale):
        for item in self.items:
            item.focusScale = scale
            if item.inFocus:
                item.focus(self.currentTime)
        
    def setUnfocusScale(self, scale):
        for item in self.items:
            item.unfocusScale = scale
            if not item.inFocus:
                item.unfocus(self.currentTime)
        
    def focusItem(self, newfocus):
        if (newfocus < 0):
            newfocus = self.count - 1
            
        if (newfocus >= self.count):
            newfocus = 0
    
        #Mixer().playSound(self.movesound)
        self.items[self.focus].unfocus(self.currentTime)
        self.items[newfocus].focus(self.currentTime)
        self.focus = newfocus            

    def nextItem(self):
        self.focusItem(self.focus + 1)

    def prevItem(self):
        self.focusItem(self.focus - 1)

    def unfocusItem(self):
        self.items[self.focus].unfocus(self.currentTime)
        
    def selectItem(self):
        self.items[self.focus].select()
