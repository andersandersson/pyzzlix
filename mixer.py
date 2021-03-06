import swmixer_pymedia as swmixer

from globals import *
from singleton import *
from options import *

# Dictionary with all sounds
sounds = dict()
streams = dict()

class Sound():
    def __init__(self, sound):
        self.channel = None
        self.stream = False
        self.sound = sound

class Mixer(Singleton):
    def _runOnce(self):
        self.samplerate = 44100
        
    def _timeToSamples(self, time):
        return int((self.samplerate + 0.0) * time)
        
    def init(self, enableSound = True):
        self.enableSound = enableSound

        if not self.enableSound:
            return

        swmixer.init(self.samplerate, chunksize=512, stereo=True)
        swmixer.start()
      
    def loadAudioFile(self, filename):
        if not self.enableSound:
            return None

        sound = 0
        try: 
            sound = sounds[filename]
        except:            
            fullname = os.path.join('data', filename)
            
            sound = Sound(swmixer.Sound(fullname))
            sounds[filename] = sound 
        return sound
        
    def loadAudioStream(self, filename):
        if not self.enableSound:
            return None

        sound = 0
        try: 
            sound = streams[filename]
        except:            
            fullname = os.path.join('data', filename)
            sound = Sound(swmixer.StreamingSound(fullname))
            sound.stream = True
            streams[filename] = sound 
        return sound   
                 

    def _play(self, sound, volume, fadein, loops):
        if not self.enableSound:
            return
        
        if (sound == None):
            return
        if (volume > 1.0):
            volume = 1.0 
        if (sound.channel != None):
            if (sound.channel.get_position() < sound.sound.get_length()):
                sound.channel.set_position(0)
            else:    
                sound.channel = sound.sound.play(volume=volume, fadein=self._timeToSamples(fadein), loops=loops)
        else:
            sound.channel = sound.sound.play(volume=volume, fadein=self._timeToSamples(fadein), loops=loops)
        pass

    def _stop(self, sound):
        if not self.enableSound:
            return

        if (sound == None):
            return
        if (sound.channel != None):
            sound.channel.stop()
            sound.channel = None
        
    def _setVolume(self, sound, volume, fadein=0.0):  
        if not self.enableSound:
            return

        if (sound == None):
            return
        if (volume > 1.0):
            volume = 1.0
        if (sound.channel != None):
            sound.channel.set_volume(volume, fadetime=self._timeToSamples(fadein))

    def playMusic(self, sound, volume=1.0, fadein=0.01, loops=0):
        master_volume = Options().get("music_volume")
        master_volume = float(master_volume) / float(VOLUME_STEPS)        
        
        self._play(sound, volume*master_volume, fadein, loops)
        
    def playSound(self, sound, volume=1.0, fadein=0.01, loops=0):
        master_volume = Options().get("sound_volume")
        master_volume = float(master_volume) / float(VOLUME_STEPS)        
        
        self._play(sound, volume*master_volume, fadein, loops)
            

    def setMusicVolume(self, sound, volume, fadein=0.0):  
        master_volume = Options().get("music_volume")
        master_volume = float(master_volume) / float(VOLUME_STEPS)        

        self._setVolume(sound, volume*master_volume, fadein)
        
    def setSoundVolume(self, sound, volume, fadein=0.0):  
        master_volume = Options().get("sound_volume")
        master_volume = float(master_volume) / float(VOLUME_STEPS)        

        self._setVolume(sound, volume*master_volume, fadein)

    def stopMusic(self, sound):
        self._stop(sound)
        
    def stopSound(self, sound):
        self._stop(sound)
        
    def cleanup(self):
        if not self.enableSound:
            return

        swmixer.quit()
    
