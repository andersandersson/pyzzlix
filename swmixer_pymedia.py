"""Advanced Realtime Software Mixer

This module implements an advanced realtime sound mixer suitable for
use in games or other audio applications.  It supports loading sounds
in uncompressed WAV format.  It can mix several sounds together during
playback.  The volume and position of each sound can be finely
controlled.  The mixer can use a separate thread so clients never block
during operations.  Samples can also be looped any number of times.
Looping is accurate down to a single sample, so well designed loops
will play seamlessly.  Also supports sound recording during playback.

Copyright 2008, Nathan Whitehead
Released under the LGPL

"""

"""
    Severely changed by joel lennartsson, 2010
"""

import time
import wave
import thread

import numpy
import pyaudio

import pymedia.muxer as muxer, pymedia.audio.acodec as acodec, pymedia.audio.sound as sound

import sys

try:
    import mad
except:
    "MP3 streaming disabled"

ginit = False
gstereo = True
gchunksize = 1024
gsamplerate = 44100
gchannels = 1
gsamplewidth = 2
gpyaudio = None
gstream = None
gmicstream = None
gmic = False
gmicdata = None
gmixer_srcs = []
gid = 1
glock = thread.allocate_lock()
ginput_device_index = None
goutput_device_index = None

class _SoundSourceData:
    def __init__(self, data, loops):
        self.data = data
        self.pos = 0
        self.loops = loops
        self.done = False
    def set_position(self, pos):
        self.pos = pos % len(self.data)
    def get_samples(self, sz):
        z = self.data[self.pos:self.pos + sz]
        self.pos += sz
        if len(z) < sz:
            # oops, sample data didn't cover buffer
            if self.loops != 0:
                # loop around
                self.loops -= 1
                self.pos = sz - len(z)
                z = numpy.append(z, self.data[:sz - len(z)])
            else:
                # nothing to loop, just append zeroes
                z = numpy.append(z, numpy.zeros(sz - len(z), numpy.int16))
                # and stop the sample, it's done
                self.done = True
        if self.pos == len(self.data):
            # this case loops without needing any appending
            if self.loops != 0:
                self.loops -= 1
                self.pos = 0
            else:
                self.done = True
                
        return z

class _SoundSourceStream:
    def __init__(self, fileobj, loops):
        self.fileobj = fileobj
        self.pos = 0
        self.loops = loops
        self.done = False
        self.buf = ''
    def set_position(self, pos):
        self.pos = pos
        self.fileobj.seek_time(pos * 1000 / gsamplerate / 2)
    def get_samples(self, sz):
        szb = sz * 2 # for 16 bit

        while len(self.buf) < szb:
            s = self.fileobj.read()
            # If buffer ends before chunk is filled then
            # restart the buffer if loops is > 0
            if s is None or s == '':
                if self.loops != 0:
                    sys.stdout.flush()
                 
                    self.loops -= 1
                    self.pos = (len(self.buf) - szb) / 2 # Place pos "before" start
                    self.fileobj.seek_time(0)
                else:
                    self.done = True
                    break
            else:
                self.buf += s[:]

        z = numpy.fromstring(self.buf[:szb], dtype=numpy.int16)
        self.pos += sz       
        if (self.done):
            # In this case we ran out of stream data, and don't want to loop,
            # append zeros
            z = numpy.append(z, numpy.zeros(sz - len(z), numpy.int16))
        else:
            # remove head of buffer
            self.buf = self.buf[szb:]
            
        return z

