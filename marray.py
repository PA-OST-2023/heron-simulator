import tomli
from devices.microphone import Microphone

def open_array(config):
    with open(config, 'rb') as f:
        config = tomli.load(f)
    m_type = config.get('type', 'mic')
    m_config = f'config/{m_type}.toml'
    for k, v in config['microphones'].items():
        print(v)
        position = v.get('position', None)
        normal = v.get('normal', None)


if __name__ == '__main__':
    print(1)
    open_array('config/array.toml')
