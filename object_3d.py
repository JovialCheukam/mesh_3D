import pygame as pg
from linear_transforms import *
from my_debug import *


class Object3D:
    def __init__(self, render, vertices, faces):
        self.render = render
        self.vertices = np.array(vertices)
        #correct_faces(faces)
        self.faces = faces
        self.font = pg.font.SysFont('Arial', 30, bold = True)
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]
        self.movement_flag, self.draw_vertices = True, False
        self.label = ''
        self.is_axe = False
        self.draw_edge = True

    def draw(self):
        self.screen_perspectivity()
        self.movement()

    def movement(self):
        if self.movement_flag:
            self.rotate_around_y(pg.time.get_ticks() % 0.01)
        
    # draw the object in the camera visible space
    def screen_perspectivity(self):

        # move the space origin axes to coincide with the camera
        vertices = self.vertices @ self.render.camera.camera_matrix()

        # project to the clip space
        vertices = vertices @ self.render.perspectivity.perspectivity_matrix

        # normalise coordinates en cut unecessary vertices
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices[(vertices > 3) | (vertices < -3)] = 0

        # transfert to screen resolution
        vertices = vertices @ self.render.perspectivity.to_screen_matrix
        vertices = vertices[:, :2]
        
        # draw faces of the 3d object
        if self.draw_edge:
            for index, color_face in enumerate(self.color_faces):
                color, face = color_face
                polygon = vertices[face]
                if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
                    if self.is_axe or len(polygon) > 1:
                        pg.draw.polygon(self.render.screen, color, polygon, 1)
                    if self.label:
                        text = self.font.render(self.label[index], True, pg.Color('white'))
                        self.render.screen.blit(text, polygon[-1])
        
        # draw vertices forming faces of the 3d object
        if self.draw_vertices:
           for vertex in vertices:
               if not np.any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)

    # manipulate the position of the object by translating, rotating or scaling it
    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos)

    def scale(self, scale_to):
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_around_x(self, angle):
        self.vertices = self.vertices @ rotate_around_x(angle)

    def rotate_around_y(self, angle):
        self.vertices = self.vertices @ rotate_around_y(angle)

    def rotate_around_z(self, angle):
        self.vertices = self.vertices @ rotate_around_z(angle)

# define the space axes or the axis of the object
class Axes(Object3D):
    def __init__(self, render):
        self.render = render
        self.vertices = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.font = pg.font.SysFont('Arial', 30, bold = True)
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertices = False
        self.label = 'XYZ'
        self.is_axe = True
        self.draw_edge = True
        

    