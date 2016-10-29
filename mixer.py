#PyJ2D - Copyright (C) 2011 James Garnon <http://gatc.ca/>
#Released under the MIT License <http://opensource.org/licenses/MIT>

from __future__ import division
from javax.sound.sampled import AudioSystem, AudioFormat
from javax.sound.sampled import LineUnavailableException
from java.io import File, IOException
from java.lang import Thread, Runnable, InterruptedException, IllegalArgumentException
import jarray
from pyj2d import env
try:
    from pyj2d import Mixer as AudioMixer
except ImportError:
    AudioMixer = None

__docformat__ = 'restructuredtext'


class Mixer(Runnable):
    """
    **pyj2d.mixer**
    
    * pyj2d.mixer.init
    * pyj2d.mixer.quit
    * pyj2d.mixer.get_init
    * pyj2d.mixer.stop
    * pyj2d.mixer.pause
    * pyj2d.mixer.unpause
    * pyj2d.mixer.set_num_channels
    * pyj2d.mixer.get_num_channels
    * pyj2d.mixer.set_reserved
    * pyj2d.mixer.find_channel
    * pyj2d.mixer.get_busy
    * pyj2d.mixer.Sound
    * pyj2d.mixer.Channel
    """

    def __init__(self):
        self._mixer = None
        Sound._mixer = self
        Channel._mixer = self
        self.Sound = Sound
        self.Channel = Channel
        self._channel_max = 8
        self._channels = {}
        self._sounds = {}
        self._channel_reserved = []
        self._channel_paused = []
        self._channel_reserves = [id for id in range(self._channel_max-1,-1,-1)]
        self._channel_pool = []
        self._lines = {}
        self._line_num = 0
        self._thread = None
        self._initialized = False
        self._nonimplemented_methods()

    def init(self, frequency=22050, size=-16, channels=2, buffer=4096):
        """
        Mixer initialization.
        Argument sampled frequency, bit size, channels, and buffer.
        Currently implements PCM 16-bit audio.
        Plays WAV, AIFF, and AU sampled audio.
        To specify the BigEndian format of AIFF and AU, use -16L for size.
        The mixing is done by Mixer.class, compiled with 'javac Mixer.java'.
        When a JAR is created, include with 'jar uvf Pyj2d_App.jar pyj2d/Mixer.class'.
        """
        if not self._initialized:
            encoding = {True:AudioFormat.Encoding.PCM_SIGNED, False:AudioFormat.Encoding.PCM_UNSIGNED}[size<0]
            channels = {True:1, False:2}[channels<=1]
            framesize = int((abs(size)/8) * channels)
            isBigEndian = isinstance(size,long)
            self._audio_format = AudioFormat(encoding, int(frequency), int(abs(size)), channels, framesize, int(frequency), isBigEndian)
            self._bufferSize = buffer
            try:
                self._mixer = AudioMixer(self._audio_format, self._bufferSize)
            except TypeError:
                self._mixer = None
                return None
            if not self._mixer.isInitialized():
                return None
            self._bufferSize = self._mixer.getBufferSize()
            self._byteArray = jarray.zeros(self._bufferSize, 'b')
            self._initialized = True
            self._thread = Thread(self)
            self._thread.start()
        return None

    def pre_init(self, frequency=22050, size=-16, channels=2, buffer=4096):
        """
        Mixer initialization.
        """
        self.init(frequency, size, channels, buffer)
        return None

    def quit(self):
        """
        Stop mixer processing and release resources.
        """
        self._initialized = False

    def _quit(self):
        self.stop()
        try:
            self._mixer.quit()
        except AttributeError:
            pass
        self._mixer = None

    def get_init(self):
        """
        Get the audio format initialized.
        """
        if self._initialized:
            frequency = int(self._audio_format.sampleRate)
            format = self._audio_format.sampleSizeInBits * {True:1,False:-1}[self._audio_format.bigEndian]
            channels = self._audio_format.channels
            return (frequency, format, channels)
        else:
            return None

    def stop(self):
        """
        Stop mixer channels.
        """
        for id in self._channel_pool:
            self._channels[id].stop()
        return None

    def pause(self):
        """
        Pause mixer channels.
        """
        for id in self._channel_pool:
            try:
                if self._channels[id]._active:
                    self._channel_paused.append(id)
                    self._channels[id].pause()
            except AttributeError:
                continue
        return None

    def unpause(self):
        """
        Unpause mixer channels.
        """
        for id in self._channel_paused:
            self._channels[id].unpause()
        self.channel_paused = []
        return None

    def set_num_channels(self, count):
        """
        Set maximum mixer channels.
        Argument channel count.
        """
        if count >= self._channel_max:
            for id in range(self._channel_max, count):
                self._channels[id] = None
            self._channel_max = count
        elif count >= 0:
                for id in range(count, self._channel_max):
                    self._channels[id].stop()
                    del self._channels[id]
                self._channel_max = count
        return None

    def get_num_channels(self):
        """
        Get maximum mixer channels.
        """
        return self._channel_max

    def set_reserved(self, count):
        """
        Reserve channel.
        Argument reserved channel count.
        """
        if count > self._channel_max:
            count = self._channel_max
        reserved_len = len(self._channel_reserved)
        if reserved_len:
            if reserved_len >= count:
                for i in range(reserved_len-count):
                    id = self._channel_reserved.pop()
                    self._channels[id]._reserved = False
                    self._channel_pool.append(id)
                count = 0
            else:
                count -= len(self._channel_reserved)
        for id in range(reserved_len, count+reserved_len):
            try:
                self._channels[id]._reserved = True
            except AttributeError:
                self._channels[id] = Channel(id)
            try:
                self._channel_pool.remove(id)
            except ValueError:
                pass
            self._channel_reserved.append(id)
        return None

    def find_channel(self, force=False):
        """
        Get an inactive mixer channel.
        Optional force attribute return longest running channel if all active.
        """
        try:
            channel = self._channel_reserves.pop()
            try:
                return self._channels[channel]
            except KeyError:
                channel = Channel(channel)
                return channel
        except IndexError:
            for id in self._channel_pool:
                if not self._channels[id]._active:
                    return self._channels[id]
            else:
                if force:
                    channel = None
                    longest = 0
                    for id in self._channel_pool:
                        try:
                            duration = self._channels[id]._stream.getMicrosecondPosition()
                            if duration > longest:
                                longest = duration
                                channel = self._channels[id]
                        except AttributeError:
                            channel = self._channels[id]
                            break
                    try:
                        channel.stop()
                        return channel
                    except AttributeError:
                        return None
                else:
                    return None

    def get_busy(self):
        """
        Check if mixer channels are actively processing.
        """
        for id in self._channel_pool:
            try:
                if self._channels[id]._active:
                    return True
            except AttributeError:
                continue
        return False

    def run(self):
        while self._initialized:
            channel_active = [self._channels[id] for id in self._channel_pool if self._channels[id]._active]
            if not channel_active:
                try:
                    self._thread.sleep(1)
                except InterruptedException:
                    Thread.currentThread().interrupt()
                    self.quit()
                continue
            if len(channel_active) > 1:
                for channel in channel_active:
                    try:
                        data, data_len, lvol, rvol = channel._get()
                    except AttributeError:
                        continue
                    self._mixer.setAudioData(data, data_len, lvol, rvol)
                data_len = self._mixer.getAudioData(self._byteArray)
                if data_len > 0:
                    try:
                        self._mixer.write(self._byteArray, 0, data_len)
                    except IllegalArgumentException:
                        nonIntegralByte = data_len % self._audio_format.getFrameSize()
                        if nonIntegralByte:
                            data_len -= nonIntegralByte
                            try:
                                self._mixer.write(self._byteArray, 0, data_len)
                            except (IllegalArgumentException, LineUnavailableException):
                                pass
                    except LineUnavailableException:
                        pass
            else:
                try:
                    data, data_len, lvol, rvol = channel_active[0]._get()
                except AttributeError:
                    data_len = 0
                if data_len > 0:
                    if lvol < 1.0 or rvol < 1.0:
                        data = self._mixer.processVolume(data, data_len, lvol, rvol)
                    try:
                        self._mixer.write(data, 0, data_len)
                    except IllegalArgumentException:
                        nonIntegralByte = data_len % self._audio_format.getFrameSize()
                        if nonIntegralByte:
                            data_len -= nonIntegralByte
                            try:
                                self._mixer.write(data, 0, data_len)
                            except (IllegalArgumentException, LineUnavailableException):
                                pass
                    except LineUnavailableException:
                        pass
        self._quit()

    def _register_channel(self, channel):
        id = channel._id
        if id < self._channel_max:
            try:
                if self._channels[id]._sound:
                    channel._sound = self._channels[id]._sound
                    channel._stream = self._channels[id]._stream
                    self._channels[id] = channel
            except KeyError:
                self._channels[id] = channel
                self._channel_pool.append(id)
        else:
            raise AttributeError("Channel not available.")

    def _register_sound(self, sound):
        self._sounds[sound._id] = sound

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.fadeout = lambda *arg: None


