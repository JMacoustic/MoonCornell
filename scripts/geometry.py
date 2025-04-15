# This code is originated from pyglet basic shapes and I added more functionalities such as deform and move

import pyglet
from pyglet import model
from math import pi, sin, cos
from pyglet.math import Mat4

class Cube(model.Model):

    def __init__(self, width=1.0, height=1.0, depth=1.0, color=(1.0, 1.0, 1.0, 1.0),
                 material=None, batch=None, group=None, program=None):
        self._width = width
        self._height = height
        self._depth = depth
        self._color = color
        self.deformation = Mat4()
        self.movement = Mat4()

        self._batch = batch
        self._program = program if program else model.get_default_shader()

        # Create a Material and Group for the Model
        self._material = material if material else model.SimpleMaterial(name="cube")
        self._group = pyglet.model.MaterialGroup(material=self._material, program=self._program, parent=group)

        self._vlist = self._create_vertexlist()

        super().__init__([self._vlist], [self._group], self._batch)

    def _create_vertexlist(self):
        w = self._width / 2
        h = self._height / 2
        d = self._depth / 2

        vertices = [
            -w, -h, -d,   # front, bottom-left    0
            w, -h, -d,    # front, bottom-right   1
            w, h, -d,     # front, top-right      2         Front
            -w, h, -d,    # front, top-left       3

            w, -h, d,     # back, bottom-right    4
            -w, -h, d,    # back, bottom-left     5
            -w, h, d,     # back, top-left        6         Back
            w, h, d,      # back, top-right       7

            w, -h, -d,    # front, bottom-right   8
            w, -h, d,     # back, bottom-right    9
            w, h, d,      # back, top-right      10         Right
            w, h, -d,     # front, top-right     11

            -w, -h, d,    # back, bottom-left    12
            -w, -h, -d,   # front, bottom-left   13
            -w, h, -d,    # front, top-left      14         Left
            -w, h, d,     # back, top-left       15

            -w, h, -d,    # front, top-left      16
            w, h, -d,     # front, top-right     17
            w, h, d,      # back, top-right      18         Top
            -w, h, d,     # back, top-left       19

            -w, -h, d,    # back, bottom-left    20
            w, -h, d,     # back, bottom-right   21
            w, -h, -d,    # front, bottom-right  22         Bottom
            -w, -h, -d,   # front, bottom-left   23
        ]

        normals = [0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1,     # front face
                   0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1,         # back face
                   1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0,         # right face
                   -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0,     # left face
                   0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,         # top face
                   0, -1, 0, 0, -1, 0, 0, -1, 0, 0, -1, 0]     # bottom face

        indices = [23, 22, 20, 22, 21, 20,  # bottom
                   19, 18, 16, 18, 17, 16,  # top
                   15, 14, 12, 14, 13, 12,  # left
                   11, 10, 8, 10, 9, 8,     # right
                   7, 6, 4, 6, 5, 4,        # back
                   3, 2, 0, 2, 1, 0]        # front

        return self._program.vertex_list_indexed(len(vertices) // 3, pyglet.gl.GL_TRIANGLES, indices,
                                                 batch=self._batch, group=self._group,
                                                 POSITION=('f', vertices),
                                                 NORMAL=('f', normals),
                                                 COLOR_0=('f', self._color * (len(vertices) // 3)))
    def deform(self, deformMat):
        self.deformation = deformMat @ self.deformation
        self.matrix = self.movement @ self.deformation

    def move(self, moveMat):
        self.movement = moveMat @ self.movement
        self.matrix = self.movement @ self.deformation


class Box(model.Model):
    def __init__(self, width=1.0, height=1.0, depth=1.0, color=(1.0, 1.0, 1.0, 1.0),
                 material=None, batch=None, group=None, program=None):
        self._width = width
        self._height = height
        self._depth = depth
        self._color = color
        self.deformation = Mat4()
        self.movement = Mat4()

        self._batch = batch
        self._program = program if program else model.get_default_shader()

        # Create a Material and Group for the Model
        self._material = material if material else model.SimpleMaterial(name="cube")
        self._group = pyglet.model.MaterialGroup(material=self._material, program=self._program, parent=group)

        self._vlist = self._create_vertexlist()

        super().__init__([self._vlist], [self._group], self._batch)

    def _create_vertexlist(self):
        w = self._width / 2
        h = self._height / 2
        d = self._depth / 2

        # Inner square offset for top hole
        hw = w / 3
        hd = d / 3

        vertices = [
            # Top face (with center hole)
            -w,  h, -d,   # 0 front-left
            w,  h, -d,   # 1 front-right
            w,  h,  d,   # 2 back-right
            -w,  h,  d,   # 3 back-left

            -hw, h, -hd,  # 4 inner front-left
            hw, h, -hd,  # 5 inner front-right
            hw, h,  hd,  # 6 inner back-right
            -hw, h,  hd,  # 7 inner back-left

            # Back face
            w, -h,  d,   # 8 bottom-right
            -w, -h,  d,   # 9 bottom-left
            -w,  h,  d,   #10 top-left (reuse 3)
            w,  h,  d,   #11 top-right (reuse 2)

            # Right face
            w, -h, -d,   #12 bottom-front
            w, -h,  d,   #13 bottom-back
            w,  h,  d,   #14 top-back (reuse 2)
            w,  h, -d,   #15 top-front (reuse 1)

            # Left face
            -w, -h,  d,   #16 bottom-back
            -w, -h, -d,   #17 bottom-front
            -w,  h, -d,   #18 top-front (reuse 0)
            -w,  h,  d,   #19 top-back (reuse 3)

            # Bottom face
            -w, -h,  d,   #20 back-left
            w, -h,  d,   #21 back-right
            w, -h, -d,   #22 front-right
            -w, -h, -d    #23 front-left
        ]

        # Normals
        normals = [
            # Top face (+y)
            0, 1, 0,  # 0
            0, 1, 0,  # 1
            0, 1, 0,  # 2
            0, 1, 0,  # 3
            0, 1, 0,  # 4
            0, 1, 0,  # 5
            0, 1, 0,  # 6
            0, 1, 0,  # 7

            # Back face (0, 0, 1)
            0, 0, 1,  # 8
            0, 0, 1,  # 9
            0, 0, 1,  #10
            0, 0, 1,  #11

            # Right face (1, 0, 0)
            1, 0, 0,  #12
            1, 0, 0,  #13
            1, 0, 0,  #14
            1, 0, 0,  #15

            # Left face (-1, 0, 0)
            -1, 0, 0, #16
            -1, 0, 0, #17
            -1, 0, 0, #18
            -1, 0, 0, #19

            # Bottom face (0, -1, 0)
            0, -1, 0, #20
            0, -1, 0, #21
            0, -1, 0, #22
            0, -1, 0  #23
        ]

        # Indices
        indices = [
            # Top face with hole (4 quads)
            0, 4, 7,  0, 7, 3,   # Left
            4, 1, 5,  4, 0, 1,   # Front
            5, 2, 6,  5, 1, 2,   # Right
            7, 6, 3,  6, 2, 3,   # Back

            # Back face
            8, 9, 10,  8, 10, 11,

            # Right face
            12, 13, 14,  12, 14, 15,

            # Left face
            16, 17, 18,  16, 18, 19,

            # Bottom face
            20, 21, 22,  20, 22, 23
        ]

        return self._program.vertex_list_indexed(len(vertices) // 3, pyglet.gl.GL_TRIANGLES, indices,
                                                 batch=self._batch, group=self._group,
                                                 POSITION=('f', vertices),
                                                 NORMAL=('f', normals),
                                                 COLOR_0=('f', self._color * (len(vertices) // 3)))

    def deform(self, deformMat):
        self.deformation = deformMat @ self.deformation
        self.matrix = self.movement @ self.deformation

    def move(self, moveMat):
        self.movement = moveMat @ self.movement
        self.matrix = self.movement @ self.deformation

class Sphere(model.Model):

    def __init__(self, radius=1.0, stacks=30, sectors=30, color=(1.0, 1.0, 1.0, 1.0),
                 material=None, batch=None, group=None, program=None):
        self._radius = radius
        self._stacks = stacks
        self._sectors = sectors
        self._color = color
        self.deformation = Mat4()
        self.movement = Mat4()

        self._batch = batch
        self._program = program if program else model.get_default_shader()

        # Create a Material and Group for the Model
        self._material = material if material else model.SimpleMaterial(name="sphere")
        self._group = pyglet.model.MaterialGroup(material=self._material, program=self._program, parent=group)

        self._vlist = self._create_vertexlist()

        super().__init__([self._vlist], [self._group], self._batch)

    def _create_vertexlist(self):
        radius = self._radius / 2
        sectors = self._sectors
        stacks = self._stacks

        vertices = []
        normals = []
        indices = []

        sector_step = 2 * pi / sectors
        stack_step = pi / stacks

        for i in range(stacks + 1):
            stack_angle = pi / 2 - i * stack_step
            for j in range(sectors + 1):
                sector_angle = j * sector_step
                vertices.append(radius * cos(stack_angle) * cos(sector_angle))    # x
                vertices.append(radius * cos(stack_angle) * sin(sector_angle))    # y
                vertices.append(radius * sin(stack_angle))                             # z
                normals.append(cos(stack_angle) * cos(sector_angle))              # x
                normals.append(cos(stack_angle) * sin(sector_angle))              # y
                normals.append(sin(stack_angle))                                       # z

        # Generate indices
        for i in range(stacks):
            for j in range(sectors):
                first = i * (sectors + 1) + j
                second = first + sectors + 1
                indices.extend([first, second, second + 1])
                indices.extend([first, second + 1, first + 1])

        return self._program.vertex_list_indexed(len(vertices) // 3, pyglet.gl.GL_TRIANGLES, indices,
                                                 batch=self._batch, group=self._group,
                                                 POSITION=('f', vertices),
                                                 NORMAL=('f', normals),
                                                 COLOR_0=('f', self._color * (len(vertices) // 3)))
    def deform(self, deformMat):
        self.deformation = deformMat @ self.deformation
        self.matrix = self.movement @ self.deformation

    def move(self, moveMat):
        self.movement = moveMat @ self.movement
        self.matrix = self.movement @ self.deformation


class Cylinder(model.Model):

    def __init__(self, radius=1.0, height=2.0, sectors=30, color=(1.0, 1.0, 1.0, 1.0),
                 material=None, batch=None, group=None, program=None):
        self._radius = radius
        self._height = height
        self._sectors = sectors
        self._color = color
        self.deformation = Mat4()
        self.movement = Mat4()

        self._batch = batch
        self._program = program if program else model.get_default_shader()

        # Create a Material and Group for the Model
        self._material = material if material else model.SimpleMaterial(name="cylinder")
        self._group = pyglet.model.MaterialGroup(material=self._material, program=self._program, parent=group)

        self._vlist = self._create_vertexlist()

        super().__init__([self._vlist], [self._group], self._batch)

    def _create_vertexlist(self):
        radius = self._radius
        height = self._height / 2
        sectors = self._sectors

        vertices = []
        normals = []
        indices = []

        sector_step = 2 * pi / sectors
        
        # Top and bottom circle vertices
        for i in range(2):  # i=0 for bottom, i=1 for top
            z = -height if i == 0 else height
            normal_z = -1 if i == 0 else 1
            for j in range(sectors + 1):
                sector_angle = j * sector_step
                x = radius * cos(sector_angle)
                y = radius * sin(sector_angle)
                vertices.extend([x, y, z])
                normals.extend([0, 0, normal_z])
        
        # Side vertices
        for i in range(2):  # i=0 for bottom, i=1 for top
            z = -height if i == 0 else height
            for j in range(sectors + 1):
                sector_angle = j * sector_step
                x = radius * cos(sector_angle)
                y = radius * sin(sector_angle)
                vertices.extend([x, y, z])
                normals.extend([cos(sector_angle), sin(sector_angle), 0])
        
        # Indices for top and bottom circles
        for j in range(sectors):
            indices.extend([j, j + 1, sectors])  # Bottom circle
            indices.extend([j + sectors + 1, j + sectors + 2, 2 * sectors + 1])  # Top circle
        
        # Indices for side faces
        for j in range(sectors):
            first = 2 * (sectors + 1) + j
            second = first + sectors + 1
            indices.extend([first, second, first + 1])
            indices.extend([second, second + 1, first + 1])

        return self._program.vertex_list_indexed(len(vertices) // 3, pyglet.gl.GL_TRIANGLES, indices,
                                                 batch=self._batch, group=self._group,
                                                 POSITION=('f', vertices),
                                                 NORMAL=('f', normals),
                                                 COLOR_0=('f', self._color * (len(vertices) // 3)))
    
    def deform(self, deformMat):
        self.deformation = deformMat @ self.deformation
        self.matrix = self.movement @ self.deformation

    def move(self, moveMat):
        self.movement = moveMat @ self.movement
        self.matrix = self.movement @ self.deformation