# A channel is a "sound event" that is playing
class Channel:
    """Represents one sound source currently playing"""
    def __init__(self, src, env, vol):
        global gid
        self.id = gid
        gid += 1
        self.src = src
        self.env = env
        self.vol = vol
        self.active = True
        self.done = False
    def stop(self):
        """Stop the sound playing"""
        glock.acquire()
        # If the sound has already ended, don't raise exception
        try:
            gmixer_srcs.remove(self)
        except ValueError:
            None
        glock.release()
    def pause(self):
        """Pause the sound temporarily"""
        glock.acquire()
        self.active = False
        glock.release()
    def unpause(self):
        """Unpause a previously paused sound"""
        glock.acquire()
        self.active = True
        glock.release()
    def set_volume(self, volume, fadetime=0):
        """Set the volume of the sound

        Overrides any pending fadeins or fadeouts. Does not interfere with envelope.

        """
        glock.acquire()
        if fadetime == 0:
            self.vol = [[0, volume]]
        else:
            curv = calc_vol(self.src.pos, self.vol)
            self.vol = [[self.src.pos, curv], [self.src.pos + fadetime, volume]]
        glock.release()
    def get_volume(self):
        """Return current volume of sound"""
        glock.acquire()
        v = calc_vol(self.src.pos, self.env)
        glock.release()
        return v
    def get_position(self):
        """Return current position of sound in samples"""
        glock.acquire()
        p = self.src.pos
        glock.release()
        return p
    def set_position(self, p):
        """Set current position of sound in samples"""
        # reset any master volume information
        v = calc_vol(self.src.pos, self.vol)
        self.vol = [[0, v]]
        glock.acquire()
        self.src.set_position(p)
        glock.release()
    def fadeout(self, time):
        """Schedule a fadeout of this sound in given time"""
        glock.acquire()
        self.set_volume(0.0, fadetime=time)
        glock.release()
    def _get_samples(self, sz):
        if not self.active: return None
        oldpos = self.src.pos

        e = calc_vol(self.src.pos, self.env)
        v = calc_vol(self.src.pos, self.vol)
        z = self.src.get_samples(sz) 

        if self.src.done: 
            self.done = True
        elif oldpos > self.src.pos:
            # If sound has looped, reset any master volume information
            self.vol = [[0, v]]

        return z * (e * v)



def resample(smp, scale=1.0):
    """Resample a sound to be a different length

    Sample must be mono.  May take some time for longer sounds
    sampled at 44100 Hz.

    Keyword arguments:
    scale - scale factor for length of sound (2.0 means double length)

    """
    # f*ing cool, numpy can do this with one command
    # calculate new length of sample
    n = round(len(smp) * scale)
    # use linear interpolation
    # endpoint keyword means than linspace doesn't go all the way to 1.0
    # If it did, there are some off-by-one errors
    # e.g. scale=2.0, [1,2,3] should go to [1,1.5,2,2.5,3,3]
    # but with endpoint=True, we get [1,1.4,1.8,2.2,2.6,3]
    # Both are OK, but since resampling will often involve
    # exact ratios (i.e. for 44100 to 22050 or vice versa)
    # using endpoint=False gets less noise in the resampled sound
    return numpy.interp(
        numpy.linspace(0.0, 1.0, n, endpoint=False), # where to interpret
        numpy.linspace(0.0, 1.0, len(smp), endpoint=False), # known positions
        smp, # known data points
        )

def interleave(left, right):
    """Given two separate arrays, return a new interleaved array

    This function is useful for converting separate left/right audio
    streams into one stereo audio stream.  Input arrays and returned
    array are Numpy arrays.

    See also: uninterleave()

    """
    return numpy.ravel(numpy.vstack((left, right)), order='F')

def uninterleave(data):
    """Given a stereo array, return separate left and right streams

    This function converts one array representing interleaved left and
    right audio streams into separate left and right arrays.  The return
    value is a list of length two.  Input array and output arrays are all
    Numpy arrays.

    See also: interleave()

    """
    return data.reshape(2, len(data)/2, order='FORTRAN')

def stereo_to_mono(left, right):
    """Return mono array from left and right sound stream arrays"""
    return (0.5 * left + 0.5 * right).astype(numpy.int16)


