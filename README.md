# heron-simulator

## TODOS

- [ ] Reflections
- [ ] Export Time Delays for each mic after simulation
- [ ] Moving Sources

## Installation
Python = 3.8.10

Install `Requirements.txt` with Pip

## Usage
```
python ./simulator.py -c ./config/{your config}.toml
```

The simulation is then performed with the setting specified in the simulation config.

## Config Description

### Simulation Config
Name | Description | Type | Example
--- | --- | --- | ---
`sr` | System sampling rate | Int | 44100
`sound_speed` | Speed of sound in m/s | Float | 340
`out_dir` | Directory to save output files | String | './out/'
`sources` | Table with Sources| Toml table| -
`sources.sourcename` | Source Config | Toml Table -
`sources.sourcename.position`| Position of the Source| List | [1,0,0]
`sources.sourcename.name`| Name of the Source| String | 'Noise1'
`sources.sourcename.audio_file`| Path to audiofile of the source| String | './audio/sound1.wav'
`array` | Config of the Array | Toml Table | -
`array.mic_type` | Path to Microphone Config | String | './config/testMic.toml'
`array.array_config` | Path to Array Config | String | './config/array.toml'

### Microphone Confg

Name | Description | Type | Example
--- | --- | --- | ---
`info.name` |Name of the Microphon |String |'ST M123456'
`characteristics.noisefloor` |Noisefloor if the Microphone in db |Float |30
`characteristics.SNR` | | |
`characteristics.samplingrate` | | |
`characteristics.amplitude_offset` | | |

### Array Config
