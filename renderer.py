from scene import *
from singleton import *

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import scenehandler

class Renderer(Singleton):
    def _runOnce(self):
        self.screen = 0
        self.fullscreen = False
        self.title = "The Game"
        self.scenehandler = scenehandler.SceneHandler()
        self.currentTime = 0.0
        self.deltaT = 0.0
        
    def init(self, title, width, height, fullscreen = False):
        self.width = width
        self.height = height
        self.fullscreen = fullscreen
        self.title = title
        # Initialize screen and window
        self.setDisplay()
        pygame.display.set_caption(self.title)
        pygame.mouse.set_visible(0)
        # OpenGL stuff
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_CULL_FACE)
        glDisable(GL_DEPTH_TEST)        
        glShadeModel(GL_FLAT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(1.0, 0.7, 0.0, 0.0)
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, 0, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
    def setDisplay(self):
        if (self.fullscreen == True):
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.OPENGL)
        else:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.HWSURFACE | pygame.OPENGL | pygame.DOUBLEBUF)
    
    def toggleFullScreen(self):
        self.fullscreen = not self.fullscreen
        self.setDisplay()    
                
    def drawSprite(self, sprite, currentTime):
        glPushMatrix()
        if (sprite._reftime_pos <= currentTime):
            x = sprite._ref_x
            y = sprite._ref_y
        else:
            factorT = (sprite._reftime_pos - currentTime) / (sprite._reftime_pos - sprite._updatetime)
            x = sprite._ref_x - (sprite._ref_x - sprite.x) * factorT
            y = sprite._ref_y - (sprite._ref_y - sprite.y) * factorT
            #print "ref:", sprite._reftime_pos, "time:",  time, "sx:", sprite.x, "sy:", sprite.y, "utime:", sprite._updatetime
        #print "x:", x, "y:", y
        
        glTranslatef(x, y, 0.0)
        if (sprite.currentImage != 0):
            image = sprite.currentImage
            srcx1 = image.srcx * image.texture.pw
            srcx2 = srcx1 + image.width * image.texture.pw
            srcy1 = image.srcy * image.texture.ph
            srcy2 = srcy1 + image.height * image.texture.ph
            
            glBindTexture(GL_TEXTURE_2D, image.texture.texID)
            glBegin(GL_QUADS)
            glTexCoord2f(srcx1, srcy1)
            glVertex2f(0.0, 0.0)
            glTexCoord2f(srcx1, srcy2)
            glVertex2f(0.0, image.height)
            glTexCoord2f(srcx2, srcy2)
            glVertex2f(image.width, image.height)
            glTexCoord2f(srcx2, srcy1)
            glVertex2f(image.width, 0.0)
            glEnd()
                
        for subsprite in sprite.subSprites:
            self.drawSprite(subsprite)
                
        glPopMatrix()
                
    def renderScene(self, scene):
        scene.renderTime += self.deltaT
        if (self.screen != 0):
            #for layer in scene.sprites.layers():
                #for sprite in scene.sprites.get_sprites_from_layer(layer):
                    #sprite.draw(self.screen)
            for spritelist in scene.sprites:
                if spritelist:
                    for sprite in spritelist:
                        self.drawSprite(sprite, scene.renderTime)   
                    
    def render(self, deltaT):                
        self.deltaT = deltaT
        self.currentTime += deltaT
        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT);
        glLoadIdentity();
        glColor3f(1.0, 1.0, 1.0)
          
        self.scenehandler.renderScenes()
        pygame.display.flip()
        
        
    
