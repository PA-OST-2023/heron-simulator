import scipy
import tomli
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

from marray import open_array, plot_array
from devices.source import Source
from devices.microphone import Microphone
from audioHelper import write_wav

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
mic_signals = []
fig, ax = plt.subplots(5, 2, sharex="all")
ax[4][1].plot(np.zeros(10))
ax[4][1].set_title("source")
for i, mic in enumerate(mic_array):
    sound_at_pos_info = [
        source.get_sound_atposition(mic.position) for source in sources
    ]
    signal_at_position = [info[0] for info in sound_at_pos_info]
    normal = [info[1] for info in sound_at_pos_info]
    mic_signal = mic.simulate_mic(signal_at_position, normal)
    mic_signals.append(mic_signal)
    write_wav(mic_signal, sources[0].sr, f"./out/mic{i}.wav")
    ax[i % 5][(i - i % 5) // 5].plot(mic_signal)
    ax[i % 5][(i - i % 5) // 5].set_title(i)
plt.show()

plot_array(mic_array, sources)
