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
        
    def removeScene(self, scene):
        try:
            self.sceneStack.remove(scene)
        except:
            return
        print "removed", scene, "from", self.sceneStack
        scene.hide()
        return scene
    
    def handleEvent(self, event):
        for scene in reversed(self.sceneStack):
            if (scene.handleEvent(event) == True):
                break
    
    def updateTimers(self, deltaTime):
        self.currentTime += deltaTime
        for scene in reversed(self.sceneStack):
            scene.updateTimer(deltaTime)
            if (scene.isBlockingUpdates() == True):
                break
    
    def doSceneTicks(self):
        for scene in reversed(self.sceneStack):
            scene.tick()
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
            renderer.renderScene(scene)
