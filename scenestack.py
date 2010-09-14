import singleton
from singleton import *

class SceneStack(Singleton):
    def _runOnce(self):
        self.sceneStack = []
        self.allScenes = []
        self.focus = 0
        self.currentTime = 0
        
    def registerScene(self, scene):
        self.allScenes.append(scene)
    
    def unregisterScene(self, scene):
        self.allScenes.remove(scene)
    
    def pushScene(self, scene):
        try:
            self.sceneStack.remove(scene)
        except:
            pass
        self.sceneStack.append(scene)
        print "pushed", scene, "onto", self.sceneStack
        scene.show()
        self.focusScene(scene)
        
    def removeScene(self, scene):
        try:
            self.sceneStack.remove(scene)
        except:
            return
        print "removed", scene, "from", self.sceneStack
        scene.hide()
        if (self.focus == scene):
            self.focus = 0
            if (len(self.sceneStack) > 0):
                for s in reversed(sceneStack):
                    if (s.canBeFocused() == True):
                        this.focusScene(s)
        return scene
        
    def focusScene(self, scene):
        if (self.focus != 0):
            self.focus.unfocus()
        scene.focus()
        self.focus = scene
        
    def handleKeyInput(self, key, keystate):
        for scene in reversed(self.sceneStack):
            if (scene.handleKeyInput(key, keystate) == True):
                break
    
    def update(self, deltaTime):
        self.currentTime += deltaTime
        self.updateScenes(deltaTime)
    
    def updateScenes(self, deltaTime):
        for scene in reversed(self.sceneStack):
            scene.update(deltaTime)
            if (scene.isBlockingUpdates() == True):
                break
        
    def renderScenes(self, screen):
        renderStack = []
        for scene in reversed(self.sceneStack):
            renderStack.append(scene)
            if (scene.isBlockingRendering() == True):
                break
        
        for scene in reversed(renderStack):
            scene.render(screen)
            
