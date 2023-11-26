import numpy as np

from devices.source import Source
from marray import open_array, plot_array
from devices.microphone import Microphone



def static_simulation(mic_array, sources, surfaces=None, plot=False):
    """
    Perform a simulation with static position of the sources
    and microphone array

    [TODO:description]

    Parameters
    ----------
    mic_array : list
        List of Microphones
    sources : list
        List of Source
    """
    mic_signals = []
    signals_info = {}
    for i, mic in enumerate(mic_array):
        sound_at_pos_info = [
            source.get_sound_at_position(mic.position) for source in sources
        ]
        signal_at_position = [info[0] for info in sound_at_pos_info]
        if surfaces is not None:
            mirrors = [mirror_pos(mic.position, surface) for surface in surfaces]
            mirros_sigs = [source.get_sound_from_mirror_pos(pos) for source in sources for pos in mirrors]
            signal_at_position += mirros_sigs
        normal = [info[1] for info in sound_at_pos_info]
        delays = {
            source.name: info[2] for source, info in zip(sources, sound_at_pos_info)
        }
        mic_signal = mic.simulate_mic(signal_at_position, normal)
        mic_signals.append(mic_signal)
        signals_info[mic.name] = delays
    if plot:
        plot_array(mic_array, sources, surfaces)
    return mic_signals, signals_info


