import numpy as np

def mirror_pos(pos, surface):
    normal = surface[:-1]
    t = np.sum(-1 * np.r_[pos, 1] * surface) /np.sum(normal**2)
    mirr_pos = pos + 2*t*normal
    return mirr_pos


if __name__ == '__main__':
    pos = np.array([3,1,2])
    surface = np.array([1,2,1,-1])
    print(mirror_pos(pos, surface))
