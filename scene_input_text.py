from scene import *
from scenehandler import *
from board import *
from block import *
from font import *
from text import *
from sprite import *
import random

import scene_highscore

class Scene_InputText(Scene):
    def _runOnce(self):
        Scene._runOnce(self)

        self.font = Font("font_fat.png", 8, 8);

        self.text = Text(160, 120, self.font, "")
        self.text.setAnchor("center")
        self.text.setScale((2.0, 2.0))

        self.sprites.add(self.text)

        self.updateBlocker = True

        self.text_buffer = ""
        self.text_buffer_counter = 0
        self.current_char = "A##"
        
        self.ticker = 0

        self.callback = None
        self.length = 3

    def display(self, x=0, y=0, length=0, callback=None):
        self.text.setPos((x, y))
        self.length = length
        self.text_buffer = ""
        self.text_buffer_counter = 0
        self.current_char = "A"
        self.callback = callback

        SceneHandler().pushScene(self)

    def tick(self):
        text = self.text_buffer

        if self.text_buffer_counter < self.length:
            if self.ticker in range(0,5):
                text = text + self.current_char
            elif self.ticker in range(5, 9):
                text = text + "#"
            else:
                text = text + "#"
                self.ticker = 0
                
            self.ticker += 1

        self.text.setText(text)
                    
    def show(self):
        print self, "is showing"
        
    def hide(self):
        print self, "is hiding"

    def handleEvent(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                c = ord(self.current_char)-1
                if c < (ord("A")):
                    c = ord("Z")

                self.current_char = chr(c)

            if event.key == K_DOWN:
                c = ord(self.current_char)+1
                if c > (ord("Z")):
                    c = ord("A")

                self.current_char = chr(c)

            if event.key == K_RETURN:
                if self.text_buffer_counter < self.length:
                    self.text_buffer_counter += 1
                    self.text_buffer += self.current_char

                elif self.text_buffer_counter >= self.length:
                    SceneHandler().removeScene(self)
                    
                    if self.callback:
                        self.callback(self.text_buffer)

        return True
        
