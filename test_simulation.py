#!/usr/bin/env python
import scipy
import tomli
import tomli_w
import numpy as np
from numpy import sin, cos, pi
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import os

from marray import open_array, plot_array
from devices.source import Source
from devices.microphone import Microphone
from audioHelper import write_wav
from geometry import mirror_pos
from simulation import static_simulation

# def static_simulation(mic_array, sources, surfaces=None):
#     """
#     Perform a simulation with static position of the sources
#     and microphone array
# 
#     [TODO:description]
# 
#     Parameters
#     ----------
#     mic_array : list
#         List of Microphones
#     sources : list
#         List of Source
#     """
#     mic_signals = []
#     signals_info = {}
#     for i, mic in enumerate(mic_array):
#         sound_at_pos_info = [
#             source.get_sound_at_position(mic.position) for source in sources
#         ]
#         signal_at_position = [info[0] for info in sound_at_pos_info]
#         if surfaces is not None:
#             mirrors = [mirror_pos(mic.position, surface) for surface in surfaces]
#             mirros_sigs = [source.get_sound_from_mirror_pos(pos) for source in sources for pos in mirrors]
#             signal_at_position += mirros_sigs
#         normal = [info[1] for info in sound_at_pos_info]
#         delays = {
#             source.name: info[2] for source, info in zip(sources, sound_at_pos_info)
#         }
#         mic_signal = mic.simulate_mic(signal_at_position, normal)
#         mic_signals.append(mic_signal)
#         signals_info[mic.name] = delays
# 
#     plot_array(mic_array, sources, walls)
#     return mic_signals, signals_info



parser = ArgumentParser()
parser.add_argument(
    "-c",
    "--config_file",
    help="path to general config file FUCK YOU",
    default="./config/simulation.toml",
)

parser.add_argument(
    "-a",
    "--angles_file",
    help="File to angles configuration",
    default="./config/simulation.toml",
)
args = parser.parse_args()

with open(args.config_file, "rb") as f:
    config = tomli.load(f)

with open(args.angles_file, "rb") as f:
    angles_config = tomli.load(f)

sources_dict = config.get("sources", None)
if sources_dict is None:
    raise ValueError("No Sources")
source_config_file = sources_dict.get('config', None)
if source_config_file is not None:
    print('sources from File')
    with open(source_config_file, "rb") as f:
        sources_dict = tomli.load(f)
sources_configs = [v for k, v in sources_dict.items()]

sources = [Source(gain=10, **source_cfg) for source_cfg in sources_configs]

array_cfg = config["array"]

walls = config.get("walls", None)
mic_array, mic_positions = open_array(**array_cfg)

out_dir = config.get("out_dir", "./out/")
isExist = os.path.exists(out_dir)
if not isExist:
    # Create a new directory because it does not exist
    os.makedirs(out_dir)

azimuth = angles_config['az']
elevation = angles_config['el']
azimuth_padded = azimuth + [2] * len(elevation)
elevation_padded= [87]*len(azimuth) + elevation
prefix = ["az"] * len(azimuth)+ ["el"]*len(elevation)
r=15
for az, el, n in zip(azimuth_padded, elevation_padded, prefix):
    az_rad = az/180 * pi
    el_rad = el/180 * pi
    x = sin(el_rad) * cos(az_rad) * r
    y = sin(el_rad) * sin(az_rad) * r
    z = cos(el_rad) * r
    sources[0].position = np.array([x,y,z])
    signals, signals_info = static_simulation(mic_array, sources, walls)
    data = np.vstack(signals).astype(np.float32)
    data = np.swapaxes(data, 0,1)
    suff = el
    if n == "az":
        suff = az
    write_wav(data, sources[0].sr, f"{out_dir}{n}_{suff}.wav")
#         write_wav(mic.recorded_audio, sources[0].sr, f"{out_dir}{mic.name}.wav")
