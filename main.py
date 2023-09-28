import numpy as np

from devices.source import Source
from devices.microphone import Microphone

so = Source()
mic = Microphone()
so.test()
mic.test()
print(mic.position)
mic.position = np.ones((1,3))
print(mic.position)
mic.set_source(so)
print(so.get_sound_at_position(np.ones((1,3))))

