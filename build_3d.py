import math
from my_debug import *

class Polyhedra3d:

    # initiate a cloud of indexed vertices  which represent a polyhedra
    def __init__(self, vertices):
        self.vertices = vertices
        self.original_vertices = list(vertices)

    # extract the coordonates of a vertex in an (x,y,z) space
    def get_coord_x(self, vertex):
           return vertex[0]
    
    def get_coord_z(self, vertex):
           return vertex[1]
    
    def get_coord_y(self, vertex):
           return vertex[2]
        
    # sort the values of vertices following one axe (horizontal axe) among x, y or z axes 
    # of the space
    def sort_for_h_axe(self, h_axe):
         if h_axe == 'x':
            self.vertices.sort(key = self.get_coord_x)
         if h_axe == 'y':
            self.vertices.sort(key = self.get_coord_y)
         if h_axe == 'z':
            self.vertices.sort(key = self.get_coord_z)
         
         return self.vertices

    # compute the mean of values for v_axe 
    def get_v_mean(self, v_axe, set_of_vertices):
        if v_axe == 'x':
            i = 0
        if v_axe == 'y':
            i = 1
        if v_axe == 'z':
            i = 2
        mean = 0
        for vertex in set_of_vertices:
            mean = mean + vertex[i]
        
        return round((mean / len(set_of_vertices)), 2)
         
    

    # cluster the cloud of vertices where each cluster is a set of vertices which have 
    # the same value following one fixed axe 
    def get_vertices_per_value_of_h_axe(self, h_axe, sort_vertices_for_h_axe):
        vertices_per_value_of_axe = {'0':[]}
        if h_axe == 'x':
            i = 0
        if h_axe == 'y':
            i = 1
        if h_axe == 'z':
            i = 2
        rank_of_value_on_h_axe = 0
        cur_value_on_h_axe = sort_vertices_for_h_axe[0][i]

        for vertex in sort_vertices_for_h_axe:
            if vertex[i] == cur_value_on_h_axe:
                vertices_per_value_of_axe[str(rank_of_value_on_h_axe)].append(vertex)
            else:
                cur_value_on_h_axe = vertex[i]
                rank_of_value_on_h_axe += 1
                vertices_per_value_of_axe[str(rank_of_value_on_h_axe)] = [vertex]

        return vertices_per_value_of_axe
    
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
         
    # get the vertex with the min or max value of the component on the v_axe (vertical axe)  
    # which belong to the plan z = z0 + tan(theta)*x
    def get_min_max_vertices_per_hvalue_of_h_axe(self, h_axe, v_axe, vertices_per_value_of_h_axe):

        h, v, z = self.get_plan_face(h_axe, v_axe)
        for key in vertices_per_value_of_h_axe.keys():
            min_vertex_on_v_axe = vertices_per_value_of_h_axe[key][0]
            max_vertex_on_v_axe = vertices_per_value_of_h_axe[key][0]

            for vertex in vertices_per_value_of_h_axe[key]:
                   if vertex[v] < min_vertex_on_v_axe[v]:
                      min_vertex_on_v_axe = vertex
                   if vertex[v] > max_vertex_on_v_axe[v]:
                      max_vertex_on_v_axe = vertex
            vertices_per_value_of_h_axe[key] = [min_vertex_on_v_axe, max_vertex_on_v_axe]
        
        return vertices_per_value_of_h_axe
            
    
    # separate index from their coresponding vertex components to get the face
    def get_face_from_it_vertices(self, face_vertices_with_indexes):
        
        face = []
        for vertex_index in face_vertices_with_indexes:
            face.append(vertex_index[3])

        return face


                
    # get all the vertices forming a face on the plan z = z0 + tan(theta)*x 
    def get_orthogonal_face_for_zvalue(self, h_axe, v_axe, z0, theta):
        sort_vertices_for_h_axe = self.sort_for_h_axe(h_axe)
        #print_to_newline('sort_vertices_for_h_axe', sort_vertices_for_h_axe)

        vertices_per_value_of_h_axe =  self.get_vertices_per_value_of_h_axe(h_axe, sort_vertices_for_h_axe)
        #print_to_newline('vertices_per_value_of_h_axe', vertices_per_value_of_h_axe)

        min_max_v_per_value_of_h_axe = self.get_min_max_vertices_per_hvalue_of_h_axe(h_axe, v_axe, vertices_per_value_of_h_axe)
        #print_to_newline('min_max_v_per_value_of_h_axe', min_max_v_per_value_of_h_axe)

        # get all the vertices belonging to the plan z = z0 + tan(theta)*x
        face_vertices = []
        j_max = len(min_max_v_per_value_of_h_axe)
        h, v, z = self.get_plan_face(h_axe, v_axe)

        for j in range(j_max):

            vertex_min = min_max_v_per_value_of_h_axe[str(j)][0]

            # Instead of using == we use <= to consider numeric instability
            if abs(vertex_min[z] - round(z0 + math.tan(theta)*vertex_min[h], 2)) <= 0.25:
               face_vertices.append(vertex_min)
          
            vertex_max = min_max_v_per_value_of_h_axe[str(j)][1]         
            if vertex_max != vertex_min and abs(vertex_max[z] - round(z0 + math.tan(theta)*vertex_max[h], 2)) <= 0.25:
                face_vertices.append(vertex_max)
                

        # get min and max vertices forming a face on the plan z = z0 + tan(theta)*x

        if face_vertices == []:
            return face_vertices
        v_mean = self.get_v_mean(v_axe, face_vertices)
        face_vertices_min = []
        face_vertices_max = []

        for vertex in face_vertices:

            if vertex[v] < v_mean:
                   face_vertices_min.append(vertex)
            else:
                   face_vertices_max.append(vertex)

        #print_to_newline('face_vertices_min',face_vertices_min)

        #print_to_newline('face_vertices_max',face_vertices_max)

        n = len(face_vertices_max)
        face_vertices_max = [face_vertices_max[n - 1 - i] for i in range(n)]

        face_vertices_with_indexes = self.avoid_intersection(h, v, face_vertices_min, face_vertices_max)
        #face_vertices_with_indexes = face_vertices_min + face_vertices_max

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
    def generate_meshe_for_theta_plan(self, h_axe, v_axe, list_of_z0s, theta):
        list_of_faces = []
        for z0 in list_of_z0s:
            
              #print_along('---Process face', z0)
              face =  self.get_orthogonal_face_for_zvalue(h_axe, v_axe, z0, theta)
              list_of_faces.append(face)
              
        
        list_of_vertices = self.get_vertices_for_faces()
        #print_to_newline('list_of_vertices', list_of_vertices)

        #print_to_newline('list_of_faces', list_of_faces)
        return list_of_vertices, list_of_faces
