from OpenGL.GL import *
from OpenGL.GLU import *

from util import *

import scene
import gui


import wx #import wxWidgets
import wx.propgrid as wxpg

class Box:
	def __init__(self, name, min, max):
		self.name = name
		self.min = min
		self.max = max
		self.selected = False
		
		self.edit = False
		
		self.uniform = False
		self.cast = False
		self.recieve = False
		
		self.type = "Box"
		
		self.transparent = False
		
		self.pointselection = -1
		
		self.pg = None
	def duplicate(self, newname):
		newbox = Box(newname, [self.min[0], self.min[1], self.min[2]], [self.max[0], self.max[1], self.max[2]])
		
		newbox.uniform = self.uniform
		newbox.recieve = self.recieve
		newbox.cast = self.cast
		
		return newbox
	def center(self):
		return mult( 0.5, add(self.min, self.max) )
	def move(self, x, y, z):
		if self.edit:
			if self.pointselection == 1:
				self.min[0] += x
				self.min[1] += y
				self.min[2] += z
			if self.pointselection == 2:
				self.max[0] += x
				self.max[1] += y
				self.max[2] += z
		else:
			self.min[0] += x
			self.max[0] += x
			
			self.min[1] += y
			self.max[1] += y
		
			self.min[2] += z
			self.max[2] += z
		
		if self.pg != None:
			self.pg.GetPropertyByName("Minimum.X").SetValue(self.min[0])
			self.pg.GetPropertyByName("Minimum.Y").SetValue(self.min[1])
			self.pg.GetPropertyByName("Minimum.Z").SetValue(self.min[2])
			
			self.pg.GetPropertyByName("Maximum.X").SetValue(self.max[0])
			self.pg.GetPropertyByName("Maximum.Y").SetValue(self.max[1])
			self.pg.GetPropertyByName("Maximum.Z").SetValue(self.max[2])
	def collide(self, ro, rd):
		return iBox(self.min, self.max, ro, rd)
	def click(self, pos):
		SELECTIONDIST = 30
		
		self.pointselection = -1
		
		modelViewMatrix = glGetDouble( GL_MODELVIEW_MATRIX )
		projectionMatrix = glGetDouble( GL_PROJECTION_MATRIX )
		viewport = glGetInteger(GL_VIEWPORT)
		
		dotpos = gluProject(self.min[0], self.min[1], self.min[2], modelViewMatrix, projectionMatrix, viewport)
		if dist( [dotpos[0], dotpos[1]], [pos[0], 720 - pos[1]] ) < SELECTIONDIST:
			self.pointselection = 1
			
		dotpos = gluProject(self.max[0], self.max[1], self.max[2], modelViewMatrix, projectionMatrix, viewport)
		if dist( [dotpos[0], dotpos[1]], [pos[0], 720 - pos[1]] ) < SELECTIONDIST:
			self.pointselection = 2
	def draw(self):
		glEnable(GL_LIGHTING)
		
		glMaterialfv(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
		
		glBegin(GL_QUADS)
		
		#Front Face
		glNormal3f( 0.0, 0.0, 1.0)
		glVertex3f( self.min[0], self.min[1],  self.max[2] )
		glVertex3f( self.max[0], self.min[1],  self.max[2] )
		glVertex3f( self.max[0], self.max[1],  self.max[2] )
		glVertex3f( self.min[0], self.max[1],  self.max[2] )
		
		#Back Face
		glNormal3f( 0.0, 0.0,-1.0)
		glVertex3f( self.min[0], self.min[1],  self.min[2] )
		glVertex3f( self.min[0], self.max[1],  self.min[2] )
		glVertex3f( self.max[0], self.max[1],  self.min[2] )
		glVertex3f( self.max[0], self.min[1],  self.min[2] )
		
		#Top Face
		glNormal3f( 0.0, 1.0, 0.0)
		glVertex3f( self.min[0], self.max[1],  self.min[2] )
		glVertex3f( self.min[0], self.max[1],  self.max[2] )
		glVertex3f( self.max[0], self.max[1],  self.max[2] )
		glVertex3f( self.max[0], self.max[1],  self.min[2] )
		
		#Bottom Face
		glNormal3f( 0.0,-1.0, 0.0)
		glVertex3f( self.min[0], self.min[1],  self.min[2] )
		glVertex3f( self.max[0], self.min[1],  self.min[2] )
		glVertex3f( self.max[0], self.min[1],  self.max[2] )
		glVertex3f( self.min[0], self.min[1],  self.max[2] )
		
		#Right Face
		glNormal3f( 1.0, 0.0, 0.0)
		glVertex3f( self.max[0], self.min[1],  self.min[2] )
		glVertex3f( self.max[0], self.max[1],  self.min[2] )
		glVertex3f( self.max[0], self.max[1],  self.max[2] )
		glVertex3f( self.max[0], self.min[1],  self.max[2] )
		
		#Left Face
		glNormal3f(-1.0, 0.0, 0.0)
		glVertex3f( self.min[0], self.min[1],  self.min[2] )
		glVertex3f( self.min[0], self.min[1],  self.max[2] )
		glVertex3f( self.min[0], self.max[1],  self.max[2] )
		glVertex3f( self.min[0], self.max[1],  self.min[2] )
		
		glEnd()
		
		glDisable(GL_LIGHTING)
		
		glLineWidth(2)
		
		if self.edit:
			glDisable(GL_DEPTH_TEST)
		
		glBegin(GL_LINES)
		
		if self.edit:
			glColor3f(1, 0.62745, 0.176470)
		elif self.selected:
			glColor3f(0,1,0)
		else:
			glColor3f(1, 1, 1)
			
		glVertex3f(self.min[0], self.min[1],  self.min[2])
		glVertex3f(self.max[0], self.min[1],  self.min[2])
		
		glVertex3f(self.min[0], self.min[1],  self.min[2])
		glVertex3f(self.min[0], self.max[1],  self.min[2])
		
		glVertex3f(self.min[0], self.min[1],  self.min[2])
		glVertex3f(self.min[0], self.min[1],  self.max[2])
		
		glVertex3f(self.max[0], self.max[1],  self.max[2])
		glVertex3f(self.min[0], self.max[1],  self.max[2])
		
		glVertex3f(self.max[0], self.max[1],  self.max[2])
		glVertex3f(self.max[0], self.min[1],  self.max[2])
		
		glVertex3f(self.max[0], self.max[1],  self.max[2])
		glVertex3f(self.max[0], self.max[1],  self.min[2])
		
		glVertex3f(self.min[0], self.max[1],  self.max[2])
		glVertex3f(self.min[0], self.max[1],  self.min[2])
		
		glVertex3f(self.max[0], self.max[1],  self.min[2])
		glVertex3f(self.min[0], self.max[1],  self.min[2])
		
		
		glVertex3f(self.min[0], self.max[1],  self.max[2])
		glVertex3f(self.min[0], self.min[1],  self.max[2])
		
		glVertex3f(self.max[0], self.max[1],  self.min[2])
		glVertex3f(self.max[0], self.min[1],  self.min[2])
		
		glVertex3f(self.max[0], self.min[1],  self.min[2])
		glVertex3f(self.max[0], self.min[1],  self.max[2])
		
		glVertex3f(self.min[0], self.min[1],  self.max[2])
		glVertex3f(self.max[0], self.min[1],  self.max[2])
		
		glEnd()
		
		glLineWidth(1)
		
		if self.edit:
			glPointSize (10)
			glBegin(GL_POINTS)
			
			if self.pointselection == 1:
				glColor3f(0, 1, 0)
			else:
				glColor3f(1, 1, 1)
			glVertex3f(self.min[0], self.min[1],  self.min[2])
			
			if self.pointselection == 2:
				glColor3f(0, 1, 0)
			else:
				glColor3f(1, 1, 1)
				
			glVertex3f(self.max[0], self.max[1],  self.max[2])
			
			glEnd()
			glPointSize (1)
			
			if self.pointselection == 1:
				movetool(self.min[0], self.min[1],  self.min[2], 5)
			if self.pointselection == 2:
				movetool(self.max[0], self.max[1],  self.max[2], 5)
				
		glEnable(GL_LIGHTING)
		
		glEnable(GL_DEPTH_TEST)
	def PropertyChange(self, event):
		p = event.GetProperty()
		if p:
			print p.GetName() + " changed."
			
			#General Properties
			if p.GetName() == "Object Name":
				del scene.objects[self.name]
				self.name = p.GetValue()
				scene.objects[self.name] = self
				gui.tree_ctrl.SetItemText(self.treeitem, self.name)
			if p.GetName() == "Uniform":
				self.uniform = p.GetValue()
				
			if p.GetName() == "Minimum.X":
				self.min[0] = p.GetValue()
			if p.GetName() == "Minimum.Y":
				self.min[1] = p.GetValue()
			if p.GetName() == "Minimum.Z":
				self.min[2] = p.GetValue()
				
			if p.GetName() == "Maximum.X":
				self.max[0] = p.GetValue()
			if p.GetName() == "Maximum.Y":
				self.max[1] = p.GetValue()
			if p.GetName() == "Maximum.Z":
				self.max[2] = p.GetValue()
				
			if p.GetName() == "Cast Shadows":
				self.cast = p.GetValue()
			if p.GetName() == "Recieve Shadows":
				self.recieve = p.GetValue()
	def populatepropgrid(self, pg):
		#Geometry Properties
		pg.Append( wxpg.PropertyCategory("Geometry") )
		
		minID = pg.Append( wxpg.StringProperty("Minimum", value="<composed>") )
		pg.AppendIn (minID, wxpg.FloatProperty("X", value=self.min[0]) )
		pg.AppendIn (minID, wxpg.FloatProperty("Y", value=self.min[1]) )
		pg.AppendIn (minID, wxpg.FloatProperty("Z", value=self.min[2]) )
		
		maxID = pg.Append( wxpg.StringProperty("Maximum", value="<composed>") )
		pg.AppendIn (maxID, wxpg.FloatProperty("X", value=self.max[0]) )
		pg.AppendIn (maxID, wxpg.FloatProperty("Y", value=self.max[1]) )
		pg.AppendIn (maxID, wxpg.FloatProperty("Z", value=self.max[2]) )
		
		#Material Properties
		pg.Append( wxpg.PropertyCategory("Material") )
		
		pg.Append( wxpg.BoolProperty("Cast Shadows",value=self.cast) )
		pg.SetPropertyAttribute("Cast Shadows", "UseCheckbox", True)
		
	def write(self, object):
		object.setAttribute("min", formatString(self.min) )
		object.setAttribute("max", formatString(self.max) )
		
		object.setAttribute("recieve", str(self.recieve) )
		object.setAttribute("cast", str(self.cast) )