class Sound:
    """Represents a playable sound"""

    def __init__(self, filename=None):
        """Create new sound from a WAV file, MP3 file, or explicit sample data"""
        assert(ginit == True)
 
        stream = _open_stream(filename)
            
        self.data = ''
        s = stream.file.read(512)
        while len(s):
            frames= stream.demuxer.parse(s) # Try to parse frames from the stream
            for fr in frames:

                # Decode frame and setup sound device and resampler
                r = stream.decoder.decode(fr[1])
                if (r and r.data): 
                    if stream.resampler:
                        data += stream.resampler.resample(r.data)  
                    else: 
                         self.data += str(r.data)        

            s = stream.file.read(512)
                
        self.data = numpy.fromstring(''.join(self.data ), dtype=numpy.int16)    
        

    def get_length(self):
        """Return the length of the sound in samples

        To convert to seconds, divide by the samplerate and then divide
        by 2 if in stereo.

        """
        return len(self.data)

    def play(self, volume=1.0, offset=0, fadein=0, envelope=None, loops=0):
        """Play the sound

        Keyword arguments:
        volume - volume to play sound at
        offset - sample to start playback
        fadein - number of samples to slowly fade in volume
        envelope - a list of [offset, volume] pairs defining
                   a linear volume envelope
        loops - how many times to play the sound (-1 is infinite)

        """
        if envelope != None:
            env = envelope
        else:
            env = []    
     
        if volume == 1.0 and fadein == 0:
            vol = []
        else:
            if fadein == 0:
                vol = [[0, volume]]
            else:
                vol = [[offset, 0.0], [offset + fadein, volume]]
                       
        src = _SoundSourceData(self.data, loops)
        src.pos = offset
        sndevent = Channel(src, env, vol)
        glock.acquire()
        gmixer_srcs.append(sndevent)
        glock.release()
        return sndevent

    def scale(self, vol):
        """Scale a sound sample

        vol is 0.0 to 1.0, amount to scale by
        """
        self.data = (self.data * vol).astype(numpy.int16)

    def resample(self, scale):
         """Resample a sound

         scale = 1.0 means original sound
         scale = 0.5 is half as long (up an octave)
         scale = 2.0 is twice as long (down an octave)
         
         """
         self.data = resample(self.data, scale)

class _Stream:
    pass

def _open_stream(filename):
    stream = _Stream()
    stream.demuxer = muxer.Demuxer( str.split(filename, '.' )[ -1 ].lower())
    assert (stream.demuxer != 0) # file extension not recognized
    stream.file = open(filename, 'rb')
    s = stream.file.read(32000) # Read abit, should contain at least one frame
    stream.device = None 
    stream.resampler= None
    stream.decoder= None
    stream.samplerate = None
    stream.channels = None
    
    ## Try to find out file info and set up decoder
    while len(s):
        frames= stream.demuxer.parse(s) # Try to parse frames from the stream
        for fr in frames:
        
            # Configure decoder
            if stream.decoder== None:
                stream.decoder= acodec.Decoder(stream.demuxer.streams[fr[0]])
        
            # Decode frame and setup sound device and resampler
            r = stream.decoder.decode(fr[1])
            if (r and r.data): 
                if stream.device== None:
                    #print 'Opening sound with %d channels' % (r.channels)
                    #stream.device = sound.Output(gsamplerate, gchannels, sound.AFMT_S16_LE, 0)
                    if (r.sample_rate != gsamplerate) or (r.channels != gchannels):
                        stream.resampler = sound.Resampler((r.sample_rate, r.channels), (gsamplerate, gchannels))
                        print 'Sound resampling %d->%d' % (r.sample_rate, gsamplerate)
                stream.samplerate = r.sample_rate
                stream.channels = r.channels
    
            # If all info has been loaded, we are done
            if stream.decoder and stream.samplerate and stream.channels:
                break
                
        if stream.decoder and stream.samplerate and stream.channels:
            break    

        s= stream.file.read( 512 )
        
    assert (stream.decoder) # Error loading device/decoder

    print "File", filename, " loaded, with samplerate:", stream.samplerate, "and", stream.channels, "channels"
    
    # Reset stream
    stream.demuxer.reset()
    stream.file.seek(0, 0)
    
    return stream


