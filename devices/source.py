import numpy as np

class Source():

    _position = np.zeros((1,3))
    def __init__(self, config):
        self._position = np.zeros((1,3))
        pass

    def __init__(self):
        pass

    def add_sound(self, sound_arr):
        pass

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def test(self):
        print('source Test')

    def get_sound_at_position(self, position):
        distance = np.linalg.norm(self._position - position)
        print(distance)
        pass

