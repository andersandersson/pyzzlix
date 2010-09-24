
class Texture():
    def __init__(self, texID, width, height):
        self.texID = texID
        self.width = width
        self.height = height
        self.pw = 1.0/self.width
        self.ph = 1.0/self.height
        