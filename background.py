
from scene import *
from scenehandler import *
from board import *
from block import *
from font import *
from text import *
from sprite import *
from math import *
import random


class BGSprite(Sprite):
    def __init__(self, maincolor, imagefile, count):
        Sprite.__init__(self)

        self.maincolor = maincolor

        self.bg_image = loadImage(imagefile, 128, 128)
        self.shapes = []
        for i in xrange(count):
            s = Sprite()
            s.setImage(self.bg_image)
            s.softblend = True
            s.center = (64, 64)
            s.setCol(maincolor + (1.0, ))
            self.shapes.append(s)
        
        self.lowestSpeed = 5
        self.speed = 0
        self.spin = 40
        self.decline = 15
        self.boosts = 0

        self.setPos((160, 120))
        self.center = (160, 120)

        self.setCol((1.0, 1.0, 1.0, 0.3))
        self.pulsate()
        
    def update(self, currentTime):
        Sprite.update(self, currentTime)
        
        if (self.boosts > 0):
            self.speed += self.spin
            self.boosts -= 1
        else:
            self.speed -= self.decline * (self.currentTime - self.lastTime)
            
            if (self.speed <= self.lowestSpeed):
                self.speed = self.lowestSpeed
                
        self.animate(self.speed)
        
    def pulsate(self):
        self.clearColCallbacks()
        
        def fadeOut(sprite):
            self.fadeTo((1.0, 1.0, 1.0, 0.2), self.currentTime, 1.0, fadeIn)
            
        def fadeIn(sprite):    
            self.fadeTo((1.0, 1.0, 1.0, 0.5), self.currentTime, 1.0, fadeOut)
                
        fadeIn(None)

    def glow(self, count):
        self.clearColCallbacks()

        def done(sprite):
            self.pulsate()
            
        def fadeOut(sprite):
            self.fadeTo((1.0, 1.0, 1.0, 0.2), self.currentTime, 1.0 * count, done)

        def fadeIn(sprite):    
            self.fadeTo((1.0, 1.0, 1.0, 1.0), self.currentTime, 0.1, fadeOut)
                           
        fadeIn(None)
            
    def boost(self, count):
        self.boosts += count
        self.glow(count)
            
                
class BG_Square(BGSprite):
    def __init__(self):
        BGSprite.__init__(self, (0.5, 1.0, 0.1), "bg_square.png", 10)
            
        for i in xrange(9):
            self.shapes[i].subSprites.append(self.shapes[i+1])
            self.shapes[i+1].setPos((64, 64))
            self.shapes[i+1].setScale((0.95, 0.95))
            self.shapes[i+1].velx = 10 + (i % 2) * -20
            self.shapes[i+1].vely = 6 + (i % 2) * -12    
            
        self.shapes[0].setScale((2.5, 2.5))
        self.shapes[0].setPos((160, 120))
        
        self.subSprites.append(self.shapes[0])

    def animate(self, speed):
        self.rotateTo(self.rot + speed, self.currentTime, 1.0)   
        
        for i in xrange(9):
            j = i + 1
            shape = self.shapes[j]
            sx, sy = shape.pos
            rot = self.shapes[j].rot

            shape.rotateTo(shape.rot + speed, self.currentTime, 1.0)   
            
            if (sx > 72 and shape.velx > 0):
                shape.velx = -shape.velx
            if (sx < 56 and shape.velx < 0):
                shape.velx = -shape.velx
            if (sy > 72 and shape.vely > 0):
                shape.vely = -shape.vely
            if (sy < 56 and shape.vely < 0):
                shape.vely = -shape.vely
                           
            shape.moveTo((sx + shape.velx, sy + shape.vely), self.currentTime, 1.0)
 
                
