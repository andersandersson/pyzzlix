from globals import *
from renderer import *
from singleton import *

class SceneHandler(Singleton):
    def _runOnce(self):
        self.sceneStack = []
        self.allScenes = []
        self.focus = 0
        self.currentTime = 0
        
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
                for s in reversed(self.sceneStack):
                    if (s.canBeFocused() == True):
                        this.focusScene(s)
        return scene
        
    def focusScene(self, scene):
        if (self.focus != 0):
            self.focus.unfocus()
        scene.focus()
        self.focus = scene
        
    def handleEvent(self, event):
        for scene in reversed(self.sceneStack):
            if (scene.handleEvent(event) == True):
                break
    
    def update(self, deltaTime):
        self.currentTime += deltaTime
        self.updateScenes(deltaTime)
    
    def updateScenes(self, deltaTime):
        for scene in reversed(self.sceneStack):
            scene.update(deltaTime)
            if (scene.isBlockingUpdates() == True):
                break
        
    def renderScenes(self):
        renderer = Renderer()
        renderStack = []
        for scene in reversed(self.sceneStack):
            renderStack.append(scene)
            if (scene.isBlockingRendering() == True):
                break       
        for scene in reversed(renderStack):
            renderer.render(scene)
