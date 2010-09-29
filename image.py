
class Image():
    def __init__(self, texture, srcx = 0, srcy = 0, width = None, height = None):
        self.texture = texture
        self.srcx = srcx
        self.srcy = srcy       
        if (width == None):
            self.width = texture.width + 0.0
        else:
            self.width = width + 0.0
        if (height == None):
            self.height = texture.height + 0.0
        else:
            self.height = height + 0.0
            
        tx1 = self.srcx * self.texture.pw
        ty1 = self.srcy * self.texture.ph
        tx2 = (self.srcx + self.width) * self.texture.pw
        ty2 = (self.srcy + self.height) * self.texture.ph
        
        self.vCoords = (0.0, 0.0, 0.0, self.height, self.width, self.height, self.width, 0.0)
        
        self.tCoords = (tx1, ty1, tx1, ty2, tx2, ty2, tx2, ty1)
        