class BG_Triangle(BGSprite):
    def __init__(self):
        BGSprite.__init__(self, (0.1, 0.1, 1.0), "bg_triangle.png", 10)
         
        for i in xrange(10):
            #self.shapes[i].subSprites.append(self.shapes[i+1])
            self.shapes[i].setScale((1.0 * exp(i/3.5), 1.0 * exp(i/3.5)))
            print self.shapes[i].scale
            self.shapes[i].setPos((160, 120))
            self.shapes[i].order = i
            self.subSprites.append(self.shapes[i])
            
    def animate(self, speed):
        self.rotateTo(self.rot + speed, self.currentTime, 1.0)
        nspeed = speed / 100.0

        for i in xrange(10):
            shape = self.shapes[i]
            scx = shape.scale[0]
            shape.rotateTo(shape.rot + i, self.currentTime, 1.0)
            
            sx, sy = shape.scale
            sx *= (1 + nspeed)
            sy *= (1 + nspeed)
            shape.scaleTo((sx, sy), self.currentTime, 1.0)
                        
            if (scx >= 16.0):
                shape.setScale((scx/16.0, scx/16.0))
                shape.scaleTo((sx/16.0, sx/16.0), self.currentTime, 1.0)
                shape.setCol((self.maincolor + (0.0,)))
                shape.fadeTo(self.maincolor + (1.0,), self.currentTime, 0.5)

                
class BG_Heart(BGSprite):
    def __init__(self):
        BGSprite.__init__(self, (1.0, 0.1, 0.1), "bg_heart.png", 10)
         
        for i in xrange(10):
            self.shapes[i].setScale((1.0 * exp(i/3.5), 1.0 * exp(i/3.5)))
            self.shapes[i].setPos((160, 120))
            self.shapes[i].order = i
            self.subSprites.append(self.shapes[i])

        self.counter = 0.0
        
            
    def animate(self, speed):
        nspeed = speed / 500.0
        self.counter += nspeed
        self.rotateTo(self.rot - 30 * nspeed, self.currentTime, 0.05)
        

        for i in xrange(10):
            shape = self.shapes[i]
            shape.rotateTo(90 * sin(self.counter - (i/5.0)), self.currentTime, 0.05)
            

    
class BG_Plus(BGSprite):
    def __init__(self):
        BGSprite.__init__(self, (1.0, 0.5, 0.6), "bg_plus.png", 10)

        self.shapes[0].setPos((160, 120))
        self.shapes[0].setScale((2.0, 2.0))
        
        for i in xrange(3):
            self.shapes[0].subSprites.append(self.shapes[i+1])
            self.shapes[i+1].setScale((0.7, 0.7))
            self.shapes[i+1].setPos((64 + 56*cos(i * 90), 64 + 56*sin(i * 90)))

            for j in xrange(3):
                self.shapes[i+1].subSprites.append(self.shapes[j+4])
                self.shapes[j+4].setScale((0.7, 0.7))
                self.shapes[j+4].setPos((64 + 56*cos(j * 90), 64 + 56*sin(j * 90)))
            
        self.subSprites.append(self.shapes[0])    
        self.counter = 0.0
        
            
    def animate(self, speed):
        nspeed = speed / 500.0
        self.counter += nspeed      
        self.rotateTo(self.rot - 30 * nspeed, self.currentTime, 0.05)
        sx = sin(self.counter) * 0.5 + 1.0
        self.scaleTo((sx, sx), self.currentTime, 0.2)
        
        for i in xrange(3):
            shape = self.shapes[i+1]
            shape.rotateTo(shape.rot - 30 * nspeed, self.currentTime, 0.05)
            shape.moveTo((64 + 48*cos(i * 90 + self.counter), 64 + 48*sin(i * 90 + self.counter)), self.currentTime, 0.05)

            for j in xrange(3):
                shape = self.shapes[j+4]
                shape.rotateTo(shape.rot - 30 * nspeed, self.currentTime, 0.05)
                shape.moveTo((64 + 48*cos(j * 90 + self.counter), 64 + 48*sin(j * 90 + self.counter)), self.currentTime, 0.05)
            
            
                
