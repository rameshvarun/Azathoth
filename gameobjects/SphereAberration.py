from OpenGL.GL import *
from OpenGL.GLU import *

from util import *

import gui
import scene

import wx #import wxWidgets
import wx.propgrid as wxpg

from gameobject import GameObject

class SphereAberration ( GameObject ):
	def __init__(self, name = None, x = 1, y = 1, z = 1, r = 1):
		self.name = name
		self.x = x
		self.y = y
		self.z = z
		
		self.r = r
		
		self.reflectivity = 0.0
		
		self.type = "SphereAberration"
		
		self.scale = [1.0, 1.0, 1.0]
		
		self.pointselection = -1
		
		GameObject.__init__(self)
	
	@staticmethod
	def create(event):
		SphereAberration()
		
	@staticmethod
	def load(element):
		name = element.getAttribute("name")
		
		newobject = SphereAberration(name, float(element.getAttribute("x")) , float(element.getAttribute("y")) , float(element.getAttribute("z")) , float(element.getAttribute("r")) )
		newobject.selected = (element.getAttribute("selected") == "True")
		
		newobject.uniform = (element.getAttribute("uniform") == "True")
		
		newobject.reflectivity = float(element.getAttribute("reflectivity"))
		newobject.recieve = (element.getAttribute("recieve") == "True")
		newobject.cast = (element.getAttribute("cast") == "True")
		
		newobject.scale = toFloats( element.getAttribute("scale").split(",") )
	
		return newobject
		
	def duplicate(self, newname):
		newsphere = SphereAberration(newname, self.x, self.y, self.z, self.r)
		
		newsphere.uniform = self.uniform
		newsphere.recieve = self.recieve
		newsphere.cast = self.cast
		
		newsphere.reflectivity = self.reflectivity
		
		newsphere.scale = list( self.scale )
		
		return newsphere
	def center(self):
		return [self.x, self.y, self.z]
	def move(self, x, y, z):
		if self.edit:
			if self.pointselection == 1:
				self.x += x
				self.y += y
				self.z += z
			if self.pointselection == 2:
				self.r += x
		else:
			self.x += x
			self.y += y
			self.z += z
		
		if self.pg != None:
			self.pg.GetPropertyByName("Center.X").SetValue(self.x)
			self.pg.GetPropertyByName("Center.Y").SetValue(self.y)
			self.pg.GetPropertyByName("Center.Z").SetValue(self.z)
			
			self.pg.GetPropertyByName("Radius").SetValue(self.r)
		
	def collide(self, ro, rd):
		return iSphere(self.x, self.y, self.z, self.r, ro, rd)
	def click(self, pos):
		SELECTIONDIST = 20
		
		self.pointselection = -1
		
		modelViewMatrix = glGetDouble( GL_MODELVIEW_MATRIX )
		projectionMatrix = glGetDouble( GL_PROJECTION_MATRIX )
		viewport = glGetInteger(GL_VIEWPORT)
		
		dotpos = gluProject(self.x , self.y, self.z, modelViewMatrix, projectionMatrix, viewport)
		if dist( [dotpos[0], dotpos[1]], [pos[0], 720 - pos[1]] ) < SELECTIONDIST:
			self.pointselection = 1
			
		dotpos = gluProject(self.x + self.r, self.y, self.z, modelViewMatrix, projectionMatrix, viewport)
		if dist( [dotpos[0], dotpos[1]], [pos[0], 720 - pos[1]] ) < SELECTIONDIST:
			self.pointselection = 2
	def draw(self):
		glEnable(GL_LIGHTING)
		
		glMaterialfv(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 0.5))
		
		
		
		glPushMatrix()
		glTranslatef(self.x, self.y, self.z)
		q = gluNewQuadric()
		gluSphere( q, self.r, 10, 10 )
		glPopMatrix()
		
		glDisable(GL_LIGHTING)
		
		glLineWidth(2)
		
		glBegin(GL_LINES)
		
		self.min = [self.x - self.r,self.y - self.r,self.z - self.r]
		self.max = [self.x + self.r,self.y + self.r,self.z + self.r]
		
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
			glDisable(GL_DEPTH_TEST)
			
			glPointSize (10)
			glBegin(GL_POINTS)
			
			if self.pointselection == 1:
				glColor3f(0, 1, 0)
			else:
				glColor3f(1, 1, 1)
			glVertex3f(self.x, self.y, self.z)
			
			if self.pointselection == 2:
				glColor3f(0, 1, 0)
			else:
				glColor3f(1, 1, 1)
				
			glVertex3f(self.x + self.r, self.y, self.z)
			
			glEnd()
			glPointSize (1)
			
			if self.pointselection == 1:
				movetool(self.x, self.y, self.z, 5)
			if self.pointselection == 2:
				movetool(self.x + self.r, self.y, self.z, 5)
				
			glEnable(GL_DEPTH_TEST)
		
		glEnable(GL_LIGHTING)
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
			
			#Aberration Properties
			if p.GetName() == "Scale.X":
				self.scale[0] = p.GetValue()
			if p.GetName() == "Scale.Y":
				self.scale[1] = p.GetValue()
			if p.GetName() == "Scale.Z":
				self.scale[2] = p.GetValue()
				
			#Geometry Properties
			if p.GetName() == "Center.X":
				self.x = p.GetValue()
			if p.GetName() == "Center.Y":
				self.y = p.GetValue()
			if p.GetName() == "Center.Z":
				self.z = p.GetValue()
				
			if p.GetName() == "Radius":
				self.r = p.GetValue()
				
			#Material Properties
			if p.GetName() == "Reflectivity":
				self.reflectivity = p.GetValue()
			if p.GetName() == "Cast Shadows":
				self.cast = p.GetValue()
			if p.GetName() == "Recieve Shadows":
				self.recieve = p.GetValue()
	def populatepropgrid(self, pg):
		#Geometry Properties
		pg.Append( wxpg.PropertyCategory("Geometry") )
		
		normalID = pg.Append( wxpg.StringProperty("Center", value="<composed>") )
		pg.AppendIn (normalID, wxpg.FloatProperty("X", value=self.x) )
		pg.AppendIn (normalID, wxpg.FloatProperty("Y", value=self.y) )
		pg.AppendIn (normalID, wxpg.FloatProperty("Z", value=self.z) )
		
		pg.Append( wxpg.FloatProperty("Radius", value=self.r) )
		
		#Aberration Properties
		pg.Append( wxpg.PropertyCategory("Aberration") )
		abID = pg.Append( wxpg.StringProperty("Scale", value="<composed>") )
		pg.AppendIn (abID, wxpg.FloatProperty("X", value=self.scale[0]) )
		pg.AppendIn (abID, wxpg.FloatProperty("Y", value=self.scale[1]) )
		pg.AppendIn (abID, wxpg.FloatProperty("Z", value=self.scale[2]) )
		
		#Material Properties
		pg.Append( wxpg.PropertyCategory("Material") )
		pg.Append( wxpg.FloatProperty("Reflectivity", value=self.reflectivity) )
		
		pg.Append( wxpg.BoolProperty("Cast Shadows",value=self.cast) )
		pg.SetPropertyAttribute("Cast Shadows", "UseCheckbox", True)
		
		pg.Append( wxpg.BoolProperty("Recieve Shadows",value=self.recieve) )
		pg.SetPropertyAttribute("Recieve Shadows", "UseCheckbox", True)
	def write(self, object):
		object.setAttribute("x", str(self.x) )
		object.setAttribute("y", str(self.y) )
		object.setAttribute("z", str(self.z) )
		object.setAttribute("r", str(self.r) )
		
		object.setAttribute("reflectivity", str(self.reflectivity) )
		object.setAttribute("recieve", str(self.recieve) )
		object.setAttribute("cast", str(self.cast) )
		
		object.setAttribute("scale", formatString(self.scale) )