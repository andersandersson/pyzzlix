from globals import *
from singleton import *

import json

class Resources(Singleton):
    sounds = {
        "menumove":  {"file": "menumove.ogg"},
        "menuselect": {"file": "menuselect.ogg"},
        "menustart": {"file": "menustart.ogg"},
        "markermove": {"file": "markermove.ogg"},
        "markerturn": {"file": "markerturn.ogg"},
        "markerfail": {"file": "markerfail.ogg"},
        "removeblock": {"file": "removeblock.ogg"},
        "combo": {"file": "circle.ogg"},
        "circle": {"file": "combo.ogg"},
        }

    music = {
        "menumusic":  {"file": "menumusic.ogg", "weight": 5},
        "music1_chord":  {"file": "music1_chord.ogg"},
        "music1_hh":  {"file": "music1_hh.ogg"},
        "music1_bass":  {"file": "music1_bass.ogg"},
        "music1_bass2":  {"file": "music1_bass2.ogg"},
        "music1_kick":  {"file": "music1_kick.ogg"},
        "music1_lead":  {"file": "music1_lead.ogg"},
        "music1_lead3":  {"file": "music1_lead3.ogg"},
        "music1_lead2":  {"file": "music1_lead2.ogg"},
        }

    data = None
    
    numResources = 0
    
    def _runOnce(self):
        def count_resource(resource):
            count = 0
            
            for name in resource:
                if "weight" in resource[name]:
                    count += resource[name]["weight"]
                else:
                    count += 1

            return count

        self.numResources = count_resource(self.sounds)
        self.numResources += count_resource(self.music)
                            
    def _getResource(self, name, resource, loadFunc):
        if name in resource:
            if "obj" in resource[name]:
                print "RESOURCE %s EXITS" % name
                return resource[name]["obj"]
            else:
                print "RESOURCE %s NOT LOADED, LOADING" % name
                resource[name]["obj"] = loadFunc(resource[name]["file"])
        else:
            print "RESOURCE %s NOT FOUND" % name
        
    def loadSound(self, filename):
        from mixer import Mixer
        print "LOADING: " + filename
        sound = Mixer().loadAudioFile(filename)
        return sound
    
    def loadMusic(self, filename):
        from mixer import Mixer
        print "LOADING: " + filename
        sound = Mixer().loadAudioStream(filename)
        return sound

    def loadData(self, filename="pyzzlix.dat"):
        if not os.path.isfile(filename):
            return None

        fp = open(filename, "r")

        string = fp.read()
        
        if string:
            self.data = json.loads(string)

        fp.close()

    def saveData(self, filename="pyzzlix.dat"):
        fp = open(filename, "w")
        fp.write(json.dumps(self.data))
        fp.close()
        
    def getSound(self, name):
        return self._getResource(name, self.sounds, self.loadSound)

    def getMusic(self, name):
        return self._getResource(name, self.music, self.loadMusic)

    def setData(self, name, value):
        if not self.data:
            self.data = {}

        self.data[name] = value
        
    def getData(self, name):
        if not self.data:
            self.loadData()

        if self.data and name in self.data:
            return self.data[name]

        return None
        
    def preload(self):
        weight = 0.0
        
        def check_resource(name, resource):
            if name in resource:
                if not "obj" in resource[name]:
                    loaded = False
                else:
                    loaded = True
                    
                if "weight" in resource[name]:
                    weight = resource[name]["weight"]
                else:
                    weight = 1

            return {"loaded": loaded, "weight": weight}

        def check_resources(resources, get_func):
            loaded = True
            weight = 0.0
            
            for name in resources:
                result = check_resource(name, resources)

                if not result["loaded"]:
                    loaded = False
                    get_func(name)
                    result = check_resource(name, resources)

            return {"loaded": loaded, "weight": weight}

        result = check_resources(self.sounds, self.getSound)
        weight += result["weight"]
        
        if not result["loaded"]:
            return float(weight) / float(self.numResources)

        result = check_resources(self.music, self.getMusic)
        weight += result["weight"]
        
        if not result["loaded"]:
            return float(weight) / float(self.numResources)

        return 2.0
