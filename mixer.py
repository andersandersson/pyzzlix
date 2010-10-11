
#import pygame
#from pygame.locals import *

import swmixer

from globals import *
from singleton import *

# Dictionary with all sounds
sounds = dict()

class Sound():
    def __init__(self, sound):
        self.channel = None
        self.sound = sound



class Mixer(Singleton):
    def _runOnce(self):
        self.samplerate = 44100
        pass
        
    def _timeToSamples(self, time):
        return int((self.samplerate + 0.0) * time)
        
    def init(self):
        swmixer.init(self.samplerate, chunksize=256, stereo=True)
        swmixer.start()
        pass
      
    def loadAudiofile(self, filename):
        sound = 0
        try: 
            sound = sounds[filename]
        except:            
            fullname = os.path.join('data', filename)
            sound = Sound(swmixer.Sound(fullname))
            sounds[filename] = sound 
        return sound
        
    def loadMusic(self, filename):
        sound = 0
        try: 
            sound = sounds[filename]
        except:            
            fullname = os.path.join('data', filename)
            sound = Sound(swmixer.StreamingSound(fullname, False))
            sounds[filename] = sound 
        return sound   
                 

    def playSound(self, sound):
        if (sound.channel != None):
            if (sound.channel.get_position() < sound.sound.get_length()):
                sound.channel.set_position(0)
            else:    
                sound.channel = sound.sound.play(offset=self._timeToSamples(0.0))
        else:
            sound.channel = sound.sound.play(offset=self._timeToSamples(0.0))
        
    def playMusic(self, music, volume=1.0, fadein=0.01):
        if (volume > 1.0):
            volume = 1.0
        if (music.channel != None):
            if (music.channel.get_position() < music.sound.get_length()):
                music.channel.set_position(0)
            else:    
                music.channel = music.sound.play(volume=volume, fadein=self._timeToSamples(fadein), loops=-1)
        else:
            music.channel = music.sound.play(volume=volume,fadein=self._timeToSamples(fadein), loops=-1)
            
    def setVolume(self, music, volume, fadein=0.0):  
        if (volume > 1.0):
            volume = 1.0
        if (music.channel != None):
            music.channel.set_volume(volume, fadetime=self._timeToSamples(fadein))

    def stopMusic(self, music):
        if (music.channel != None):
            music.channel.stop()
            music.channel = None
        
        
    def stopSound(self, sound):
        if (sound.channel != None):
            sound.channel.stop()
            sound.channel = None
        
    def cleanup(self):
        swmixer.quit()
    