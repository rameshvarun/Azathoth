from OpenGL.GL import *
from OpenGL.GLU import *

from util import *

import gui
import scene

import wx #import wxWidgets
import wx.propgrid as wxpg

from gameobject import GameObject

class Point ( GameObject ):
	def __init__(self, name = None, x = 1, y = 1, z = 1):
		self.name = name
		self.x = x
		self.y = y
		self.z = z
		
		self.type = "Point"
		
		self.pointselection = -1
		
		self.r = 1
		
		GameObject.__init__(self)
		
	@staticmethod
	def create(event):
		Point()
		
	@staticmethod
	def load(element):
		name = element.getAttribute("name")
		
		newobject = Point(name, float( element.getAttribute("x")) , float(element.getAttribute("y")) , float(element.getAttribute("z")) )
		
		newobject.uniform = (element.getAttribute("uniform") == "True")
	
		return newobject
		
	def duplicate(self, newname):
		newsphere = Point(newname, self.x, self.y, self.z)
		
		newsphere.uniform = self.uniform
		
		return newsphere
		
	def center(self):
		return [self.x, self.y, self.z]
		
	def move(self, x, y, z):
		self.x += x
		self.y += y
		self.z += z
		
		if self.pg != None:
			self.pg.GetPropertyByName("Position.X").SetValue(self.x)
			self.pg.GetPropertyByName("Position.Y").SetValue(self.y)
			self.pg.GetPropertyByName("Position.Z").SetValue(self.z)
		
	def collide(self, ro, rd):
		return iSphere(self.x, self.y, self.z, self.r, ro, rd)
		
	#This has no edit mode
	def click(self, pos):
		pass
		
	def draw(self):
		glDisable(GL_LIGHTING)
		
		glLineWidth(2)
		
		glBegin(GL_LINES)
		
		#Y axis
		glColor3f(255,255,255)
		
		glVertex3f(self.x, self.y - self.r, self.z)
		glVertex3f(self.x, self.y + self.r, self.z)
		
		#Z axis
		glVertex3f(self.x, self.y, self.z - self.r)
		glVertex3f(self.x, self.y, self.z + self.r)
		
		#X axis
		glVertex3f(self.x - self.r, self.y, self.z)
		glVertex3f(self.x + self.r, self.y, self.z)
		
		glEnd()
		
		glLineWidth(1)
		
		glEnable(GL_LIGHTING)
		
		drawText3d((self.x, self.y + self.r, self.z), self.name, 32)
		
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
				
			if p.GetName() == "Position.X":
				self.x = p.GetValue()
			if p.GetName() == "Position.Y":
				self.y = p.GetValue()
			if p.GetName() == "Position.Z":
				self.z = p.GetValue()

	def populatepropgrid(self, pg):
		#Geometry Properties
		pg.Append( wxpg.PropertyCategory("Geometry") )
		
		normalID = pg.Append( wxpg.StringProperty("Position", value="<composed>") )
		pg.AppendIn (normalID, wxpg.FloatProperty("X", value=self.x) )
		pg.AppendIn (normalID, wxpg.FloatProperty("Y", value=self.y) )
		pg.AppendIn (normalID, wxpg.FloatProperty("Z", value=self.z) )
		
	def write(self, object):
		object.setAttribute("x", str(self.x) )
		object.setAttribute("y", str(self.y) )
		object.setAttribute("z", str(self.z) )