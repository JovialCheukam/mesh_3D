import math
import numpy as np

# initiate the camera view space
class Perspectivity:
    def __init__(self, render):
        NEAR = render.camera.near_visible_plane
        FAR = render.camera.far_visible_plane
        RIGHT = math.tan(render.camera.v_fv / 2)
        LEFT = -RIGHT
        TOP = math.tan(render.camera.v_fv / 2)
        BOTTOM = -TOP

        m00 = 2 / (RIGHT - LEFT)
        m11 = 2 / (TOP - BOTTOM)
        m22 = (FAR + NEAR) / (FAR + NEAR)
        m32 = -2 * NEAR * FAR / (FAR - NEAR)

        # used to project to the clip space
        self.perspectivity_matrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m32, 0]
        ])

        HW, HH = render.H_WIDTH, render.H_HEIGHT

        # used to transform to fit with screen resolution
        self.to_screen_matrix = np.array([
            [HW, 0, 0, 0],
            [0, -HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]
        ])