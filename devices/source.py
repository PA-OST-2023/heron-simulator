import numpy as np

class Source():

    _position = np.zeros((1,3))
    _sr = 8 * 44100
    # speed of sound in m/s
    _speed_sound = 333
    _sound = np.random.normal(0, 1, 44100)

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
        diff_vector = self._position - position
        distance = np.linalg.norm(diff_vector)
        normal_vec = diff_vector / distance
        print(distance)
        delay = distance / self._speed_sound
        samples_d = int(delay * self._sr)
        print(samples_d)
        sound_at_pos = np.r_[np.zeros(samples_d), self._sound[samples_d:]]
        print(sound_at_pos)
        print(sound_at_pos.shape)
        return sound_at_pos, normal_vec

