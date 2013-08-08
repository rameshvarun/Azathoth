from OpenGL.GL import *
from OpenGL.GLU import *

from util import *

import gui
import scene

import wx #import wxWidgets
import wx.propgrid as wxpg

class Plane:
	def __init__(self, name = None, x = 0, y = 1, z = 0, c = 0):
		
		self.name = name
		
		if self.name == None:
			self.name = scene.uniqueName("Plane")
		
		n = norm( [x, y, z] )
		
		self.x = n[0]
		self.y = n[1]
		self.z = n[2]
		self.c = -c
		
		self.selected = False
		
		self.type = "Plane"
		
		self.reflectivity = 0.0
		self.uniform = False
		self.recieve = False
		
		
		self.edit = False
		
		self.transparent = False
		
		self.extension = 1000
		
		self.pg = None
		
		scene.objects[self.name] = self
		self.treeitem = gui.tree_ctrl.AppendItem(gui.treeroot, self.name)
		gui.tree_ctrl.ExpandAll()
		
		print "Added plane " + self.name
		
	@staticmethod
	def create(event):
		Plane()
		
	def duplicate(self, newname):
		newplane = Plane(newname, self.x, self.y, self.z, -self.c)
		
		newplane.reflectivity = self.reflectivity
		newplane.uniform = self.uniform
		newplane.recieve = self.recieve
		
		return newplane
		
	def center(self):
		return (self.x * self.c, self.y * self.c, self.z * self.c)
	def move(self, x, y, z):
		pass
	def collide(self, ro, rd):
		return iPlane(self.x, self.y, self.z, -self.c, ro, rd)
	def uniformChanged(self, event):
		print event.widget.variable.get()
	def draw(self):
		glEnable(GL_LIGHTING)
		glDisable(GL_CULL_FACE)
		
		glMaterialfv(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
		
		glBegin(GL_QUADS)
		
		glNormal3f( self.x, self.y, self.z)
		
		origin = (self.x * self.c, self.y * self.c, self.z * self.c)
		
		v1 = norm( cross( ( self.x, self.y, self.z), ( self.x + 1, self.y, self.z) ) )
		
		v2 = norm( cross( ( self.x, self.y, self.z), v1) )
		
		
		glVertex3f( origin[0] - self.extension*v1[0] - self.extension*v2[0], origin[1] - self.extension*v1[1] - self.extension*v2[1], origin[2] - self.extension*v1[2] - self.extension*v2[2])
		
		glVertex3f( origin[0] - self.extension*v1[0] + self.extension*v2[0], origin[1] - self.extension*v1[1] + self.extension*v2[1], origin[2] - self.extension*v1[2] + self.extension*v2[2] )
		
		glVertex3f( origin[0] + self.extension*v1[0] + self.extension*v2[0], origin[1] + self.extension*v1[1] + self.extension*v2[1], origin[2] + self.extension*v1[2] + self.extension*v2[2] )
		
		glVertex3f( origin[0] + self.extension*v1[0] - self.extension*v2[0], origin[1] + self.extension*v1[1] - self.extension*v2[1], origin[2] + self.extension*v1[2] - self.extension*v2[2] )
		
		glEnd()
		
		glEnable(GL_CULL_FACE)
		
		glDisable(GL_LIGHTING)
		
		glLineWidth(2)
		
		glBegin(GL_LINES)
		
		if self.edit:
			glColor3f(1, 0.62745, 0.176470)
		elif self.selected:
			glColor3f(0,1,0)
		else:
			glColor3f(1, 1, 1)
			
		glVertex3f(origin[0], origin[1], origin[2] )
		glVertex3f( origin[0] + 10*self.x, origin[1] + 10*self.y, origin[2] + 10*self.z)
		
		
		glVertex3f(origin[0], origin[1], origin[2] )
		glVertex3f(  origin[0] + 10*v1[0],  origin[1] + 10*v1[1],  origin[2] + 10*v1[2])
		
		glVertex3f(origin[0], origin[1], origin[2] )
		glVertex3f(  origin[0] + 10*v2[0],  origin[1] + 10*v2[1],  origin[2] + 10*v2[2])
			
		glEnd()
		
		glLineWidth(1)
		
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
				
			#Geometry Properties
			if p.GetName() == "C":
				self.c = -p.GetValue()
			
			if p.GetName() == "Normal":
				
				n = norm( [self.pg.GetPropertyByName("Normal.X").GetValue(),
				self.pg.GetPropertyByName("Normal.Y").GetValue(),
				self.pg.GetPropertyByName("Normal.Z").GetValue()] )
				
				self.x = n[0]
				self.y = n[1]
				self.z = n[2]
				
			#Material Properties
			if p.GetName() == "Reflectivity":
				self.reflectivity = p.GetValue()
			if p.GetName() == "Recieve Shadows":
				self.recieve = p.GetValue()
	def populatepropgrid(self, pg):
		#Geometry Properties
		pg.Append( wxpg.PropertyCategory("Geometry") )
		
		normalID = pg.Append( wxpg.StringProperty("Normal", value="<composed>") )
		pg.AppendIn (normalID, wxpg.FloatProperty("X", value=self.x) )
		pg.AppendIn (normalID, wxpg.FloatProperty("Y", value=self.y) )
		pg.AppendIn (normalID, wxpg.FloatProperty("Z", value=self.z) )
		
		pg.Append( wxpg.FloatProperty("C", value=self.c) )
		
		
		pg.Append( wxpg.PropertyCategory("Material") )
		
		pg.Append( wxpg.FloatProperty("Reflectivity", value=self.reflectivity) )
		
		pg.Append( wxpg.BoolProperty("Recieve Shadows",value=self.recieve) )
		pg.SetPropertyAttribute("Recieve Shadows", "UseCheckbox", True)
	def write(self, object):
		object.setAttribute("x", str(self.x) )
		object.setAttribute("y", str(self.y) )
		object.setAttribute("z", str(self.z) )
		object.setAttribute("c", str(-self.c) )
		
		object.setAttribute("reflectivity", str(self.reflectivity) )
		object.setAttribute("recieve", str(self.recieve) )