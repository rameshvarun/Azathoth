import pkgutil

types = {}

add = {}

import inspect

def get_user_attributes(cls):
    boring = dir(type('dummy', (object,), {}))
    return [item
            for item in inspect.getmembers(cls)
            if item[0] not in boring]

for loader, name, ispkg in  pkgutil.walk_packages(__path__):
	module = __import__( "gameobjects." + name )
	object_class = eval( name + "." + name )
	
	types[name] = object_class
	
	print "Loaded GameObject type ", name