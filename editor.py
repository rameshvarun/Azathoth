#These lines below have to do with the exporting to an exe process
from ctypes import util
try:
    from OpenGL.platform import win32
except AttributeError:
    pass
#import pygame._view
	
from math import *

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

from camera import *

import gameobjects

import gui

import threading

from util import *

import scene

import os



DEFAULTSCREENSIZE = (1280,720)

#Properties of the Light
LightAmbient = ( 0.0, 0.0, 0.0, 1.0 )
LightDiffuse = ( 0.8, 0.8, 0.8, 1.0 )
LightSpecular = ( 0.2, 0.2, 0.2, 1.0)
LightPosition = ( 1.0, 1.0, 1.0, 0.0 )

#Called automatically when the screen has been resized
def resize(size):
	width = size[0]
	height = size[1]
	
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(60.0, float(width)/height, .1, 1000.)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

#Draws an axis (used in the center)
def axes():
	glDisable(GL_LIGHTING)
	glBegin(GL_LINES)
	
	#Y axis
	glColor3f(0,255,0)
	glVertex3f(0,0,0)
	glColor3f(0,255,0)
	glVertex3f(0,10,0)
	
	#Z axis
	glColor3f(0,0,255)
	glVertex3f(0,0,0)
	glColor3f(0,0,255)
	glVertex3f(0,0,10)
	
	#X axis
	glColor3f(255,0,0)
	glVertex3f(0,0,0)
	glColor3f(255,0,0)
	glVertex3f(10,0,0)
	
	glEnd()
	
	drawText3d((0,10, 0), "y", 32)
	drawText3d((10,0, 0), "x", 32)
	drawText3d((0,0, 10), "z", 32)
	
	glEnable(GL_LIGHTING)
	

			
