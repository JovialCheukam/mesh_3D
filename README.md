
## WELCOME TO THE 3D MESH FROM POINT CLOUD SOFTWARE !

This software do a 3D mesh reconstruction from a cloud of points which are at the surface of a solid object.
The reconstruction in 3D mesh is done by a basic algorithm which connect the points of the cloud having the maximum and 
minimum X, Y, Z values of their space components that belong to the same plane. The algorithm browses through parallel planes
of the space and connect with edges the points of the cloud belonging to those planes.

### HOW TO INSTALL THE SOFTWARE IN ORDER TO GENERATE A 3D MESH FROM YOUR CLOUD OF POINTS

To install the software, it is simple. You just need to execute in order the following steps: 

    1- you first make sure that ```python3``` and ```pygame```  are installed in your your operating system
    2- clone the software from the git repository 
    3- open a terminal and with the `cd` command, go to the directory containing the cloned repository
    4- tap in the terminal from the prevous directory the command ```python3 setup.py```
  
### HOW TO USE THE SOFTWARE TO GENERATE A 3D MESH FROM YOUR CLOUD OF POINTS

To use the software  to generate a 3D mesh from your cloud of points, do in order the following steps:

     1- Prepare your data json file containing the cloud of points from which you want to generate a 3d mesh:
          your data json file should contain a python list of tuples where each tuples has 4 components. From the left to the right, 
          the first three components represent the X, Y, Z coordonates values of each point in the space while the fourth 
          component is the rank of the tuple in the python list.
          As an example, you have *[(0.5, 0.5, 1, 0), (0.4, 1, -1.2, 1), (-2, -0.5, -1, 2), (0.5, 0.75, 1, 0)]* as a list of four 
          points where the third point is (-2, -0.5, -1, 2) which means that its space coordonates are X = -2, Y = -0.5 and Z = -2
          while it rank is 2.

     2- Make sure to have the absolute path of your data cloud json file in your operating system

     3- In the terminal, tap the command `python3 rend_3d.py`. This will pop up a window in which you are asked to enter the
            absolute path of your data cloud json file. After entering the path of your data json file, click on the button bilow
            and a new window will pop up show you your 3d mesh reconstruction of your 3D cloud.
     
     4- Manipulate the rendering view of the 3D mesh by using the following keyboard of your pc: D, Q, Z, S, W, X, LEFT, RIGHT, UP, DOWN.
    
### EXAMPLES OF 3D MESH RECONSTRUCTION