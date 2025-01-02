import random 
import math
import numpy as np
import json
from my_debug import *


# class to generate cloud of vertices to reconstruct the a 3D from it
class CloudPoints:
    def __init__(self):
        self.cloud = [(0, 0, 0, 0)]

    # get the min and max value of coordonates of the vertice
    def min_max_axe_size(self, axe):
        if axe == 'x':
            i = 0
        if axe == 'y':
            i = 1
        if axe == 'z':
            i = 2
        min_size = self.cloud[0][i]
        max_size = self.cloud[0][i]
        for point in self.cloud:
            if point[i] < min_size:
                min_size = point[i]
            if point[i] > max_size:
                max_size = point[i]
        return min_size, max_size
    

    # get the cutting plans to which belong a face  
    def get_list_of_plans_for_faces(self, z0_min, z0_max, nb_plans):
        z_step = round(((z0_max - z0_min) / nb_plans), 2)
        
        list_of_z0s = []
        z0 = z0_min

        while z0 <= z0_max:
            z0 = z0 + z_step
            list_of_z0s.append(round(z0, 2))

        return list_of_z0s
    
    # gen vertices on the plans z = z0 + tan(theta)*x for z0 in z0_list
    def gen_random_cloud(self, shape,  min_size, max_size, nb_points, z0_list, theta):
        self.cloud = [0]*(len(z0_list)*nb_points)
        mu = (min_size + max_size) / 2
        sigma = (max_size - min_size) 
        k = 0
        for z0 in z0_list:
            for i in range(nb_points):
                x = round(random.gauss(mu, sigma), 2)

                if shape == 'circle':
                   radius = 2

                   while  abs(x) > radius:
                      x = round(random.gauss(mu, sigma), 2)
                   
                   
                   y = ((-1)**i)*round(math.sqrt(radius*radius - x*x), 2)
                   z = round(z0 + math.tan(theta)*x, 2)

                if shape == 'cylinder':
                    radius = 1.5

                    while  abs(x) > radius:
                      x = round(random.gauss(mu, sigma), 2)
                   
                    z = ((-1)**i)*round(math.sqrt(radius*radius - x*x), 2)
                    y = ((-1)**random.randint(1,10))*2 
                     
                if shape == 'random':
                   
                   y = round(random.gauss(mu, sigma), 2) 
                   z = round(z0 + math.tan(theta)*x, 2)
                
                self.cloud[i + k*nb_points] = (x, y, z, i + k*nb_points)
                
            k = k + 1

        self.save_generated_cloud(self.cloud)
        return self.cloud
    
   
    
    def save_generated_cloud(self, points):
        
        # Serializing json
        json_object = json.dumps(points)
 
        # Writing to sample.json
        with open("cloud.json", "w") as outfile:
             outfile.write(json_object)

    def get_the_last_generated_cloud(self, file_name):

        # Opening JSON file
        with open(file_name, 'r') as openfile:
 
        # Reading from json file
            points = json.load(openfile)
        return points
    
   

    
    def gen_cloud_tube(self):
        self.vertices = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1), 
                                  (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1), (1.5, 0, 0.5, 1), (1.5, 1, 0.5, 1)])
        
        self.faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 4, 5, 1], [2, 3, 8, 9], [8, 9, 6, 7], [1, 2, 9, 6, 5], [0, 3, 8, 7, 4]]
