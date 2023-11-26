import tomli
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from .devices.source import Source
from .devices.microphone import Microphone


def open_array(array_config, mic_type="./config/testMic.toml", center=None, normal=None):
    """
    Creates a Mic Array based on a geometric config and Mycrophone Type

    [TODO:description]

    Parameters
    ----------
    array_config : String
        path of Array config file
    mic_type : String
        Path of Microphone config file
    """
    print("Initilaize Array")
    with open(array_config, "rb") as f:
        config = tomli.load(f)
    mic_config = mic_type
    if center is not None:
        offset = np.array(center)
    else:
        offset = np.zeros(3)
    if normal is not None:
        r = get_rot_m(np.array([1,0,0], dtype=np.float32), np.array(normal, dtype=np.float32))
    else:
        r = np.eye(3)
    mics = []
    for k, v in config["microphones"].items():
        position = v.get("position", None)
        if position is None:
            raise Exceptions('No mic Pos')
        position = np.array(position)
        position = r @ position.T + offset
        normal = v.get("normal", None)
        mic = Microphone(mic_config, position, normal, k)
        mics.append(mic)
    print("initilaized")
    return mics, config

def open_array_from_numpy(positions, mic_type, center=None, normal=None):
    print("Initilaize Array")
    if center is not None:
        offset = np.array(center)
    else:
        offset = np.zeros(3)
    if normal is not None:
        r = get_rot_m(np.array([1,0,0], dtype=np.float32), np.array(normal, dtype=np.float32))
    else:
        r = np.eye(3)
    mics = []
    for i, position in enumerate(positions):
        position = r @ position.T + offset
        mic = Microphone(mic_type, position, name=f'{i}')
        mics.append(mic)
    print("Initialized Array")
    return mics



def get_rot_m(n, n_new):
    n_new = n_new / np.linalg.norm(n_new)
    n = n / np.linalg.norm(n)
    v = np.cross(n, n_new)
    s = np.linalg.norm(v)
    c = np.dot(n, n_new)
    vx = np.array([[0, -v[2], v[1]],[v[2], 0, -v[0]],[-v[1], v[0], 0]])
#     import ipdb; ipdb.set_trace()
    r = np.eye(3) + vx + np.dot(vx, vx) *(1-c)/s**2
    return r

def plot_array(mic_array, sources, walls=None):
    source_mesh = o3d.geometry.TriangleMesh()
    for source in sources:
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.131)
        sphere.translate(source.position)
        source_mesh += sphere
    mic_mesh = o3d.geometry.TriangleMesh()
    for mic in mic_array:
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.021)
        sphere.translate(mic.position)
        mic_mesh += sphere
    zero_ground = []
    ground_col = []
    for i in np.arange(-10,11,0.1):
        for j in np.arange(-10,11,0.1):
            zero_ground.append(np.array([i, j, 0]))
            col = np.array([0,0,0])
            if np.abs(i) < 0.01:
                col = np.array([1,0,0])
            if np.abs(j) < 0.01:
                col = np.array([0,1,0])
            ground_col.append(col)
    ground_pcd = o3d.geometry.PointCloud()
    ground_pcd.points = o3d.utility.Vector3dVector(np.array(zero_ground))
    ground_pcd.colors = o3d.utility.Vector3dVector(np.array(ground_col))
#     ground_mesh = o3d.geometry.TriangleMesh()
#     for g in zero_ground:
#         sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.05)
#         sphere.translate(g)
#         ground_mesh += sphere
    wall_pcd = o3d.geometry.PointCloud()
    wall_points = []
    if walls:
        for wall in walls:
            wall = [np.array(vec, dtype=np.float32) for vec in wall]
            p, u, v = wall
            u = u / np.linalg.norm(u)
            v = v / np.linalg.norm(v)
            for s in np.arange(-10,11,0.1):
                for t in np.arange(-10,11,0.1):
                    wall_points.append(p + s * u + t *v)
        wall_pcd.points = o3d.utility.Vector3dVector(np.array(wall_points))
    mic_mesh.paint_uniform_color([1.0, 0.75, 0.0])
    source_mesh.paint_uniform_color([0.1, 0.75, 1.0])
    wall_pcd.paint_uniform_color([0.01, 0.99, 0.66])
#     ground_pcd.paint_uniform_color([0.0, 0.05, 0.0])
    o3d.visualization.draw_geometries([mic_mesh, source_mesh, ground_pcd, wall_pcd])


if __name__ == "__main__":
    n = np.array([0.1,0.1,1])
    n_new = np.array([1,1,-1])
    r = get_rot_m(n, n_new)
    n_t = r @ n.T
    print(f'{n =}')
    print(f'{n_new =}')
    print(f'{r =}')
    print(f'{n_t =}')
    import ipdb; ipdb.set_trace()

    import hans
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
