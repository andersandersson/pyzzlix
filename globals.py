import os, pygame
from pygame import *

from image import *

from OpenGL.GL import *
from OpenGL.GLU import *

from texture import *



BOARD_WIDTH = 10
BOARD_HEIGHT = 13

HOURGLASS_DEFAULT = 1000

EVENT_CIRCLE_FOUND = USEREVENT
EVENT_GAME_OVER = USEREVENT+1
EVENT_LEVEL_UP = USEREVENT+2

# Functions to create our resources
textures = dict()


def initTexture(texture):
    imagefile = 0
    fullname = texture.fullname
    try:
        imagefile = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load texture:', fullname
        raise SystemExit, message
    textureID = glGenTextures(1)
    imagefile.convert_alpha()
    data = pygame.image.tostring(imagefile, "RGBA", False)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, imagefile.get_width(), imagefile.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    imageWidth, imageHeight =  imagefile.get_size()
    texture.updateData(textureID, imageWidth, imageHeight)

# Loads an image
def loadImage(filename, srcx = 0, srcy = 0, srcw = None, srch = None):
    texture = 0
    try: 
        texture = textures[filename]
    except:            
        fullname = os.path.join('data', filename)
        texture = Texture(fullname)
        initTexture(texture)
        textures[filename] = texture 
    return Image(texture, srcx, srcy, srcw, srch)

def reloadTextures():
    for t in textures:
        initTexture(textures[t])

# Loads a list of images from a larger ones. Each subimage is the same size.
# This function generates as many subimages that fits wholly on the source image.
def loadImageSheet(filename, w, h, srcx = 0, srcy = 0, srcw = None, srch = None):
    sheet = []
    image = 0
    masterImage = loadImage(filename)
    sourcex = srcx
    sourcey = srcy
    if (srcw == None):
        sourceWidth = masterImage.texture.width
    else:
        sourceWidth = srcw
        
    if (srch == None):
        sourceHeight = masterImage.texture.height
    else:
        sourceHeight = srch
  
    for j in xrange(int(sourceHeight/h)):
        for i in xrange(int(sourceWidth/w)):
            image = Image(masterImage.texture, sourcex + i*w, sourcey + j*h, w, h)
            sheet.append(image)
    
    try:
        image = sheet[0]
    except pygame.error, message:
        print 'Could not load image(s) from:', fullname
        raise SystemExit, message
            
    return sheet

def loadSound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound
