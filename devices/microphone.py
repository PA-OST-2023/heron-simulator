import numpy as np
from devices.source import Source

class Microphone():

    _source = None
    _position = np.zeros((1,3))
    _normal = np.array([1,0,0])
    _characteristic = np.ones(360)

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

    def simulate_mic(self, sounds, normals):
        print(1)
        for sound, normal in zip(sounds, normals):
            pass
        return np.sum(sounds, axis=0)
        pass

    def test(self):
        print('Mic Test')