class Sound:
    """
    **pyj2d.mixer.Sound**
    
    * Sound.play
    * Sound.stop
    * Sound.set_volume
    * Sound.get_volume
    * Sound.get_num_channels
    * Sound.get_length
    """

    _id = 0
    _mixer = None

    def __init__(self, sound_file):
        self._id = Sound._id
        Sound._id += 1
        if isinstance(sound_file, str):
            try:
                self._sound_object = env.japplet.getClass().getResource(sound_file.replace('\\','/'))    #java uses /, not os.path Windows \
                if not self._sound_object:
                    raise IOError
            except:
                self._sound_object = File(sound_file)      #make path os independent
        else:
            self._sound_object = sound_file
        self._channel = None
        self._volume = 1.0
        self._mixer._register_sound(self)
        self._nonimplemented_methods()

    def play(self, loops=0, maxtime=0, fade_ms=0):
        """
        Play sound on mixer channel.
        Argument loops is number of repeats or -1 for continuous.
        """
        self._channel = self._mixer.find_channel()
        try:
            self._channel._set_sound(self)
        except AttributeError:
            pass
        try:
            if not loops:
                self._channel._play()
            else:
                self._channel._play_repeat(loops)
        except AttributeError:
            pass
        return self._channel

    def stop(self):
        """
        Stop sound on mixer channel.
        """
        try:
            self._channel.stop()
        except AttributeError:
            pass

    def set_volume(self, volume):
        """
        Set sound volume.
        Argument volume of value 0.0 to 1.0.
        """
        if volume < 0.0:
            volume = 0.0
        elif volume > 1.0:
            volume = 1.0
        self._volume = volume
        return None

    def get_volume(self):
        """
        Get sound volume.
        """
        return self._volume

    def get_num_channels(self):
        """
        Get number of channels sound is active.
        """
        channel = 0
        for id in self._mixer._channel_pool:
            try:
                if self._mixer._channels[id]._sound._id == self._id:
                    channel += 1
            except AttributeError:
                continue
        return channel

    def get_length(self):
        """
        Get length of sound sample.
        """
        stream = AudioSystem.getAudioInputStream(self._sound_object)
        length = stream.getFrameLength() / stream.getFormat().getFrameRate()
        stream.close()
        return length

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.fadeout = lambda *arg: None
        self.get_buffer = lambda *arg: None


