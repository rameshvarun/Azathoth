#File that handles all GUI-Related stuff
import threading, os, sys, time
import wx #import wxWidgets
import wx.stc
import wx.propgrid as wxpg
import scene

import scripteditor

#Callback for exiting application
def closeFile(event):
	os._exit(0)

app = wx.App(False)

evtloop = wx.EventLoop()
old = wx.EventLoop.GetActive()
wx.EventLoop.SetActive(evtloop)


#Create main window
frame = wx.Frame(None, wx.ID_ANY, "Non-Euclidean Level Editor", (10,10), (250,550))
frame.Show(True)

filemenu = wx.Menu()
addmenu = wx.Menu()
runmenu = wx.Menu()

frame.CreateStatusBar()

frame.Bind(wx.EVT_CLOSE, closeFile)

scripteditor.init()

menuBar = wx.MenuBar()
menuBar.Append(filemenu,"&File")
menuBar.Append(addmenu,"&Add")
menuBar.Append(runmenu,"&Run")
frame.SetMenuBar(menuBar)

#Create all of the actions under the file menu
new = filemenu.Append(wx.ID_NEW, "&New","Create a new scene.")
open = filemenu.Append(wx.ID_OPEN, "&Open","Open an existing scene file.")
save = filemenu.Append(wx.ID_SAVE, "&Save","Save the current scene file.")
close = filemenu.Append(wx.ID_EXIT, "&Exit","Exit the editor.")

#Bind a function to every action under the file menu
frame.Bind(wx.EVT_MENU, scene.newFile, new)
frame.Bind(wx.EVT_MENU, scene.openFile, open)
frame.Bind(wx.EVT_MENU, scene.saveFile, save)
frame.Bind(wx.EVT_MENU, closeFile, close)

#Create all of the menu items under the Add menu
plane = addmenu.Append(wx.ID_ANY, "&Plane","Create a new plane.")
sphere = addmenu.Append(wx.ID_ANY, "&Sphere","Create a new sphere.")
box = addmenu.Append(wx.ID_ANY, "&Box","Create a new box.")

boxaberration = addmenu.Append(wx.ID_ANY, "&Box Aberration","Create a new box aberration.")
sphereaberration = addmenu.Append(wx.ID_ANY, "&Sphere Aberration","Create a new sphere aberration.")

sphereportal = addmenu.Append(wx.ID_ANY, "&Sphere Portal","Create a new sphere portal.")

#Bind a function to every action under the add menu
frame.Bind(wx.EVT_MENU, scene.addPlane, plane)
frame.Bind(wx.EVT_MENU, scene.addSphere, sphere)
frame.Bind(wx.EVT_MENU, scene.addBox, box)

frame.Bind(wx.EVT_MENU, scene.addBoxAberration, boxaberration)
frame.Bind(wx.EVT_MENU, scene.addSphereAberration, sphereaberration)

frame.Bind(wx.EVT_MENU, scene.addSpherePortal, sphereportal)

#Create/Bind a function to the runTest item
runtest = runmenu.Append(wx.ID_ANY, "&Run Test","Run a test of the map within the actual game engine.")
frame.Bind(wx.EVT_MENU, scene.runTest, runtest)


#Create the tree view
tree_ctrl = wx.TreeCtrl(frame,  -1, style=wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_EDIT_LABELS | wx.TR_MULTIPLE)
treeroot = tree_ctrl.AddRoot('Scene')
tree_ctrl.ExpandAll()

class PropertyGridPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)
		topsizer = wx.BoxSizer(wx.VERTICAL)
		self.pg = pg = wxpg.PropertyGrid(self, style=wxpg.PG_SPLITTER_AUTO_CENTER|wxpg.PG_TOOLBAR)
		
		pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS | wxpg.PG_EX_MULTIPLE_SELECTION)
		topsizer.Add(pg,1,wx.EXPAND)
		rowsizer = wx.BoxSizer(wx.HORIZONTAL)
		self.delete = wx.Button(self,-1,"Delete Object")
		
		rowsizer.Add(self.delete,1)
		
		topsizer.Add(rowsizer,0,wx.EXPAND)
		self.SetSizer(topsizer)
		topsizer.SetSizeHints(self)

#Create the edit window
editframe = wx.Frame( None, -1, "Properties Window", (1280,10), (350,550) )

editframe.panel = PropertyGridPanel(editframe)

editframe.Show()
editframe.Bind(wx.EVT_CLOSE, closeFile)

currentselection = None
editframe.panel.delete.Hide()


def updateSelection(event):
	for obj in scene.objects.values():
		if tree_ctrl.IsSelected(obj.treeitem):
			obj.selected = True
		else:
			obj.selected = False

frame.Bind(wx.EVT_TREE_SEL_CHANGED, updateSelection, tree_ctrl)

def update():
	global currentselection

	while evtloop.Pending():
		evtloop.Dispatch()
		
	#time.sleep(0.10)
	app.ProcessIdle()
	
	newselection = None
	for obj in scene.objects.values():
		if obj.selected:
			newselection = obj
			break
			
	if currentselection != newselection:
		if currentselection != None:
			currentselection.pg = None
			
		currentselection = newselection
		
		editframe.panel.pg.Clear()

		if currentselection == None:
			editframe.SetTitle("Properties Window")
			editframe.panel.delete.Hide()
		else:
			currentselection.pg = editframe.panel.pg
			
			currentselection.pg.Bind( wxpg.EVT_PG_CHANGED, currentselection.PropertyChange )
			
			editframe.SetTitle("Properties of " + currentselection.name)
			editframe.panel.delete.Show()
			
			pg = editframe.panel.pg
			
			pg.Append( wxpg.PropertyCategory("General") )
			pg.Append( wxpg.StringProperty("Object Name", value=currentselection.name) )
			pg.Append( wxpg.BoolProperty("Uniform",value=currentselection.uniform) )
			pg.SetPropertyAttribute("Uniform", "UseCheckbox", True)
			
			currentselection.populatepropgrid(pg)