def _create_stream(filename):
    # create stream object
 
    stream = _open_stream(filename)
 
    def str_read(): 
        data = ''
        while len(data) <= 0:
            s = stream.file.read(512)
            if len(s):
                frames= stream.demuxer.parse(s) # Try to parse frames from the stream
                for fr in frames:

                    # Decode frame and setup sound device and resampler
                    r = stream.decoder.decode(fr[1])
                    if (r and r.data): 
                        if stream.resampler:
                            data += stream.resampler.resample(r.data)  
                        else: 
                            data += str(r.data)        
            else:
                break
                
        return data
        
    def str_seek_time(t):
        if t == 0: 
            stream.file.seek(0, 0)
            #stream.demuxer.reset()
        else:
            assert(False) # unsupported
    
    stream.read = str_read
    stream.seek_time = str_seek_time
    
    return stream
        
    assert(False) # filename must have wav or mp3 extension

class StreamingSound:
    """Represents a playable sound stream"""

    def __init__(self, filename):
        """Create new streaming sound from a WAV file or an MP3 file

        The new streaming sound must match the output samplerate
        and stereo-ness.  You can turn off these checks by setting
        the keyword checks=False, but the sound will be distorted.
        
        """
        assert(ginit == True)
        if filename is None:
            assert False
        self.filename = filename

    def get_length(self):
        """Return the length of the sound stream in samples

        Only available for MP3 streams, not WAV ones.  To convert
        result to seconds, divide by the samplerate and then divide by
        2.

        """
        stream = _create_stream(self.filename, self.checks)
        t = stream.total_time() * gsamplerate * 2 / 1000
        del(stream)
        return t

    def play(self, volume=1.0, offset=0, fadein=0, envelope=None, loops=0):
        """Play the sound stream

        Keyword arguments:
        volume - volume to play sound at
        offset - sample to start playback
        fadein - number of samples to slowly fade in volume
        envelope - a list of [offset, volume] pairs defining
                   a linear volume envelope
        loops - how many times to play the sound (-1 is infinite)

        """
        stream = _create_stream(self.filename)
 
        if envelope != None:
            env = envelope
        else:
            env = []    
     
        if volume == 1.0 and fadein == 0:
            vol = []
        else:
            if fadein == 0:
                vol = [[0, volume]]
            else:
                vol = [[offset, 0.0], [offset + fadein, volume]]
                       
        src = _SoundSourceStream(stream, loops)
        src.pos = offset
        sndevent = Channel(src, env, vol)
        glock.acquire()
        gmixer_srcs.append(sndevent)
        glock.release()
        return sndevent

def calc_vol(t, env):
    """Calculate volume at time t given envelope env

    envelope is a list of [time, volume] points
    time is measured in samples
    envelope should be sorted by time

    """
    #Find location of last envelope point before t
    if len(env) == 0: return 1.0
    if len(env) == 1:
        return env[0][1]
    n = 0
    while n < len(env) and env[n][0] < t:
        n += 1
    if n == 0:
        # in this case first point is already too far
        # envelope hasn't started, just use first volume
        return env[0][1]
    if n == len(env):
        # in this case, all points are before, envelope is over
        # use last volume
        return env[-1][1]
        
    # now n holds point that is later than t
    # n - 1 is point before t
    f = float(t - env[n - 1][0]) / (env[n][0] - env[n - 1][0])
    # f is 0.0--1.0, is how far along line t has moved from
    #  point n - 1 to point n
    # volume is linear interpolation between points
    return env[n - 1][1] * (1.0 - f) + env[n][1] * f

def microphone_on():
    """Turn on microphone

    Schedule audio input during main mixer tick.

    """
    global gstream, gmicstream, gmic
    glock.acquire()
    if gmicstream is not None:
        gmicstream.close()
    if gstream is not None:
        gstream.close()
    gmicstream = gpyaudio.open(
        format = pyaudio.paInt16,
        channels = gchannels,
        rate = gsamplerate,
        input_device_index = ginput_device_index,
        input = True)
    gstream = gpyaudio.open(
        format = pyaudio.paInt16,
        channels = gchannels,
        rate = gsamplerate,
        output_device_index = goutput_device_index,
        output = True)
    gmic = True
    glock.release()

def microphone_off():
    """Turn off microphone"""
    global gstream, gmicstream, gmic
    glock.acquire()
    if gmicstream is not None:
        gmicstream.close()
    if gstream is not None:
        gstream.close()
    gstream = gpyaudio.open(
        format = pyaudio.paInt16,
        channels = gchannels,
        rate = gsamplerate,
        output_device_index = goutput_device_index,
        output = True)
    gmic = False
    glock.release()