def main():
	
	pygame.init() #Startup pygame
	
	font = pygame.font.Font (None, 10) #Create the font object that will be used to draw things

	screen = pygame.display.set_mode(DEFAULTSCREENSIZE, HWSURFACE|OPENGL|DOUBLEBUF)

	resize(DEFAULTSCREENSIZE)

	glEnable(GL_DEPTH_TEST)
	
	glShadeModel(GL_SMOOTH) #Smooth shading
	
	#Create one main light
	glLightfv(GL_LIGHT1, GL_DIFFUSE, LightDiffuse)
	glLightfv(GL_LIGHT1, GL_POSITION,LightPosition)
	glEnable(GL_LIGHT1)
	
	glEnable(GL_LIGHTING) #Enable lighting
	
	glClearColor(0, 0, 0, 0.0)
	glEnable (GL_BLEND);
	glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

	glEnable(GL_CULL_FACE);

	clock = pygame.time.Clock() #Clock object for calculating a dt
	
	running = True #When this is set to false, the main loop will no longer repeat
	
	mousedown = [0, 0] #What position was the mouse at when the left click is first pressed
	mousecolor = None #What color was under the mouse when the left click is first pressed
	
	
	center = [0,0,0] #Value for storing the center of the current selection of objects (Averages the individual center of the objects in the selection)
	#This is important because it is where the move tool is drawn
	
	#Quick set of utilities for handling the edit mode
	def isEdit(): #Are we in edit mode? Basically checks to see if any object has its edit value set to True
		for obj in scene.objects.values():
			if obj.edit:
				return True
		return False
	def getEdit(): #What object is currently being edited
		for obj in scene.objects.values():
			if obj.edit:
				return obj
		return None
	def endEdit(): #End edit mode - basically set every single objects edit value to false
		for obj in scene.objects.values():
			obj.edit = False
	
	#Main loop
	while running:
		gui.update() #Update gui system - handle event polling
		
		#Process all pygame events
		for event in pygame.event.get():
			keys = pygame.key.get_pressed()
			
			#Quitting
			if event.type == QUIT:
				running = False
				
			if event.type == KEYUP:
				if event.key == K_ESCAPE:
					running = False
				
				#Handle deleting of objects from scene
				if event.key == K_DELETE and not isEdit(): #Can't delete objects in edit mode
					for obj in scene.objects.values():
						if obj.selected:
							gui.tree_ctrl.Delete(obj.treeitem)
							del objects[obj.name]
			
				#Hitting space duplicates the current selection
				if event.key == K_SPACE and not isEdit(): #Can't duplicate objects in edit mode
					for obj in scene.objects.values():
						if obj.selected:
							newobj = obj.duplicate( None )
			
				#The e key enables edit mode
				if event.key == K_e:
					if isEdit():
						endEdit()
					else:
						for obj in scene.objects.values():
							if obj.selected:
								obj.edit = True
								break
					print getEdit()
				
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 4:
					cam.speed *= 1.1
				if event.button == 5:
					cam.speed *= 0.9
				if event.button == 1:
					mousedown = event.pos
					
					data = glReadPixels( 0,0, DEFAULTSCREENSIZE[0], DEFAULTSCREENSIZE[1], GL_RGB, GL_UNSIGNED_BYTE)
					surface = pygame.image.fromstring(str(buffer(data)), DEFAULTSCREENSIZE, 'RGB', True)
					mousecolor = surface.get_at( (event.pos[0], event.pos[1]) )
			if event.type == MOUSEMOTION:
				relx = -event.rel[0]*0.002*dist( center, [cam.x, cam.y, cam.z] )
				rely = event.rel[1]*0.002*dist( center, [cam.x, cam.y, cam.z] )
				
				modelViewMatrix = glGetDouble( GL_MODELVIEW_MATRIX )
				projectionMatrix = glGetDouble( GL_PROJECTION_MATRIX )
				viewport = glGetInteger(GL_VIEWPORT)
				
				if event.buttons[0]:
					if dist(mousedown, event.pos) > 5:
						if mousecolor == (0,255,0,255):
							v = subtract( gluProject(center[0], center[1], center[2], modelViewMatrix, projectionMatrix, viewport), gluProject(center[0], center[1] + 10, center[2], modelViewMatrix, projectionMatrix, viewport) )
							v = norm(v)
							
							move = dot( [ v[0], v[1] ], [relx, rely] )
							for obj in scene.objects.values():
								if obj.selected == True:
									obj.move( 0, move, 0 )
									
						if mousecolor == (255,0,0,255):
							v = subtract( gluProject(center[0], center[1], center[2], modelViewMatrix, projectionMatrix, viewport), gluProject(center[0] + 10, center[1], center[2], modelViewMatrix, projectionMatrix, viewport) )
							v = norm(v)
							
							move = dot( [ v[0], v[1] ], [relx, rely] )
							for obj in scene.objects.values():
								if obj.selected == True:
									obj.move( move, 0, 0 )
						if mousecolor == (0,0,255,255):
							v = subtract( gluProject(center[0], center[1], center[2], modelViewMatrix, projectionMatrix, viewport), gluProject(center[0], center[1], center[2] + 10, modelViewMatrix, projectionMatrix, viewport) )
							v = norm(v)
							
							move = dot( [ v[0], v[1] ], [relx, rely] )
							for obj in scene.objects.values():
								if obj.selected == True:
									obj.move(0, 0, move)
			if event.type == MOUSEBUTTONUP:
				if event.button == 1:
					if dist(mousedown, event.pos) < 5:
						if not isEdit(): #You cant select other objects in edit mode
							if keys[K_LSHIFT]:
								pass
							else:
								for obj in scene.objects.values():
									obj.selected = False
								gui.tree_ctrl.UnselectAll()
						
							modelViewMatrix = glGetDouble( GL_MODELVIEW_MATRIX )
							projectionMatrix = glGetDouble( GL_PROJECTION_MATRIX )
							viewport = glGetInteger(GL_VIEWPORT)
							
							ro = gluUnProject( event.pos[0] , DEFAULTSCREENSIZE[1] -  event.pos[1], 0.0, modelViewMatrix, projectionMatrix, viewport )
							re = gluUnProject( event.pos[0] , DEFAULTSCREENSIZE[1] - event.pos[1], 1.0, modelViewMatrix, projectionMatrix, viewport )
							rd = norm( [re[0] - ro[0], re[1] - ro[1], re[2] - ro[2] ] )
							
							cam.ro = ro
							cam.rd = rd
							
							selected = None
							
							tm = 10000.0
							t = tm
							for obj in scene.objects.values():
								result, t = obj.collide(ro, rd)
								if result and t  < tm:
									tm = t
									selected = obj
								
							if selected != None:
								selected.selected = not selected.selected
								gui.tree_ctrl.ToggleItemSelection(selected.treeitem)
								
								selection = ""
								for obj in scene.objects.values():
									if obj.selected == True:
										selection += obj.name
										selection += " "
						else:
							getEdit().click(event.pos)

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		time_passed = clock.tick()
		dt = time_passed / 1000.0
		
		cam.update(dt)
		
		keys =  pygame.key.get_pressed()
		

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		cam.render()
		
		axes()
		
		selection = []
		center = [0, 0, 0]
		for obj in scene.objects.values():
			if obj != getEdit() and obj.transparent == False:
				obj.draw()
			
			if obj.selected == True:
				selection.append(obj)
				
		for obj in scene.objects.values():
			if obj != getEdit() and obj.transparent == True:
				obj.draw()
				
		#Make sure that the current object being edited is drawn last
		if isEdit():
			getEdit().draw()
				
		for obj in selection:
			center = add( center, obj.center() )
			
		
		if len(selection) > 0:
			center = mult( 1/float(len(selection)) , center)
			
			distance = dist( center, [cam.x, cam.y, cam.z] )
			
			if not isEdit(): #Don't draw move tool in edit mode
				movetool(center[0] , center[1], center[2], distance*0.3)
		
		
		drawText2d ( (0,720-25), "Camera Speed = " + str(cam.speed) , 30)
		

		pygame.display.flip()
		
	pygame.quit()

gui.initialize()
scene.initialize()


main() #Start the main code block
os._exit(0) #Once that loop is done, for both threads to close