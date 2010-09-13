
sceneStack = 0

background = 0
screen = 0


# Functions to create our resources
images = dict()

def loadImage(name, colorkey=None):
    image = 0
    try: 
        image = images[name]
    except:            
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
        images[name] = image 
            
    image = image.convert()
    image.set_colorkey((0, 0, 0), RLEACCEL)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

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