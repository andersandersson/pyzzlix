import os, pygame
from pygame import *

# Functions to create our resources
images = dict()

def loadImage(filename, colorkey=None):
    image = 0
    try: 
        image = images[filename]
    except:            
        fullname = os.path.join('data', filename)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
        images[filename] = image 
            
    image = image.convert()
    image.set_colorkey((0, 0, 0), RLEACCEL)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

# Loads a list of images from a larger ones. Each subimage is the same size.
# This function generates as many subimages that fits wholly on the source image.
def loadImageSheet(filename, w, h, colorkey=None):
    sheet = []
    image = 0
    masterImage = loadImage(filename, colorkey)

    masterWidth, masterHeight = masterImage.get_size()
    for j in xrange(int(masterHeight/h)):
        for i in xrange(int(masterWidth/w)):
                name = filename + "__" + str(i) + "__" + str(j)
                try: 
                    image = images[name]
                except:
                    image = masterImage.subsurface((i*w, j*h, w, h))
                    images[name] = image
                    print name
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