

import gui
import scene

class GameObject:
	def __init__(self):
		self.selected = False
		
		self.uniform = False
		self.edit = False
		
		self.pg = None
		
		self.cast = False
		self.recieve = False
		
		self.transparent = False
		
		if self.name == None:
			self.name = scene.uniqueName( self.type )
		
		scene.objects[self.name] = self #Add back to scene
		
		#Add to gui tree
		self.treeitem = gui.tree_ctrl.AppendItem(gui.treeroot, self.name)
		gui.tree_ctrl.ExpandAll()
		
		print "Added " + self.type + " - " + self.name