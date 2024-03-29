import numpy as np
import scipy
import tomli
import matplotlib.pyplot as plt
import sys

# sys.path.append("..")
# sys.path.append("./")
from heronsim.audioHelper import AudioObject, read_wav


class Source:
    position = None
    sr = None
    name = None
    # speed of sound in m/s
    _speed_sound = None

    def __init__(
            self, position=None, name="Default", audio_file=None, speed_sound=333, sr=44100, frequency=222, lenght=10, gain=1
    ):
        if position is None:
            position = np.zeros(3)
        self.position = np.asarray(position)
        self._speed_sound = speed_sound
        self.sr = sr
        self.name = name
        if audio_file is None:
            x = np.linspace(0, lenght, sr * length)
            self._sound = np.sin(2 * np.pi * frequency * x)
            return
        audio = read_wav(audio_file)
        self.sr = audio.sr
        self._sound = audio.audio * gain

    @classmethod
    def fromposition(cls, position):
        return cls(position=position)

    def add_sound(self, sound_arr):
        self._sound = sound_arr
        pass

    def _shift(self, arr, num, fill_value=np.nan):
        result = np.empty_like(arr)
        if num > 0:
            result[:num] = fill_value
            result[num:] = arr[:-num]
        elif num < 0:
            result[num:] = fill_value
            result[:num] = arr[-num:]
        else:
            result[:] = arr
        return result

    def get_sound_at_position(self, position):
        print(f"calculate sound at Position {position}")
        diff_vector = self.position - position
        distance = np.linalg.norm(diff_vector)
        normal_vec = diff_vector / distance
        delay = distance / self._speed_sound
        samples_df = delay * self.sr
        samples_d = int(np.round(samples_df))
        sub_s_delay = samples_df - samples_d

        f_len = 45
        f_len_half = (f_len - 1) // 2
        x = np.linspace(-f_len_half, f_len_half, f_len)
        delay_filter = np.sinc(x - sub_s_delay)
        delay_filter = delay_filter * scipy.signal.windows.hamming(f_len)
        filtered = scipy.signal.lfilter(delay_filter, 1, self._sound)
        filtered = filtered[f_len_half:]
        sound_at_pos = self._shift(filtered, samples_d, 0)
        sound_at_pos /= distance
        return sound_at_pos, normal_vec, delay

    def get_sound_from_mirror_pos(self, position, damp_f=0.1):
        sound_at_pos, *_ = self.get_sound_at_position(position)
        sound_at_pos *= damp_f
        return sound_at_pos


if __name__ == "__main__":
    x = np.linspace(-22050, 22049, 44100)
    print(x[0:10])
    print(x[-10:])
    y = np.sinc(x - 0.5)
    source = Source()
    source.add_sound(np.sin(x / 44100 * 3000))
    sound1, _ = source.get_sound_at_position(np.ones(3) * 0.1)
    sound2, _ = source.get_sound_at_position(np.ones(3) * 0.2)
    fig, ax = plt.subplots(3, sharex="all")
    ax[0].plot(np.sin(x / 44100 * 3000))
    ax[1].plot(sound1)
    ax[2].plot(sound2)
    plt.show()
    hansi = scipy.signal.correlate(sound1[1000:1200], sound2[1000:1200])
    lags = scipy.signal.correlation_lags(200, 200)
    fig, ax = plt.subplots(2)
    ax[0].plot(lags, hansi)
    ax[1].plot(lags, np.abs(hansi))
    plt.show()
