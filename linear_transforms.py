import math
import numpy as np

# translate a set of space points along the (t_x, t_y, t_z) vector
def translate(pos):
    t_x, t_y, t_z = pos
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [t_x, t_y, t_z, 1]
    ])

# rotate  a set of space points around the x, y or z axe:
def rotate_around_x(alpha):
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(alpha), math.sin(alpha), 0],
        [0, -math.sin(alpha), math.cos(alpha), 0],
        [0, 0, 0, 1]
    ])

def rotate_around_y(alpha):
    return np.array([
        [math.cos(alpha), 0, -math.sin(alpha), 0],
        [0, 1, 0, 0],
        [math.sin(alpha), 0,  math.cos(alpha), 0],
        [0, 0, 0, 1]
    ])

def rotate_around_z(alpha):
    return np.array([
        [math.cos(alpha), math.sin(alpha), 0, 0],
        [-math.sin(alpha), math.cos(alpha), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

# scale the edges formed by the set of points with a scaling ratio equal to k
def scale(k):
    return np.array([
        [k, 0, 0, 0],
        [0, k, 0, 0],
        [0, 0, k, 0],
        [0, 0, 0, 1]
    ])