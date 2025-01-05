import pygame as pg
from object_3d import *
from camera import *
from perspectivity import *
from build_3d import *
from points_cloud import *
from collect_cloud import *
from marchin_cube import *
import numpy as np


from my_debug import *

class Rendering3D:
    def __init__(self):
        pg.init()

        # widow resolution
        self.RES = self.WIDTH, self.HEIGHT = 1200, 900

        # drawing surfcae
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2

        # number of frames per second
        self.FPS = 100
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()
    
    # create the 3D object to render
    def create_objects(self):
        
        # get the cloud of points 
        points = CloudPoints().get_the_last_generated_cloud('cloud.json')
        
        # generate faces using parallel cutting planes
        # generate the points cloud 
        nb_cutting_plans = 25
        z0_min = -3
        z0_max = 3
    

        pre_points = CloudPoints()  
        z0_list = pre_points.get_list_of_plans_for_faces(z0_min, z0_max, nb_cutting_plans)

        #print_to_newline('z0_list', z0_list)
        
        #points = pre_points.gen_random_cloud('circle',z0_min, z0_max, 300, z0_list)
        
        #points = pre_points.gen_unregular_surface(z0_min, z0_max, 100, z0_list)
        
        # set the vertices and faces of the 3d of the object
        cloud = Polyhedra3d(points)
        vertices, faces_1 = cloud.generate_meshe_for_theta_plan('x','y', z0_list)
        vertices_, faces_2 = cloud.generate_meshe_for_theta_plan('x','z', z0_list)
        faces =  faces_1 + faces_2
        
        #faces = faces_2
        #print_to_newline('faces', faces)
        #print_to_newline('vertices', vertices)
        """
        
        # generate faces using marching cubes
        points = TriangleMesh(points)
        vertices, faces = points.apply_marching_cubes()
        vertices = points.get_points_with_indexes(vertices)

        for i, vertex in enumerate(vertices):
            print(i)
            if vertex[0] > 2.4 or vertex[1] > 2.4 or vertex[2] > 2.4 :
                print('vertice rank:', i)
                print_along('vertex', vertex)
        
        
        #print('vertices \n', vertices, '\nlen:', len(vertices))
        #print('faces \n', faces, '\nlen:', len(faces))
        """
        # set the camera
        self.camera = Camera(self, [0.5, 1, -11])
        self.perspectivity = Perspectivity(self)

        # generate the mesh object
        self.object = Object3D(self, vertices, faces)
        self.object.translate([0.2, 0.4, 0.2])
        self.object.rotate_around_y(math.pi / 6)

        #self.axes = Axes(self)
        #self.axes.translate([0.7, 0.9, 0.7])

        # generate the space axes
        self.world_axes = Axes(self)
        self.world_axes.movement_flag = False
        self.world_axes.scale(2.5)
        self.world_axes.translate([0.0001, 0.0001, 0.0001])

    def draw(self):

        # color of the screen
        self.screen.fill(pg.Color('darkslategray'))

        self.world_axes.draw()
        #self.axes.draw()
        self.object.draw()

    def run(self):
        while True:
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]

            # display and update the frames
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)
            #self.camera.create_gif(self.screen,'irregular',self.FPS)


if __name__ == '__main__':
   window = DataCollectWindow()
   window.data_cloud_collect().mainloop()
   appli = Rendering3D()
   appli.run()
   