class BG_Circle(BGSprite):
    def __init__(self):
        BGSprite.__init__(self, (0.1, 0.9, 1.0), "bg_circle.png", 10)
         
        for i in xrange(10):
            self.shapes[i].setScale((8.0 - (i * 0.75), 8.0 - (i * 0.75)))
            self.shapes[i].setPos((160, 120))
            self.shapes[i].order = i
            self.subSprites.append(self.shapes[i])

        self.counter = 0.0
        
            
    def animate(self, speed):
        nspeed = speed / 400.0
        self.counter += nspeed
        self.rotateTo(self.rot + 30 * nspeed, self.currentTime, 0.05)

        sx = sin(self.counter)
        sy = cos(self.counter)
        r = 64 * sin(self.counter * nspeed) + 64 * cos(self.counter * nspeed)

        
        self.shapes[0].moveTo((160 + sx * r, 120 + sy *r), self.currentTime, 0.05)
        self.shapes[0].rotateTo(self.rot + 30 * nspeed, self.currentTime, 0.02)
        
        for i in xrange(9):
            parent = self.shapes[i]
            shape = self.shapes[i + 1]
            shape.moveTo(parent.pos, self.currentTime, 0.08)

            
class BG_Cross(BGSprite):
    def __init__(self):
        BGSprite.__init__(self, (1.0, 0.9, 0.2), "bg_cross.png", 10)

        self.shapes[0].setPos((160, 120))
        self.shapes[0].setScale((2.0, 2.0))
        
        for i in xrange(9):
            self.shapes[0].subSprites.append(self.shapes[i+1])
            self.shapes[i+1].setScale((0.7, 0.7))
            self.shapes[i+1].setPos((64 + 64*cos(i * (2.0*pi/9.0)), 64 + 64*sin(i * (2*pi/9.0))))
            
        self.subSprites.append(self.shapes[0])    
        self.counter = 0.0
        
            
    def animate(self, speed):
        nspeed = speed / 900.0
        self.counter += nspeed      
        self.rotateTo(self.rot - 30 * nspeed, self.currentTime, 0.05)


        self.shapes[0].rotateTo(self.counter*100, self.currentTime, 0.02)
        
        for i in xrange(9):
            shape = self.shapes[i + 1]
            sx = sin(self.counter + i * (2.0*pi/9.0))
            sy = cos(self.counter + i * (2.0*pi/9.0))
            r = 64 * cos(self.counter * 2 + i*0.15)
            shape.moveTo((64 + sx*r, 64 + sy*r), self.currentTime, 0.08)
            shape.rotateTo(self.counter*200, self.currentTime, 0.1)
            shape.scaleTo((r/32.0, r/32.0), self.currentTime, 0.2)

                
class BG_Diamond(BGSprite):
    def __init__(self):
        BGSprite.__init__(self, (0.8, 0.1, 1.0), "bg_diamond.png", 10)
         
        for i in xrange(10):
            self.shapes[i].setScale((4.0, 4.0))
            self.shapes[i].setPos((160, 120))
            self.shapes[i].order = i
            self.subSprites.append(self.shapes[i])

        self.counter = 0.0
        
                
    def animate(self, speed):
        nspeed = speed / 200.0
        self.counter += nspeed
        self.rotateTo(self.rot + 30 * nspeed, self.currentTime, 0.05)
        
        sx = sin(self.counter/2.0)
        sy = cos(self.counter/2.0)
        r = 96* sin(self.counter * 0.2)

        self.shapes[0].moveTo((160 + sx * r, 120 + sy *r), self.currentTime, 0.05)
            
        for i in xrange(9):
            parent = self.shapes[9 - i - 1]
            shape = self.shapes[9 - i]
            shape.moveTo((parent.pos), self.currentTime, 0.1)


            
class Background(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.setPos((0, 0))

        self.shapes = [BG_Diamond(),
                       BG_Cross(),
                       BG_Square(),
                       BG_Triangle(),
                       BG_Heart(),
                       BG_Circle(),
                       BG_Plus()]
        self.shapeCount = len(self.shapes)
        
        self.currentShape = self.shapes[0]
        self.subSprites.append(self.currentShape)
        
    def update(self, currentTime): 
        Sprite.update(self, currentTime)
        self.currentShape.update(currentTime)

    def boost(self, count):
        self.currentShape.boost(count)

    def setTheme(self, shape):
        shape = shape % self.shapeCount    
            
        self.subSprites.remove(self.currentShape)
        self.currentShape = self.shapes[shape]    
        self.subSprites.append(self.currentShape)
        pass
