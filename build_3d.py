import math
from sklearn import linear_model
from my_debug import *

class Polyhedra3d:

    # initiate a cloud of indexed vertices  which represent a polyhedra
    def __init__(self, vertices):
        self.vertices = vertices
        self.original_vertices = list(vertices)

    # extract the coordonates of a vertex in an (x,y,z) space
    def get_coord_x(self, vertex):
           return vertex[0]
    
    def get_coord_y(self, vertex):
           return vertex[1]
    
    def get_coord_z(self, vertex):
           return vertex[2]
        

    # compute a straight line regression model for the plane (h_axe,v_axe) to separate
    # top points from bottom points 
    def get_straight_line_separation(self, h_axe, v_axe, set_of_vertices):
        h, v, z = self.get_plan_face(h_axe, v_axe)
        length = len(set_of_vertices)
        h_train = [0] * length
        v_train = [0] * length

        for j in range(length):
            h_train[j] = [set_of_vertices[j][h]]
            v_train[j] = [set_of_vertices[j][v]]

        reg = linear_model.LinearRegression()
        reg.fit(h_train,v_train)

        # get coef a and b of the straight separate line v = a*h+b
        #print_along('coef',reg.coef_)
        
        return reg
         

    
    # given two axes (h_axe, v_axe) identify the plan given by the vertcal axe and the 
    # third axe
    def get_plan_face(self, h_axe, v_axe):
        if v_axe == 'x' and h_axe == 'y':
            h, v, z = 1, 0, 2
        if v_axe == 'x' and h_axe == 'z':
            h, v, z = 2, 0, 1
        if v_axe == 'y' and h_axe == 'x':
            h, v, z = 0, 1, 2
        if v_axe == 'y' and h_axe == 'z':
            h, v, z = 2, 1, 0
        if v_axe == 'z' and h_axe == 'x':
            h, v, z = 0, 2, 1
        if v_axe == 'z' and h_axe == 'y':
            h, v, z = 1, 2, 0
        return h, v, z 
         
            
    
    # separate index from their coresponding vertex components to get the face
    def get_face_from_it_vertices(self, face_vertices_with_indexes):
        
        face = []
        for vertex_index in face_vertices_with_indexes:
            face.append(vertex_index[3])

        return face


                
    # get all the vertices forming a face on the plan z + z0 = 0  
    def get_orthogonal_face_for_zvalue(self, h_axe, v_axe, z0):
        

        # get all the vertices belonging to the plan z + z0 = 0
        face_vertices = []
        h, v, z = self.get_plan_face(h_axe, v_axe)

        for vertex in self.vertices:

            # Instead of using == we use <= to consider numeric instability
            if abs(vertex[z] + z0) <= 0.05:
               face_vertices.append(vertex)
                
        # get min and max vertices forming a face on the plan z + z0 = 0
        
        if face_vertices == []:
            return face_vertices
        
        #print_to_newline('face_vertices',face_vertices)
        
        regression = self.get_straight_line_separation(h_axe, v_axe, face_vertices)
        face_vertices_min = []
        face_vertices_max = []

        for vertex_ in face_vertices:

            if vertex_[v] < regression.predict([[vertex_[h]]])[0]:
                   face_vertices_min.append(vertex_)
            else:
                   face_vertices_max.append(vertex_)


        def get_h_value(vertice_):
            return vertice_[h]
        face_vertices_min.sort(key = get_h_value)
        face_vertices_max.sort(key = get_h_value)

        
        #print_to_newline('face_vertices_min',face_vertices_min)

        #print_to_newline('face_vertices_max',face_vertices_max)

        n = len(face_vertices_max)
        face_vertices_max = [face_vertices_max[n - 1 - i] for i in range(n)]

        

        face_vertices_with_indexes = self.avoid_intersection(h, v, face_vertices_min, face_vertices_max)
        #face_vertices_with_indexes = face_vertices_min + face_vertices_max

        #print_to_newline('face_vertices_with_indexes', face_vertices_with_indexes)

        

        # remove vertices of the identified face
        self.vertices = [vertex for vertex in self.vertices if vertex not in face_vertices_with_indexes] 

        return self.get_face_from_it_vertices(face_vertices_with_indexes)
    
    # avoid intersection between edges at the right extremity of the face
    def avoid_intersection(self, h, v, face_vertices_min, face_vertices_max):

        if len(face_vertices_min) <= 2 or len(face_vertices_max) < 1:

            return face_vertices_min + face_vertices_max
        else:

            
            x0 = face_vertices_min[-3][h]
            y0 = face_vertices_min[-3][v]
            x1 = face_vertices_min[-2][h]
            y1 = face_vertices_min[-2][v]

            x2 = face_vertices_min[-1][h]
            y2 = face_vertices_min[-1][1]
            x3 = face_vertices_max[0][h]
            y3 = face_vertices_max[0][v]

            if x1 == x0 or x3 == x2:
                return face_vertices_min + face_vertices_max

            a0 = (y1 - y0) / (x1 - x0)
            b0 = y0 - a0*x0

            a1 = (y3 - y2) / (x3 - x2)
            b1 = y2 - a1*x2

            x_intersect = (b1 - b0) / (a0 - a1)
            is_between = (x0 < x_intersect and x_intersect < x1) or (x1 < x_intersect and x_intersect < x0)

            if a0 * b1 != a1 * b0 and is_between :
                return face_vertices_min[:-2]+[face_vertices_min[-1]] + [face_vertices_min[-2]] + face_vertices_max
            else:
                if len(face_vertices_max) <= 2 or len(face_vertices_min) < 1:

                   return face_vertices_min + face_vertices_max
                else:

            
                    x0 = face_vertices_max[1][h]
                    y0 = face_vertices_max[1][v]
                    x1 = face_vertices_max[2][h]
                    y1 = face_vertices_max[2][v]

                    x2 = face_vertices_max[0][h]
                    y2 = face_vertices_max[0][v]
                    x3 = face_vertices_min[-1][h]
                    y3 = face_vertices_min[-1][v]

                    if x1 == x0 or x3 == x2:
                       return face_vertices_min + face_vertices_max

                    a0 = (y1 - y0) / (x1 - x0)
                    b0 = y0 - a0*x0

                    a1 = (y3 - y2) / (x3 - x2)
                    b1 = y2 - a1*x2

                    x_intersect = (b1 - b0) / (a0 - a1)
                    is_between = (x0 < x_intersect and x_intersect < x1) or (x1 < x_intersect and x_intersect < x0)

                    if a0 * b1 != a1 * b0 and is_between :
                        return face_vertices_min + [face_vertices_max[1]]+[face_vertices_max[0]] + face_vertices_max[2:]
                    else:
                        return face_vertices_min + face_vertices_max
        
        

    
    # get the min and max value on the z component
    def get_min_max_of_zvalue(self, z_axe):
        if z_axe == 'x':
            z = 0
        if z_axe == 'y':
            z = 1
        if z_axe == 'z':
            z = 2

        min_value_on_z_axe = self.vertices[0][z]
        max_value_on_z_axe = self.vertices[0][z]

        for vertex in self.vertices:
            if vertex[z] < min_value_on_z_axe:
                min_value_on_z_axe = vertex[z]
            if vertex[z] > max_value_on_z_axe:
                min_value_on_z_axe = vertex[z]

        return min_value_on_z_axe, max_value_on_z_axe
    

    # separate index from their coresponding vertex components to get vertices cloud
    def get_vertices_for_faces(self):
        face_vertices = []
        
        for vertex_index in self.original_vertices:
            face_vertices.append((vertex_index[0],vertex_index[1],vertex_index[2],
                                  1))

        return face_vertices

    
    # generate a meshe version of the polyhedra from the cloud of vertices
    def generate_meshe_for_theta_plan(self, h_axe, v_axe, list_of_z0s):
        list_of_faces = []
        for z0 in list_of_z0s:
            
              #print_along('---Process face', z0)
              face =  self.get_orthogonal_face_for_zvalue(h_axe, v_axe, z0)
              #print_to_newline('face', face)
              list_of_faces.append(face)
              
        
        list_of_vertices = self.get_vertices_for_faces()
        #print_to_newline('list_of_vertices', list_of_vertices)

        #print_to_newline('list_of_faces', list_of_faces)
        
        return list_of_vertices, list_of_faces
