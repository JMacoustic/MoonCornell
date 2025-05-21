# Source: https://github.com/SNU-IntelligentMotionLab/SNU_ComputerGraphics_/blob/main/main.py
# This script is based on above repository and adjusted for additional functionalities

import pyglet
from scripts import camera
from scripts.cornell import CornellScene
from pyglet.gl import *
from customshader import customShader
from pyglet.math import Vec3, Vec4, Mat4
from scripts import geometry

width  = 810
height = 1440

window = pyglet.window.Window(width, height, resizable=True, caption="Moon Cornell Box")
cornellBatch = pyglet.graphics.Batch()
shader = customShader(batch=cornellBatch)
customprogram = shader.program
basicprogram = pyglet.graphics.get_default_shader()


@window.event
def on_resize(width, height):
    camera.resize( window, width, height )
    return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
	window.clear()
	camera.apply(window)
	customprogram.use()
	customprogram['lightPos'] = Vec3(0, 16.8, 0.0)
	customprogram['lightColor'] = Vec3(1.0, 1.0, 1.0)
	customprogram['projection'] = window.projection

	identity = Mat4()
	customprogram['model'] = identity

	cornellBatch.draw()

@window.event
def on_key_press( key, mods ):	
	if key==pyglet.window.key._1:
		camera.curquat=camera.init_quat

	if key==pyglet.window.key.Q:
		pyglet.app.exit()
	
	if key==pyglet.window.key.UP:
		camera.ty -= 1
	
	if key==pyglet.window.key.DOWN:
		camera.ty += 1
	
@window.event
def on_mouse_release( x, y, button, mods ):
	global mouseRotatePressed, mouseMovePressed, mouseDollyPressed
	mouseMovePressed   = False
	mouseRotatePressed = False
	mouseDollyPressed   = False

@window.event
def on_mouse_press( x, y, button, mods ):
	global mouseRotatePressed, mouseMovePressed, mouseDollyPressed

	if button & pyglet.window.mouse.LEFT and mods & pyglet.window.key.MOD_SHIFT:
		mouseMovePressed   = True
		mouseRotatePressed = False
		mouseDollyPressed   = False
	elif button & pyglet.window.mouse.LEFT and mods & pyglet.window.key.MOD_CTRL:
		mouseMovePressed   = False
		mouseRotatePressed = False
		mouseDollyPressed   = True
	elif button & pyglet.window.mouse.LEFT:
		camera.beginRotate(x, y)
		mouseMovePressed   = False
		mouseRotatePressed = True
		mouseDollyPressed   = False

@window.event
def on_mouse_drag(x, y, dx, dy, button, mods ):	
	if mouseRotatePressed:
		camera.rotate(x, y)
	elif mouseMovePressed:
		camera.move(dx/width, dy/height, 0.0)
	elif mouseDollyPressed:
		camera.zoom(dy/height)

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    camera.zoom(z=-scroll_y*0.1)  # Use scroll_y for zooming


def update(dt):
	customprogram['viewPos'] = camera.get_camera_position()
	customprogram['view'] = window.view


moonCornell = CornellScene(cornellBatch, program=customprogram)

# vlist = customprogram.vertex_list_indexed(24, GL_TRIANGLES, moonCornell.cube.indices, cornellBatch, None,
#     position=('f', moonCornell.cube.vertices), normal=('f', moonCornell.cube.normals))

pyglet.clock.schedule_interval(update, 1/60)
glClearColor(0.0, 0.0, 0.0, 1.0)
glEnable(GL_DEPTH_TEST)
glClearDepth(1.0)
glDepthFunc(GL_LESS)

camera.resize( window, width, height )	
pyglet.app.run()