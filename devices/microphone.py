import numpy as np
from devices.source import Source


class Microphone:
    _source = None
    _position = np.zeros((3))
    _normal = np.array([-1, 0, 0])
    _characteristic = np.ones(360)
    _noisefloor = 0
    _SNR = 100
    _samplingrate = 44100
    _amplitude_offset = 0

    def __init__(self, config, position, normal):
        with open(config, "rb") as f:
            m_conf = tomli.load(f)
        characterisitcs = m_conf.get("characterisitcs", {})
        self._SNR = characterisitcs.get("SNR", self._SNR)
        self._noisefloor = characterisitcs.get("noisefloor", self._noisefloor)
        self._samplingrate = characterisitcs.get("samplingrate", self._samplingrate)
        self._amplitude_offset = characterisitcs.get(
            "amplitude_offset", self._amplitude_offset
        )
        pass

    def __init__(self, position):
        self.__position = position

    def __init__(self, config):
        pass

    def __init__(self):
        print("ok Python")

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
            angle = np.arccos(np.clip(np.dot(self._normal, normal), -1.0, 1.0))
            print(f"{angle = }")
            characteristic = self._get_characteristic_at_angle(angle)
        return np.sum(sounds, axis=0)

    def test(self):
        print("Mic Test")

    def _get_characteristic_at_angle(self, angle):
        angle = int(angle / (2 * pi) * 180)
        return self._characteristic[angle + 180]

