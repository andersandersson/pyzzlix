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

    def selectItem(self):
        self.items[self.focus].select()