class Channel(Runnable):
    """
    **pyj2d.mixer.Channel**
    
    * Channel.play
    * Channel.stop
    * Channel.pause
    * Channel.unpause
    * Channel.set_volume
    * Channel.get_volume
    * Channel.get_busy
    * Channel.get_sound
    """

    _mixer = None

    def __init__(self, id):
        self._id = id
        self._sound = None
        self._stream = None
        self._data = jarray.zeros(self._mixer._bufferSize, 'b')
        self._data_len = 0
        self._active = False
        self._pause = False
        self._loops = 0
        self._volume = 1.0
        self._lvolume = 1.0
        self._rvolume = 1.0
        self._mixer._register_channel(self)
        self._nonimplemented_methods()
        self._thread = Thread(self)
        self._thread.start()

    def _set_sound(self, sound):
        self._sound = sound
        self._stream = AudioSystem.getAudioInputStream(sound._sound_object)

    def run(self):
        return

    def _get(self):
        try:
            self._data_len = self._stream.read(self._data)
        except IOException:
            self._data_len = 0
        if self._data_len > 0:
            return (self._data, self._data_len, self._lvolume*self._sound._volume, self._rvolume*self._sound._volume)
        else:
            if not self._loops:
                self.stop()
            else:
                self._stream.close()
                self._set_sound(self._sound)
                if self._loops != -1:
                    self._loops -= 1
            return (self._data, self._data_len, 1.0, 1.0)

    def _play(self):
        self._volume = 1.0
        self._lvolume = 1.0
        self._rvolume = 1.0
        self._active = True

    def _play_repeat(self, loops):
        if loops > 0:
            self._loops = loops
        else:
            self._loops = -1
        self._play()

    def play(self, sound, loops=0, maxtime=0, fade_ms=0):
        """
        Play sound on channel.
        Argument sound to play and loops is number of repeats or -1 for continuous.
        """
        if self._sound:
            self.stop()
        self._set_sound(sound)
        if not loops:
            self._play()
        else:
            self._play_repeat(loops)
        return None

    def stop(self):
        """
        Stop sound on channel.
        """
        try:
            self._stream.close()
            self._stream = None
        except AttributeError:
            pass
        self._sound = None
        self._pause = False
        self._loops = 0
        self._active = False
        return None

    def pause(self):
        """
        Pause sound on channel.
        """
        if self._active:
            self._active = False
            self._pause = True
        return None

    def unpause(self):
        """
        Unpause sound on channel.
        """
        if self._pause:
            if self._stream:
                self._active = True
                self._pause = False
        return None

    def set_volume(self, volume, volume2=None):
        """
        Set channel volume of sound playing.
        Argument volume of value 0.0 to 1.0, setting for both speakers when single, stereo l/r speakers with second value.
        """
        if volume < 0.0:
            volume = 0.0
        elif volume > 1.0:
            volume = 1.0
        self._lvolume = volume
        if volume2:
            if volume2 < 0.0:
                volume2 = 0.0
            elif volume2 > 1.0:
                volume2 = 1.0
            self._rvolume = volume2
        else:
            self._rvolume = self._lvolume
            self._volume = volume
        return None

    def get_volume(self):
        """
        Get channel volume for current sound.
        """
        return self._volume

    def get_busy(self):
        """
        Check if channel is processing sound.
        """
        return self._active

    def get_sound(self):
        """
        Get sound open by channel.
        """
        return self._sound

    def _nonimplemented_methods(self):
        """
        Non-implemented methods.
        """
        self.fadeout = lambda *arg: None
        self.queue = lambda *arg: None
        self.get_queue = lambda *arg: None
        self.set_endevent = lambda *arg: None
        self.get_endevent = lambda *arg: 0

