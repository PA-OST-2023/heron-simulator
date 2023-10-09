import scipy
import tomli
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

from marray import open_array, plot_array
from devices.source import Source
from devices.microphone import Microphone
from audioHelper import write_wav


def static_simulation(mic_array, sources):
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
    for i, mic in enumerate(mic_array):
        sound_at_pos_info = [
            source.get_sound_at_position(mic.position) for source in sources
        ]
        signal_at_position = [info[0] for info in sound_at_pos_info]
        normal = [info[1] for info in sound_at_pos_info]
        mic_signal = mic.simulate_mic(signal_at_position, normal)
        mic_signals.append(mic_signal)
        write_wav(mic_signal, sources[0].sr, f"./out/{mic.name}.wav")

    plot_array(mic_array, sources)
    return mic_signals


parser = ArgumentParser()
parser.add_argument(
    "-c",
    "--config_file",
    help="path to general config file",
    default="./config/simulation.toml",
)
args = parser.parse_args()

with open(args.config_file, "rb") as f:
    config = tomli.load(f)

sources_dict = config.get("sources", None)
if sources_dict is None:
    raise ValueError("No Sources")
sources_configs = [v for k, v in sources_dict.items()]

sources = [Source(**source_cfg) for source_cfg in sources_configs]

array_cfg = config["array"]
mic_array = open_array(**array_cfg)
signals = static_simulation(mic_array, sources)
