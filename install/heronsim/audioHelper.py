import scipy
import numpy as np


class AudioObject:
    def __init__(self, audio, sr):
        self.audio = audio
        self.sr = sr


def read_wav(filename):
    sr, data = scipy.io.wavfile.read(filename)
    if data.dtype == np.int32:
        data = data / (2**31 - 1)
    return AudioObject(data, sr)


def write_wav(data, sr, filename):
    scipy.io.wavfile.write(filename, sr, data)
