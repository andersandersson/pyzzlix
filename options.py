from globals import *
from resources import *
from singleton import *

class Options(Singleton):
    defaults = {"music_volume": VOLUME_STEPS,
                "sound_volume": VOLUME_STEPS,
                "show_tutorials": True,
                "fullscreen": False,
                }
    options = {}
    
    def _runOnce(self):
        pass

    def getDefault(self, name):
        if self.defaults and name in self.defaults:
            return self.defaults[name]
        else:
            return None
    
    def get(self, name, default=None):
        self.options = Resources().getData("options")
        
        if not self.options or not name in self.options:
            return self.getDefault(name)

        return self.options[name]

    def set(self, name, value):
        self.options = Resources().getData("options")

        if not self.options:
            self.options = {}

        self.options[name] = value

        Resources().setData("options", self.options)
        Resources().saveData()
