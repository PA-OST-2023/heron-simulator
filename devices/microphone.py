import numpy as np
from devices.source import Source

class Microphone():

    _source = None
    _position = np.zeros((1,3))

    def __init__(self, position):
        self.__position = position

    def __init__(self, config):
        pass

    def __init__(self):
        print('ok Python')

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def set_source(self, source):
        self._source = source

    def simulate(self):
        print(1)
        self._source.get_sound_at_position(self._position)
        pass

    def test(self):
        print('Mic Test')

