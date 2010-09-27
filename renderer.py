import operator

from scene import *
from singleton import *

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from globals import *

import scenehandler

class Renderer(Singleton):
    def _runOnce(self):
        self.screen = 0
        self.fullscreen = False
        self.title = "The Game"
        self.scenehandler = scenehandler.SceneHandler()
        self.currentTime = 0.0
        self.deltaT = 0.0
        self.colorStack = []
        self.currentColor = (1.0, 1.0, 1.0, 1.0)
        self.width = 0
        self.height = 0
        
    def init(self, title, width, height, fullscreen = False):
        self.width = width
        self.height = height
        self.title = title
        self.fullscreen = fullscreen
        # Initialize screen and window
        self.setDisplay()
        
    def setDisplay(self):
        if (self.fullscreen == True):
            self.screen = pygame.display.set_mode((self.width * 2, self.height * 2), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.OPENGL)
        else:
            self.screen = pygame.display.set_mode((self.width * 2, self.height * 2), pygame.HWSURFACE | pygame.OPENGL | pygame.DOUBLEBUF)
    
        pygame.display.set_caption(self.title)
        pygame.mouse.set_visible(0)
        # OpenGL stuff
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_CULL_FACE)
        glDisable(GL_DEPTH_TEST)        
        glShadeModel(GL_FLAT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glViewport(0, 0, self.width * 2, self.height * 2)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, 0, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        reloadTextures()
        
    
    def toggleFullScreen(self):
        glClear(GL_COLOR_BUFFER_BIT);
        pygame.display.flip()
        self.fullscreen = not self.fullscreen
        self.setDisplay()

                
    def drawSprite(self, sprite, currentTime):
        glPushMatrix()
        last_color = self.currentColor
        self.colorStack.append(self.currentColor)

        x, y = sprite.calcPos(currentTime)
        rot = sprite.calcRot(currentTime)
        sx, sy = sprite.calcScale(currentTime)

        calc_color = sprite.calcCol(currentTime)
        self.currentColor = tuple(map(operator.mul, calc_color, self.currentColor))

        r, g, b, a = self.currentColor

        cx, cy = sprite.center

        if not x == 0.0 or not y == 0.0:
            glTranslatef(x, y, 0.0)

        if not rot == 0.0:
            glRotatef(rot, 0.0, 0.0, 1.0)

        if not sx == 1.0 or not sy == 1.0:
            glScalef(sx, sy, 1.0)

        if not cx == 0.0 or not cy == 0.0:
            glTranslatef(-cx, -cy, 0.0)

        if not (1.0, 1.0, 1.0, 1.0) == calc_color:
            glColor4f(r, g, b, a)

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
            self.drawSprite(subsprite, currentTime)

        self.currentColor = self.colorStack.pop()
        
        if not (1.0, 1.0, 1.0, 1.0) == calc_color:
            r, g, b, a = self.currentColor
            glColor4f(r, g, b, a)

        glPopMatrix()
                
    def renderScene(self, scene):
        scene.renderTime += self.deltaT
        if (scene.softblend == True):
            glBlendFunc(GL_ONE, GL_ONE)
        else:
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        if (self.screen != 0):
            #for layer in scene.sprites.layers():
                #for sprite in scene.sprites.get_sprites_from_layer(layer):
                    #sprite.draw(self.screen)
            for sprite in scene.sprites:
                self.drawSprite(sprite, scene.renderTime)   
                    
    def render(self, deltaT):                
        self.deltaT = deltaT
        self.currentTime += deltaT
        # Clear the screen
        glClear(GL_COLOR_BUFFER_BIT);
        glLoadIdentity();
        self.currentColor = (1.0, 1.0, 1.0, 1.0)
          
        self.scenehandler.renderScenes()
        pygame.display.flip()
        
        
    
