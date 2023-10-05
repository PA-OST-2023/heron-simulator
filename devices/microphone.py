import numpy as np
import matplotlib.pyplot as plt
import scipy
import tomli

try:
    from source import Source
except ModuleNotFoundError:
    pass


class Microphone:
    _source = None
    position = None
    _normal = None
    _noisefloor = 40
    _SNR = 100
    _samplingrate = 44100
    _amplitude_offset = 0

    def __init__(self, config=None, position=None, normal=None):
        if position is None:
            position = np.zeros(3)
        if normal is None:
            normal = np.array([1, 0, 0])
        self.position = position
        self._normal = normal
        if config is None:
            return
        with open(config, "rb") as f:
            m_conf = tomli.load(f)
        characterisitcs = m_conf.get("characterisitcs", {})
        self._SNR = characterisitcs.get("SNR", self._SNR)
        self._noisefloor = characterisitcs.get("noisefloor", self._noisefloor)
        self._samplingrate = characterisitcs.get("samplingrate", self._samplingrate)
        self._amplitude_offset = characterisitcs.get(
            "amplitude_offset", self._amplitude_offset
        )

    @classmethod
    def fromposition(cls, position):
        return cls(position=position)

    def set_source(self, source):
        self._source = source

    def simulate_mic(self, sounds, normals):
        print(1)
        noise_scale = 10 ** ((self._noisefloor - 120) / 20)
        noise = np.random.normal(0, noise_scale, sounds[0].shape[0])
        for sound, normal in zip(sounds, normals):
            sound *= 10 ** (self._amplitude_offset / 20)
        return np.sum(sounds, axis=0) + noise


if __name__ == "__main__":
    print(1)
    xx = np.linspace(0, 3, 44100 * 3)
    sigi = (
        np.sin(50 * xx)
        + np.cos(25 * xx)
        + np.sin(12.5 * xx + 2)
        + np.cos(6.25 * xx + 0.7)
    )
    fig, ax = plt.subplots()
    ax.plot(xx, sigi)
    plt.show()
    source = Source()
    source.add_sound(sigi)
    mic = Microphone.fromposition(np.ones(3))
    sisgi_at_mic, hansi = source.get_sound_atposition(mic.position)
    micsound = mic.simulate_mic([sisgi_at_mic], [hansi])
    fig, ax = plt.subplots(3)
    ax[0].plot(xx, sigi)
    ax[1].plot(xx[:-22], sisgi_at_mic)
    ax[2].plot(xx[:-22], micsound)
    plt.show()
