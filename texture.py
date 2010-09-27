
class Texture():
    def __init__(self, fullname):
        self.fullname = fullname
        self.texID = -1
        self.width = 1.0
        self.height = 1.0
        self.pw = 1.0/self.width
        self.ph = 1.0/self.height
        
    def updateData(self, texID, width, height):
        self.texID = texID
        self.width = width
        self.height = height
        self.pw = 1.0/self.width
        self.ph = 1.0/self.height
    
    