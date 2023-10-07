import tomli
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from devices.source import Source
from devices.microphone import Microphone


def open_array(array_config, mic_type="./config/testMic.toml"):
    print('Initilaize Array')
    with open(array_config, "rb") as f:
        config = tomli.load(f)
    mic_config = mic_type
    mics = []
    for k, v in config["microphones"].items():
        position = v.get("position", None)
        normal = v.get("normal", None)
        mic = Microphone(mic_config, position, normal, k)
        mics.append(mic)
    print("initilaized")
    return mics


def plot_array(mic_array, sources):
    source_mesh = o3d.geometry.TriangleMesh()
    for source in sources:
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.131)
        sphere.translate(source.position)
        source_mesh += sphere
    mic_mesh = o3d.geometry.TriangleMesh()
    for mic in mic_array:
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.131)
        sphere.translate(mic.position)
        mic_mesh += sphere
    mic_mesh.paint_uniform_color([1.0, 0.75, 0.0])
    source_mesh.paint_uniform_color([0.1, 0.75, 1.0])
    o3d.visualization.draw_geometries([mic_mesh, source_mesh])


if __name__ == "__main__":
    mic_array = open_array("config/array.toml")
    xx = np.linspace(0, 3, 44100 * 3)
    sigi = (
        np.sin(50 * xx)
        + np.cos(25 * xx)
        + np.sin(12.5 * xx + 2)
        + np.cos(6.25 * xx + 0.7)
    )
    fig, ax = plt.subplots()
    ax.plot(xx, sigi)
    plt.show()
    source = Source()
    source.add_sound(sigi)
    mic_signals = []
    fig, ax = plt.subplots(5, 2, sharex="all")
    ax[4][1].plot(xx, sigi)
    ax[4][1].set_title("source")
    for i, mic in enumerate(mic_array):
        signal_at_position, normal = source.get_sound_at_position(mic.position)
        mic_signal = mic.simulate_mic([signal_at_position], [normal])
        mic_signals.append(mic_signal)
        ax[i % 5][(i - i % 5) // 5].plot(xx[:-22], mic_signal)
        ax[i % 5][(i - i % 5) // 5].set_title(i)
    plt.show()
    plot_array(mic_array, [source])
