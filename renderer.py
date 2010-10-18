import operator

from scene import *
from singleton import *

import pygame
from pygame.locals import *

from OpenGL.GL import *

from globals import *

RES_SCALE = 2

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
        self.softblend = False
        
        self.width = 0
        self.height = 0
        self.currentTexture = None

        
    def init(self, title, width, height, fullscreen = False):
        self.width = width
        self.height = height
        self.title = title
        self.fullscreen = fullscreen
        # Initialize screen and window
        self.setDisplay()
    
    def cleanup():
        unloadTextures()
        pygame.display.quit()
        
    def setDisplay(self):
        ##pygame.display.quit()
        if (self.fullscreen == True):
            self.screen = pygame.display.set_mode((self.width * RES_SCALE, self.height * RES_SCALE), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.OPENGL)
        else:
            self.screen = pygame.display.set_mode((self.width * RES_SCALE, self.height * RES_SCALE), pygame.HWSURFACE | pygame.OPENGL | pygame.DOUBLEBUF)
    
        pygame.display.set_caption(self.title)
        pygame.mouse.set_visible(0)
        # OpenGL stuff
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_CULL_FACE)
        glDisable(GL_DEPTH_TEST)        
        glShadeModel(GL_FLAT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        #glEnableClientState(GL_VERTEX_ARRAY)
        #glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glViewport(0, 0, self.width * RES_SCALE, self.height * RES_SCALE)
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

        if (sprite.softblend != self.softblend):
            if (sprite.softblend == True):
                glBlendFunc(GL_ONE, GL_ONE)
                pass
            else:
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                pass
            self.softblend = sprite.softblend    

        
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
            i = sprite.currentImage
            if (self.currentTexture != i.texture.texID):
                glBindTexture(GL_TEXTURE_2D, i.texture.texID)
                self.currentTexture = i.texture.texID

            #glVertexPointer(2, GL_FLOAT, 0, i.vCoords)
            #glTexCoordPointer(2, GL_FLOAT, 0, i.tCoords)
            #glDrawArrays(GL_QUADS, 0, 4)
            
            glBegin(GL_QUADS)
            glTexCoord2f(i.tCoords[0], i.tCoords[1])
            glVertex2f(i.vCoords[0], i.vCoords[1])
            glTexCoord2f(i.tCoords[2], i.tCoords[3])
            glVertex2f(i.vCoords[2], i.vCoords[3])
            glTexCoord2f(i.tCoords[4], i.tCoords[5])
            glVertex2f(i.vCoords[4], i.vCoords[5])
            glTexCoord2f(i.tCoords[6], i.tCoords[7])
            glVertex2f(i.vCoords[6], i.vCoords[7])
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
        
        
    
