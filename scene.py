from OpenGL.GL import *
from OpenGL.GLU import *

from xml.dom.minidom import getDOMImplementation
from xml.dom.minidom import parse

import subprocess

import os

import gui
import scripteditor

import wx

from util import *

from camera import *

def initialize():
	global objects
	global currentfile
	
	#Dictionary of all objects in scene
	objects = {}

	#The current file that the editor is working on
	currentfile = "empty"

#A helper function for generating a unique name that is not currently being used for an object in the scene
def uniqueName(stub):
	counter = 1
	while (stub + str(counter)) in objects:
		counter += 1
	
	return (stub + str(counter))

#Clear the entire scene
def clearScene():
	#Clear both the GUI tree and the objects list
	gui.tree_ctrl.DeleteAllItems()
	objects.clear()
	
	#Re-add the root element of the scene tree
	gui.treeroot = gui.tree_ctrl.AddRoot('Scene')
	gui.tree_ctrl.ExpandAll()
	
	#Clear script
	scripteditor.SetText( "" )
	
def newFile(event):
	global currentfile
	currentfile = "empty"
	
	clearScene()

def getText(n):
    rc = []
    for node in n.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

#Function that loads a scene from a file
def openFile(event):
	global currentfile
	
	clearScene() #Clear current scene first
	
	openFileDialog = wx.FileDialog(gui.frame, "Open a scene file", "", "","XML file (*.xml)|*.xml", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
	
	if openFileDialog.ShowModal() == wx.ID_CANCEL:
		return
	
	currentfile = openFileDialog.GetPath()
	
	doc = parse(currentfile)

	#Turns a list of strings into a list of floats
	def toFloats(val):
		returnval = []
		
		for s in val:
			returnval.append( float(s) )
			
		return returnval
	
	#For every xml element with tag <Camera>
	for camObj in doc.getElementsByTagName("Camera"):
		cam.phi = float(camObj.getAttribute("phi"))
		cam.theta = float(camObj.getAttribute("theta"))
		
		cam.speed = float(camObj.getAttribute("speed"))
		
		cam.x = float(camObj.getAttribute("x"))
		cam.y = float(camObj.getAttribute("y"))
		cam.z = float(camObj.getAttribute("z"))
	
	#For every xml element with tag <Plane>
	for plane in doc.getElementsByTagName("Plane"):
		name = plane.getAttribute("name")
		
		objects[name] = Plane(name, float(plane.getAttribute("x")) , float(plane.getAttribute("y")) , float(plane.getAttribute("z")) , float(plane.getAttribute("c")) )
		objects[name].selected = (plane.getAttribute("selected") == "True")
		
		objects[name].uniform = (plane.getAttribute("uniform") == "True")
		objects[name].reflectivity = float(plane.getAttribute("reflectivity"))
		objects[name].recieve = (plane.getAttribute("recieve") == "True")
		
		objects[name].treeitem = gui.tree_ctrl.AppendItem(gui.treeroot, name) #Add this plane to the tree view
	
	#For every xml element with tag <Box>
	for box in doc.getElementsByTagName("Box"):
		name = box.getAttribute("name")
		min = box.getAttribute("min").split(",")
		max = box.getAttribute("max").split(",")
		
		objects[name] = Box(name, toFloats(min), toFloats(max) )
		objects[name].selected = (box.getAttribute("selected") == "True")
		
		objects[name].uniform = (box.getAttribute("uniform") == "True")
		
		objects[name].cast = (box.getAttribute("cast") == "True")
		objects[name].recieve = (box.getAttribute("recieve") == "True")
		
		objects[name].treeitem = gui.tree_ctrl.AppendItem(gui.treeroot, name)
	
	#For every xml element with tag <Sphere>
	for sphere in doc.getElementsByTagName("Sphere"):
		name = sphere.getAttribute("name")
		
		objects[name] = Sphere(name, float(sphere.getAttribute("x")) , float(sphere.getAttribute("y")) , float(sphere.getAttribute("z")) , float(sphere.getAttribute("r")) )
		objects[name].selected = (sphere.getAttribute("selected") == "True")
		
		objects[name].uniform = (sphere.getAttribute("uniform") == "True")
		
		objects[name].reflectivity = float(sphere.getAttribute("reflectivity"))
		objects[name].recieve = (sphere.getAttribute("recieve") == "True")
		objects[name].cast = (sphere.getAttribute("cast") == "True")
		
		objects[name].treeitem = gui.tree_ctrl.AppendItem(gui.treeroot, name)
	
	#For every xml element with tag <BoxAberration>
	for box in doc.getElementsByTagName("BoxAberration"):
		name = box.getAttribute("name")
		min = box.getAttribute("min").split(",")
		max = box.getAttribute("max").split(",")
		
		objects[name] = BoxAberration(name, toFloats(min), toFloats(max) )
		objects[name].selected = (box.getAttribute("selected") == "True")
		
		objects[name].uniform = (box.getAttribute("uniform") == "True")
		
		objects[name].cast = (box.getAttribute("cast") == "True")
		objects[name].recieve = (box.getAttribute("recieve") == "True")
		
		objects[name].scale = toFloats( box.getAttribute("scale").split(",") )
		
		objects[name].treeitem = gui.tree_ctrl.AppendItem(gui.treeroot, name)
		
	#For every xml element with tag <SphereAberration>
	for sphere in doc.getElementsByTagName("SphereAberration"):
		name = sphere.getAttribute("name")
		
		objects[name] = SphereAberration(name, float(sphere.getAttribute("x")) , float(sphere.getAttribute("y")) , float(sphere.getAttribute("z")) , float(sphere.getAttribute("r")) )
		objects[name].selected = (sphere.getAttribute("selected") == "True")
		
		objects[name].uniform = (sphere.getAttribute("uniform") == "True")
		
		objects[name].reflectivity = float(sphere.getAttribute("reflectivity"))
		objects[name].recieve = (sphere.getAttribute("recieve") == "True")
		objects[name].cast = (sphere.getAttribute("cast") == "True")
		
		objects[name].scale = toFloats( sphere.getAttribute("scale").split(",") )
		
		objects[name].treeitem = gui.tree_ctrl.AppendItem(gui.treeroot, name)
		
	#For every xml element with tag <SpherePortal>
	for sphere in doc.getElementsByTagName("SpherePortal"):
		name = sphere.getAttribute("name")
		
		objects[name] = SpherePortal(name, float(sphere.getAttribute("x")) , float(sphere.getAttribute("y")) , float(sphere.getAttribute("z")) , float(sphere.getAttribute("r")) )
		
		objects[name].x2 = float(sphere.getAttribute("x2"))
		objects[name].y2 = float(sphere.getAttribute("y2"))
		objects[name].z2 = float(sphere.getAttribute("z2"))
		
		objects[name].selected = (sphere.getAttribute("selected") == "True")
		
		objects[name].uniform = (sphere.getAttribute("uniform") == "True")
		
		objects[name].reflectivity = float(sphere.getAttribute("reflectivity"))
		objects[name].recieve = (sphere.getAttribute("recieve") == "True")
		objects[name].cast = (sphere.getAttribute("cast") == "True")
		
		objects[name].treeitem = gui.tree_ctrl.AppendItem(gui.treeroot, name)
		
	for script in doc.getElementsByTagName("script"):
		scripteditor.SetText( getText(script) )
	
def writeXML(filename):
		
	file = None
	
	doc = getDOMImplementation().createDocument(None, "scene", None)
	
	camera = doc.createElement("Camera")
	camera.setAttribute("x", str(cam.x) )
	camera.setAttribute("y", str(cam.y) )
	camera.setAttribute("z", str(cam.z) )
	
	camera.setAttribute("theta", str(cam.theta) )
	camera.setAttribute("phi", str(cam.phi) )
	camera.setAttribute("speed", str(cam.speed) )
	
	doc.documentElement.appendChild(camera)
	
	for obj in objects.values():
		object = doc.createElement(obj.type)
		
		object.setAttribute("name", obj.name)
		
		object.setAttribute("uniform", str(obj.uniform) )
		
		obj.write(object)
			
		object.setAttribute("selected", str(obj.selected) )
		
		doc.documentElement.appendChild(object)
		
	script = doc.createElement("script")
	script.appendChild( doc.createTextNode( scripteditor.GetText() ) )
	doc.documentElement.appendChild(script)
		
	file = open(filename, "w")
	file.write( doc.toprettyxml() )
	file.close()
	
def saveFile(event):
	global currentfile
	
	if currentfile == "empty":
		saveFileDialog = wx.FileDialog(gui.frame, "Save a scene file", "", "","XML file (*.xml)|*.xml", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
	
		if saveFileDialog.ShowModal() == wx.ID_CANCEL:
			return
	
		currentfile = saveFileDialog.GetPath()
		
	writeXML(currentfile)
	
#Triggered by menu button, runs current scene in game engine
def runTest(event):
	writeXML("Renderer\\test.xml") #Save file
	
	subprocess.Popen("Renderer\\NonEuclid.exe", cwd="Renderer\\") #Start game process

def addBox(event=None):
	name = uniqueName("Box")
	
	objects[name] = Box(name, [0,0,0], [5,5,5])
	
	print "Added " + name
	
	objects[name].treeitem = gui.tree_ctrl.AppendItem(gui.treeroot, name)
	gui.tree_ctrl.ExpandAll()
	
def addSphere(event=None):
	name =  uniqueName("Sphere")
	objects[name] = Sphere(name, 1, 1, 1, 1)
	
	print "Added " + name
	
	objects[name].treeitem = gui.tree_ctrl.AppendItem(gui.treeroot, name)
	gui.tree_ctrl.ExpandAll()
	

#Add default box aberration to scene
def addBoxAberration(event=None):
	name = uniqueName("BoxAberration")
	
	objects[name] = BoxAberration(name, [0,0,0], [5,5,5])
	
	print "Added " + name
	
	objects[name].treeitem = gui.tree_ctrl.AppendItem(gui.treeroot, name)
	gui.tree_ctrl.ExpandAll()

#Adds a default sphere aberration to the scene (triggered by gui command)
def addSphereAberration(event=None):
	name =  uniqueName("SphereAberration")
	objects[name] = SphereAberration(name, 1, 1, 1, 1)
	
	print "Added " + name
	
	objects[name].treeitem = gui.tree_ctrl.AppendItem(gui.treeroot, name)
	gui.tree_ctrl.ExpandAll()
	
def addSpherePortal(event=None):
	name =  uniqueName("SpherePortal")
	objects[name] = SpherePortal(name, 1, 1, 1, 1)
	
	print "Added " + name
	
	objects[name].treeitem = gui.tree_ctrl.AppendItem(gui.treeroot, name)
	gui.tree_ctrl.ExpandAll()