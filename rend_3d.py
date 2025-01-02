import pygame as pg
from object_3d import *
from camera import *
from perspectivity import *
from build_3d import *
from points_cloud import *
from collect_cloud import *

from my_debug import *

class Rendering3D:
    def __init__(self):
        pg.init()

        # widow resolution
        self.RES = self.WIDTH, self.HEIGHT = 1200, 900

        # drawing surfcae
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2

        # number of frames per second
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()
    
    # create the 3D object to render
    def create_objects(self):
                
        # generate the points cloud  
        nb_cutting_plans = 150
        z0_min = -5
        z0_max = 5
    

        pre_points = CloudPoints()  
        z0_list = pre_points.get_list_of_plans_for_faces(z0_min, z0_max, nb_cutting_plans)
        
        #points = pre_points.gen_random_cloud('cylinder',z0_min, z0_max, 100, z0_list, 0.2)
        points = CloudPoints().get_the_last_generated_cloud('cloud.json')
        
        
        # set the vertices and faces of the 3d of the object
        cloud = Polyhedra3d(points)
        vertices, faces_x_y = cloud.generate_meshe_for_theta_plan('x','y', z0_list, 0.2)
        _, faces_z_y = cloud.generate_meshe_for_theta_plan('z','y', z0_list, 0.2)
        faces = faces_x_y + faces_z_y

        # set the camera
        self.camera = Camera(self, [0.5, 1, -9])
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


if __name__ == '__main__':
   window = DataCollectWindow()
   window.data_cloud_collect().mainloop()
   appli = Rendering3D()
   appli.run()
   