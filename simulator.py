import scipy
import tomli
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

from marray import open_array, plot_array
from devices.source import Source
from devices.microphone import Microphone

parser = ArgumentParser()
parser.add_argument(
        "-c", "--config_file", help="path to general config file", default="./config/simulation.toml"
)
parser.add_argument(
        "-a", "--array_config", help="path to array config file", default="./config/array.toml"
)
parser.add_argument(
        "-s", "--source_config", help="path to source config", default=["./config/source.toml"], nargs="*"
)
args = parser.parse_args()

with open(args.config_file, 'rb') as f:
    config = tomli.load(f)

sources = [Source(conf) for conf in args.source_config]
mic_array = open_array(args.array_config)
import ipdb; ipdb.set_trace()

print(args.source_config)

