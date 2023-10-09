# heron-simulator

## Installation
Python = 3.8.10
Install `Requirements.txt` with Pip

## Usage
'''
python ./simulator.py -c ./config/{your config}.toml
'''

The simulation is then performed with the setting specified in the simulation config.

## Config Description

### Simulation Config
Name | Description | Type | Example
--- | --- | --- | ---
`sr` | System sampling rate | Int | 44100
`sound_speed` | Speed of sound in m/s | Float | 340
`sources` | Table with Sources| Toml table| -
`sources.sourcename` | Source Config | Toml Table -
`sources.sourcename.position`| Position of the Source| List | [1,0,0]
`sources.sourcename.name`| Name of the Source| String | Noise1
`sources.sourcename.audio_file`| Path to audiofile of the source| String | './audio/sound1.wav'


### Microphone Confg


### Source Config
