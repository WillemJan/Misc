# -*- coding: utf-8 -*-
"""
    The basic alsa functionality, using :class: `~python-alsa`.

    Implements a command line tool named noise,
    sets all mix channels to max volume.

    Implements a command line tool named mute,
    sets all mix channels to min volume.

    :class:`~Fe2.tools.alsa`
"""
import alsaaudio
import optparse
import os
import threading

from sqlalchemy.engine import create_engine

import Fe2.tools.log


log = Fe2.tools.log.create_logger(__name__)

class Mixer():
    """
        Implements simple mixer wrapper for alsa.
        Sets all channels to requested volume.

        :param volume: Volume to set mixers to.

        >>> mixer = Fe2.tools.alsa.Mixer()
        >>> mixer.setvolume(100)
        >>> mixer.getvolume()
        100
    """
    def __init__(self, volume=100):
        """
            Set volume of all channels to given volume.

            :param volume: Set all channes to given volume.
        """
        self.volume = volume
        self._reset()

    @staticmethod
    def _test_alsamixer(channel="PCM"):
        """
            Test alsamixer with the given mix chanel.

            >>> (left, right) = test_alsamixer()
            >>> print(left >0 <100)
            True
        """
        mixer = alsaaudio.Mixer(chanel)
        return(mixer.getvolume())

    def _reset(self):
        self.setvolume(self.volume)

    def setvolume(self, volume=100):
        """
            Set volume for all channels to same level.

            :param volume: Set the volume for all channels.
        """
        try:
            channel_list = alsaaudio.mixers()
        except:
            log.warn("Error, no sound device present")
            return(-1)
        mixers = []
        self.volume = int(volume)
        for channel in channel_list:
            channel = SetVolume(channel, volume)
            channel.start()  # Starting the mixer thread.
            mixers.append(channel)
        for channel in mixers:
            channel.join()  # Waiting for all mixers to end.


class SetVolume(threading.Thread):
    """
        Wrapper to set all the mix channels parallel.
        This wrapper actually makes the call and waits.

        :param channel: Channel to use.
        :param volume: Volume to set to.
    """
    def __init__(self, channel, volume):
        threading.Thread.__init__(self)
        self.channel = channel
        self.volume = volume

    def run(self):
        mixer = alsaaudio.Mixer(self.channel)
        log.info("Setting %s to %s" % (self.channel, str(self.volume)))
        for i in range(2):
            try:
                mixer.setvolume(self.volume, i)
            except:
                pass


def mute():
    """
        mute: A program to mute all mix channels.
    """
    mixer = Mixer(0)


def noise():
    """
        noise: A program to make a lot of noise.
    """
    mixer = Mixer()
