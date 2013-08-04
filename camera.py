from math import *

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

class Camera:
	def __init__(self):
		self.speed = 1
		self.theta = 1.24
		self.phi = 0.75
		
		self.old = False
		self.downX = 0
		self.downY = 0
		
		self.oldTheta = 0
		self.oldPhi = 0
		
		self.lookX = 0
		self.lookY = 0
		self.lookZ = 0

		
		self.x = 0
		self.y = 0
		self.z = 0
		
		self.ro = [0,0,0]
		self.rd = [0,0,0]
		
	def render(self):
		gluLookAt(self.x, self.y, self.z, self.x + self.lookX, self.y + self.lookY, self.z + self.lookZ, 0, 1, 0)
		
		
		glDisable(GL_LIGHTING)
		glBegin(GL_LINES)
		
		glColor3f(0,255,0)
		glVertex3f(self.ro[0], self.ro[1], self.ro[2])
		glVertex3f(self.ro[0] + self.rd[0]*50, self.ro[1]+self.rd[1]*50, self.ro[2]+self.rd[2]*50)
		
		glEnd()
		
		glEnable(GL_LIGHTING)
	def update(self, dt):
		keys = pygame.key.get_pressed()
	
		if pygame.mouse.get_pressed()[2] == True and self.old == False:
			self.downX = pygame.mouse.get_pos()[0]
			self.downY = pygame.mouse.get_pos()[1]
			
			self.oldTheta = self.theta
			self.oldPhi = self.phi
			
		self.old = pygame.mouse.get_pressed()[2]
		
		
			
		if pygame.mouse.get_pressed()[2]:
			self.currX = pygame.mouse.get_pos()[0]
			self.currY = pygame.mouse.get_pos()[1]
			
			self.theta = self.oldTheta + float(self.currY - self.downY)/100
			self.phi = self.oldPhi + float(self.currX - self.downX)/100
			
			if self.theta < 0.5:
				self.theta = 0.5
			if self.theta > 3.14:
				self.theta = 3.14
				
			if keys[K_w]:
				self.x += sin(self.theta)*cos(self.phi)*self.speed
				self.y += cos(self.theta)*self.speed
				self.z += sin(self.theta)*sin(self.phi)*self.speed
			if keys[K_s]:
				self.x -= sin(self.theta)*cos(self.phi)*self.speed
				self.y -= cos(self.theta)*self.speed
				self.z -= sin(self.theta)*sin(self.phi)*self.speed
			if keys[K_d]:
				self.x += sin(self.theta)*cos(self.phi + 3.14/2)*self.speed
				self.z += sin(self.theta)*sin(self.phi + 3.14/2)*self.speed
			if keys[K_a]:
				self.x -= sin(self.theta)*cos(self.phi + 3.14/2)*self.speed
				self.z -= sin(self.theta)*sin(self.phi + 3.14/2)*self.speed
			if keys[K_e]:
				self.y += self.speed
			if keys[K_q]:
				self.y -= self.speed
			
		self.lookX = sin(self.theta)*cos(self.phi)
		self.lookY = cos(self.theta)
		self.lookZ = sin(self.theta)*sin(self.phi)
		
cam = Camera()