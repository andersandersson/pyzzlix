
class Image():
    def __init__(self, texture, srcx = 0, srcy = 0, width = -1, height = -1):
        self.texture = texture
        self.srcx = srcx
        self.srcy = srcy        
        if (width <= 0):
            self.width = texture.width
        else:
            self.width = width
        if (height <= 0):
            self.height = texture.height
        else:
            self.height = height
            