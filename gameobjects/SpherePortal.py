from OpenGL.GL import *
from OpenGL.GLU import *

from util import *

import gui
import scene

import wx #import wxWidgets
import wx.propgrid as wxpg

from gameobject import GameObject

class SpherePortal ( GameObject ):
	def __init__(self, name = None, x = 1, y = 1, z = 1, r = 1):
		self.name = name
		self.x = x
		self.y = y
		self.z = z
		

		self.x2 = x+r*4
		self.y2 = y
		self.z2 = z
		
		self.r = r
		
		self.reflectivity = 0.0
		
		self.type = "SpherePortal"
		
		self.pointselection = -1
		
		GameObject.__init__(self)
		
	@staticmethod
	def create(event):
		SpherePortal()
		
	@staticmethod
	def load(element):
		name = element.getAttribute("name")
		
		newobject = SpherePortal(name, float( element.getAttribute("x")) , float(element.getAttribute("y")) , float(element.getAttribute("z")) , float(element.getAttribute("r")) )
		
		newobject.x2 = float(element.getAttribute("x2"))
		newobject.y2 = float(element.getAttribute("y2"))
		newobject.z2 = float(element.getAttribute("z2"))
		
		newobject.selected = (element.getAttribute("selected") == "True")
		
		newobject.uniform = (element.getAttribute("uniform") == "True")
		
		newobject.reflectivity = float(element.getAttribute("reflectivity"))
		newobject.recieve = (element.getAttribute("recieve") == "True")
		newobject.cast = (element.getAttribute("cast") == "True")
	
		return newobject
		
	def duplicate(self, newname):
		newsphere = SpherePortal(newname, self.x, self.y, self.z, self.r)
		
		newsphere.uniform = self.uniform
		newsphere.recieve = self.recieve
		newsphere.cast = self.cast
		
		newsphere.x2 = self.x2
		newsphere.y2 = self.y2
		newsphere.z2 = self.z2
		
		newsphere.reflectivity = self.reflectivity
		
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
			if self.pointselection == 3:
				self.x2 += x
				self.y2 += y
				self.z2 += z
			if self.pointselection == 4:
				self.r += x
		else:
			self.x += x
			self.y += y
			self.z += z
			
			self.x2 += x
			self.y2 += y
			self.z2 += z
		
		if self.pg != None:
			self.pg.GetPropertyByName("Center.X").SetValue(self.x)
			self.pg.GetPropertyByName("Center.Y").SetValue(self.y)
			self.pg.GetPropertyByName("Center.Z").SetValue(self.z)
			
			self.pg.GetPropertyByName("Center2.X").SetValue(self.x2)
			self.pg.GetPropertyByName("Center2.Y").SetValue(self.y2)
			self.pg.GetPropertyByName("Center2.Z").SetValue(self.z2)
			
			self.pg.GetPropertyByName("Radius").SetValue(self.r)
		
	def collide(self, ro, rd):
		result1 = iSphere(self.x, self.y, self.z, self.r, ro, rd)
		result2 = iSphere(self.x2, self.y2, self.z2, self.r, ro, rd)
		
		if result1[0]:
			return result1
		else:
			return result2
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
			
		dotpos = gluProject(self.x2 , self.y2, self.z2, modelViewMatrix, projectionMatrix, viewport)
		if dist( [dotpos[0], dotpos[1]], [pos[0], 720 - pos[1]] ) < SELECTIONDIST:
			self.pointselection = 3
			
		dotpos = gluProject(self.x2 + self.r, self.y2, self.z2, modelViewMatrix, projectionMatrix, viewport)
		if dist( [dotpos[0], dotpos[1]], [pos[0], 720 - pos[1]] ) < SELECTIONDIST:
			self.pointselection = 4
	def draw(self):
		glEnable(GL_LIGHTING)
		
		glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.0, 0.0, 1.0, 1.0))
		
		
		
		glPushMatrix()
		glTranslatef(self.x, self.y, self.z)
		q = gluNewQuadric()
		gluSphere( q, self.r, 10, 10 )
		glPopMatrix()
		
		glPushMatrix()
		glTranslatef(self.x2, self.y2, self.z2)
		q = gluNewQuadric()
		gluSphere( q, self.r, 10, 10 )
		glPopMatrix()
		
		glDisable(GL_LIGHTING)
		
		glLineWidth(2)
		
		glBegin(GL_LINES)
		
		#Set bounding box color
		if self.edit:
			glColor3f(1, 0.62745, 0.176470)
		elif self.selected:
			glColor3f(0,1,0)
		else:
			glColor3f(1, 1, 1)
		
		#Draw box around first sphere
		self.min = [self.x - self.r,self.y - self.r,self.z - self.r]
		self.max = [self.x + self.r,self.y + self.r,self.z + self.r]
		
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
		
		#Draw box around second sphere
		self.min = [self.x2 - self.r,self.y2 - self.r,self.z2 - self.r]
		self.max = [self.x2 + self.r,self.y2 + self.r,self.z2 + self.r]
		
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
			
			if self.pointselection == 3:
				glColor3f(0, 1, 0)
			else:
				glColor3f(1, 1, 1)
			glVertex3f(self.x2, self.y2, self.z2)
			
			if self.pointselection == 4:
				glColor3f(0, 1, 0)
			else:
				glColor3f(1, 1, 1)
			glVertex3f(self.x2 + self.r, self.y2, self.z2)
			
			glEnd()
			glPointSize (1)
			
			if self.pointselection == 1:
				movetool(self.x, self.y, self.z, 5)
			if self.pointselection == 2:
				movetool(self.x + self.r, self.y, self.z, 5)
			if self.pointselection == 3:
				movetool(self.x2, self.y2, self.z2, 5)
			if self.pointselection == 4:
				movetool(self.x2 + self.r, self.y2, self.z2, 5)
				
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
				
			if p.GetName() == "Center.X":
				self.x = p.GetValue()
			if p.GetName() == "Center.Y":
				self.y = p.GetValue()
			if p.GetName() == "Center.Z":
				self.z = p.GetValue()
				
			if p.GetName() == "Center2.X":
				self.x2 = p.GetValue()
			if p.GetName() == "Center2.Y":
				self.y2 = p.GetValue()
			if p.GetName() == "Center2.Z":
				self.z2 = p.GetValue()
				
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
		
		normalID2 = pg.Append( wxpg.StringProperty("Center2", value="<composed>") )
		pg.AppendIn (normalID2, wxpg.FloatProperty("X", value=self.x2) )
		pg.AppendIn (normalID2, wxpg.FloatProperty("Y", value=self.y2) )
		pg.AppendIn (normalID2, wxpg.FloatProperty("Z", value=self.z2) )
		
		pg.Append( wxpg.FloatProperty("Radius", value=self.r) )
		
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
		
		object.setAttribute("x2", str(self.x2) )
		object.setAttribute("y2", str(self.y2) )
		object.setAttribute("z2", str(self.z2) )
		
		object.setAttribute("r", str(self.r) )
		
		object.setAttribute("reflectivity", str(self.reflectivity) )
		object.setAttribute("recieve", str(self.recieve) )
		object.setAttribute("cast", str(self.cast) )