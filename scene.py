from OpenGL.GL import *
from OpenGL.GLU import *

from xml.dom.minidom import getDOMImplementation
from xml.dom.minidom import parse

import subprocess

import os

import gui
import scripteditor

import gameobjects

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


	
	#For every xml element with tag <Camera>
	for camObj in doc.getElementsByTagName("Camera"):
		cam.phi = float(camObj.getAttribute("phi"))
		cam.theta = float(camObj.getAttribute("theta"))
		
		cam.speed = float(camObj.getAttribute("speed"))
		
		cam.x = float(camObj.getAttribute("x"))
		cam.y = float(camObj.getAttribute("y"))
		cam.z = float(camObj.getAttribute("z"))
	
	#Load in all the object types
	for class_name in gameobjects.types.keys():
		for object_element in doc.getElementsByTagName( class_name ):
			gameobjects.types[class_name].load(object_element)
	
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