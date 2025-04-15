from scripts import geometry
from pyglet.math import Mat4, Vec3
from math import pi, atan

class CornellScene:
    "this class generate cornell box"
    def __init__(self, batch):
        self.cornellBatch = batch
        self.default_colors = {
            "box": (1.0, 1.0, 1.0, 1.0),
            "kamilcap": (0.27, 0.42, 0.31, 1.0),
            "kamilbottom": (1.0, 1.0, 1.0, 1.0),
            "slidebar": (0.6, 0.6, 0.6, 1.0),
            "cube": (0.2, 0.2, 0.2, 0),
            "light": (0.7, 0.7, 0.7, 1.0)
        }
        self.create_scene()

    def create_scene(self):
        box = geometry.Box(width=15.5, height=16.8, depth=12.5, color=self.default_colors["box"], batch=self.cornellBatch)
        box.deform(Mat4.from_rotation(pi, Vec3(0, 1, 0)))
        box.deform(Mat4.from_translation(Vec3(0, 8.4, 0)))

        kamill_cap = geometry.Cylinder(radius=0.9, height=5.5, sectors=50, color = self.default_colors["kamilcap"], batch=self.cornellBatch)
        kamill_cap.deform(Mat4.from_rotation(-pi/2, Vec3(1, 0, 0)))
        kamill_cap.deform(Mat4.from_translation(Vec3(0, 4.6, 0)))
        kamill_cap.move(Mat4.from_translation(Vec3(3.45, 0, -2)))

        kamill_bottom = geometry.Cylinder(radius=0.9, height= 1.9, sectors=50, color = self.default_colors["kamilbottom"], batch=self.cornellBatch)
        kamill_bottom.deform(Mat4.from_rotation(-pi/2, Vec3(1, 0, 0)))
        kamill_bottom.deform(Mat4.from_translation(Vec3(0, 0.95, 0)))
        kamill_bottom.move(Mat4.from_translation(Vec3(3.45, 0, -2)))

        slidebar = geometry.Cylinder(radius=1, height=3, sectors=50, color = self.default_colors["slidebar"], batch=self.cornellBatch)
        slidebar.deform(Mat4.from_rotation(-pi/2, Vec3(1, 0, 0)))
        slidebar.deform(Mat4.from_translation(Vec3(0, 1.5, 0)))
        slidebar.move(Mat4.from_translation(Vec3(-3.35, 0, 0)))

        cube = geometry.Cube(width=6, height=3.2, depth=5, color=self.default_colors["cube"], batch=self.cornellBatch)
        cube.deform(Mat4.from_translation(Vec3(0, 1.6, 0)))
        cube.move(Mat4.from_rotation(atan(2.5/3), Vec3(0, 1, 0)))
        cube.move(Mat4.from_translation(Vec3(-3.35, 3, 0)))

        light = geometry.Cube(width=4.5, height=1, depth=4.5, color=self.default_colors["light"], batch=self.cornellBatch)
        light.deform(Mat4.from_translation(Vec3(0, 0.5, 0)))
        light.move(Mat4.from_translation(Vec3(0, 16.8, 0)))

    def set_shadings(self):
        pass