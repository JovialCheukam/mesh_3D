import pygame as pg
import imageio
from linear_transforms import *


class Camera:
    def __init__(self, render, position):
        self.render = render

        # initial position of the camera
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

        # angular horizontal view of the image
        self.h_fv = math.pi / 3

        # angular verticaal view of the image
        self.v_fv = self.h_fv * (render.HEIGHT / render.WIDTH)

        # define the visible part of the image viewed by the camera
        self.near_visible_plane = 0.1
        self.far_visible_plane = 100

        # define the translation and rotation speed of the camera
        self.moving_speed = 0.06
        self.rotation_speed = 0.01

    # to manipulate the camera using keyboard of the pc computer
    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_d]:
            self.position -= self.right * self.moving_speed
        if key[pg.K_q]:
            self.position += self.right * self.moving_speed
        if key[pg.K_z]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pg.K_w]:
            self.position += self.up * self.moving_speed
        if key[pg.K_x]:
            self.position -= self.up * self.moving_speed

        if key[pg.K_LEFT]:
            self.camera_rotate_around_y(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_rotate_around_y(self.rotation_speed)
        if key[pg.K_UP]:
            self.camera_rotate_around_x(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_rotate_around_x(self.rotation_speed)

    def camera_rotate_around_y(self, angle):
        rotate = rotate_around_y(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_rotate_around_x(self, angle):
        rotate = rotate_around_x(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    # used to move the space origin axes to coincide with the camera
    def translate_matrix(self):
         x, y, z, w = self.position
         return np.array([
             [1, 0, 0, 0],
             [0, 1, 0, 1],
             [0, 0, 1, 0],
             [-x, -y, -z, 1]
         ])
    
    
    # used to move the space axes so that it orientation coincide with the orientation of camera
    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
    
    # set the space origine and orientation to coincide with camera
    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()
    

    # create animated gif:
    def create_gif(self, screen, gif_name, FPS):
        files = []
        
        done_capturing = False
        file_num = 0
        while not done_capturing:
             file_num = file_num + 1
             image = pg.display.get_surface()
             screen.blit(image, (0,0))
             pg.display.update()
             
             # Save every frame
             filename = "reconstruction_exples/%04d.png" % file_num
             pg.image.save(image, filename)

             files.append(filename)
             for event in pg.event.get():
                if event.type == pg.QUIT:
                  done_capturing = True

        with imageio.get_writer(gif_name+'.gif', fps = FPS ) as writer:
             for file in files:
                 image = imageio.imread(file)
                 writer.append_data(image)
                 