def get_microphone():
    """Return raw data from microphone as Numpy array

    Default format will be 16-bit signed mono.  Format will match
    audio playback.  You must call tick() every frame to update the
    results from this function.

    """
    glock.acquire()
    d = gmicdata
    glock.release()
    return numpy.fromstring(gmicdata, dtype=numpy.int16)
    
def tick(extra=None):
    """Main loop of mixer, mix and do audio IO

    Audio sources are mixed by addition and then clipped.  Too many
    loud sources will cause distortion.

    extra is for extra sound data to mix into output
      must be in numpy array of correct length
      
    """

    global ginit
    global gmixer_srcs
    rmlist = []
    if not ginit:
        return
    sz = gchunksize * gchannels
    b = numpy.zeros(sz, numpy.float)
    if glock is None: return # this can happen if main thread quit first

    glock.acquire()
    for sndevt in gmixer_srcs:
        s = sndevt._get_samples(sz)
        
        if s is not None:
            b += s
        if sndevt.done:
            rmlist.append(sndevt)  
    
    if extra is not None:
        b += extra
    b = b.clip(-32767.0, 32767.0)
    for e in rmlist:
        gmixer_srcs.remove(e)
    global gmicdata
    if gmic:
        gmicdata = gmicstream.read(sz)
    glock.release()
    odata = (b.astype(numpy.int16)).tostring()
    
  
    # yield rather than block, pyaudio doesn't release GIL
    while gstream.get_write_available() < gchunksize: 
        time.sleep(0.001)
    gstream.write(odata, gchunksize)
 

def init(samplerate=44100, chunksize=1024, stereo=True, microphone=False, input_device_index=None, output_device_index=None):
    """Initialize mixer

    Must be called before any sounds can be played or loaded.

    Keyword arguments:
    samplerate - samplerate to use for playback (default 22050)
    chunksize - size of playback chunks
      smaller is more responsive but perhaps stutters
      larger is more buffered, less stuttery but less responsive
      Can be any size, does not need to be a power of two. (default 1024)
    stereo - whether to play back in stereo
    microphone - whether to enable microphone recording
    
    """
    global gstereo, gchunksize, gsamplerate, gchannels, gsamplewidth
    global ginit
    assert (10000 < samplerate <= 48000)
    gsamplerate = samplerate
    gchunksize = chunksize
    assert (stereo in [True, False])
    gstereo = stereo
    if stereo:
        gchannels = 2
    else:
        gchannels = 1
    gsamplewidth = 2
    global gpyaudio, gstream
    gpyaudio = pyaudio.PyAudio()
    # It's important to open Input, then Output (not sure why)
    # Other direction gives very annoying sound errors (1/2 rate?)
    global ginput_device_index, goutput_device_index
    ginput_device_index = input_device_index
    goutput_device_index = output_device_index
    if microphone:
        global gmicstream, gmic
        gmicstream = gpyaudio.open(
            format = pyaudio.paInt16,
            channels = gchannels,
            rate = gsamplerate,
            input_device_index = input_device_index,
            input = True)
        gmic = True
    gstream = gpyaudio.open(
        format = pyaudio.paInt16,
        channels = gchannels,
        rate = gsamplerate,
        output_device_index = output_device_index,
        output = True)
    ginit = True

def start():
    """Start separate mixing thread"""
    global gthread
    def f():
        while True:
            tick()
            time.sleep(0.001)
    gthread = thread.start_new_thread(f, ())

def quit():
    """Stop all playback and terminate mixer"""
    global ginit
    glock.acquire()
    ginit = False
    if gstream is not None:
        gstream.close()
    if gmicstream is not None:
        gmicstream.close()
    gpyaudio.terminate()
    glock.release()

def set_chunksize(size=1024):
    """Set the audio chunk size for each frame of audio output

    This function is useful for setting the framerate when audio output
    is synchronized with video.
    """
    global gchunksize
    glock.acquire()
    gchunksize = size
    glock.release()
