import numpy as np

def mirror_pos(pos, surface, as_param=True):
    if as_param:
        surface = converto_to_zero(surface)
    print(surface)
    normal = surface[:-1]
    t = np.sum(-1 * np.r_[pos, 1] * surface) /np.sum(normal**2)
    mirr_pos = pos + 2*t*normal
    return mirr_pos

def converto_to_zero(surface):
    A = np.array(surface).reshape(3,3)
    print(A)
    b = np.array([1,0,0])
    coefs = np.linalg.solve(A, b)
    return np.r_[coefs, -1]

if __name__ == '__main__':
    q = np.array([1,3,1])/11
    v = np.array([1,0,-1])
    u = np.cross(q, v)
    g = [q,v,u]
    pos = np.array([3,1,2])

    print(mirror_pos(pos, g))

    surface = np.array([1,3,1,-1])
    print(mirror_pos(pos, surface, False))
