import os, pygame
from pygame import *

from image import *

from OpenGL.GL import *
from OpenGL.GLU import *

from texture import *

# Functions to create our resources
textures = dict()

# Loads an image
def loadImage(filename, colorkey=None):
    texture = 0
    try: 
        texture = textures[filename]
    except:            
        fullname = os.path.join('data', filename)
        imagefile = 0
        try:
            imagefile = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
        textureID = glGenTextures(1)
        imagefile.convert_alpha()
        data = pygame.image.tostring(imagefile, "RGBA", 1)
        glBindTexture(GL_TEXTURE_2D, textureID)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, imagefile.get_width(), imagefile.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        imageWidth, imageHeight =  imagefile.get_size()
        texture = Texture(textureID, imageWidth, imageHeight)
        textures[filename] = texture
        
    return Image(texture)

# Loads a list of images from a larger ones. Each subimage is the same size.
# This function generates as many subimages that fits wholly on the source image.
def loadImageSheet(filename, w, h, colorkey=None):
    sheet = []
    image = 0
    masterImage = loadImage(filename, colorkey)
    masterWidth = masterImage.texture.width
    masterHeight = masterImage.texture.height
    for j in xrange(int(masterHeight/h)):
        for i in xrange(int(masterWidth/w)):
                image = Image(masterImage.texture, i*w, j*h, w, h)
                sheet.append(image)
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