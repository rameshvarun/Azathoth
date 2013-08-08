import math
from OpenGL.GL import *
from OpenGL.GLU import *

#Turns a vector of either length 3 or 2 into a string
def formatString(v):
	if len(v) == 3:
		return str(v[0]) + ", " + str(v[1]) + ", " + str(v[2])
	if len(v) == 2:
		return str(v[0]) + ", " + str(v[1])
		
#Turns a list of strings into a list of floats
def toFloats(val):
	returnval = []
	
	for s in val:
		returnval.append( float(s) )
		
	return returnval

#Cross-product of two Vectors
def cross(v1, v2):
	c1 = v1[1]*v2[2] - v1[2]*v2[1]
	c2 = v1[2]*v2[0] - v1[0]*v2[2]
	c3 = v1[0]*v2[1] - v1[1]*v2[0]
	
	return [c1, c2, c3]
	
#Normalize a vector
def norm(v):
	mag = math.sqrt( v[0]*v[0] + v[1]*v[1] + v[2]*v[2] )
	return [v[0] / mag, v[1] / mag, v[2] / mag]

#Calculate the dot-product of two vectors
def dot(v1, v2):
	if len(v1) == 3 and len(v2) == 3:
		return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2] 
	if len(v1) == 2 and len(v2) == 2:
		return v1[0]*v2[0] + v1[1]*v2[1]

#Given a ray and a box, return the intersection point
#ro -- Ray Origin
#rd -- Ray Direction
#min -- Lower corner of box
#max -- Upper corner of box
def iBox(min, max, ro, rd):
	if min[0] < ro[0] and min[1] < ro[1] and min[2] < ro[2]:
		if max[0] > ro[0] and max[1] > ro[1] and max[2] > ro[2]:
			return False, 0
			
	tmin = ( min[0] - ro[0] ) / rd[0]
	tmax = ( max[0] - ro[0] ) / rd[0]
	
	if tmin > tmax:
		temp = tmin
		tmin = tmax
		tmax = temp
		
	tymin = ( min[1] - ro[1] ) / rd[1]
	tymax = ( max[1] - ro[1] ) / rd[1]
	
	if tymin > tymax:
		temp = tymin
		tymin = tymax
		tymax = temp
		
	if (tmin > tymax) or (tymin > tmax) :
		return False, 0
		
	if (tymin > tmin):
		tmin = tymin
	if (tymax < tmax):
		tmax = tymax
		
	tzmin = ( min[2] - ro[2] ) / rd[2]
	tzmax = ( max[2] - ro[2] ) / rd[2]
	
	if(tzmin > tzmax):
		temp = tzmin
		tzmin = tzmax
		tzmax = temp
		
	if ((tmin > tzmax) or (tzmin > tmax)):
		return False, 0
		
	if (tzmin > tmin):
		tmin = tzmin
	if (tzmax < tmax):
		tmax = tzmax
		
	if ( tmax < 0.0 ):
		return False, 0
		
	t = tmin
			
	return True, t

#Intersect a ray with a plane
#(x, y, z) = normal of plane
#w = distance along normal
#These values follow the plane equation: n*pos = w
#ro - Ray origin
#rd - Ray direction
def iPlane(x, y, z, w, ro, rd):
	t = -(dot( [x, y, z] ,ro) + w)/dot( [x, y, z] ,rd)
	
	if t > 0.0:
		return True, t
	else:
		return False, 0

#Intersect a ray with a sphere
#(x, y, z) = center of sphere
#r = radius of sphere
#ro - Ray origin
#rd - Ray direction
def iSphere(x, y, z, r, ro, rd):
	d = [ ro[0] - x, ro[1] - y, ro[2] - z ];
	b = dot(rd, d)
	c = dot(d, d) - r*r
	
	t = b*b - c
	if t > 0.0:
		t = - b - math.sqrt(t)
		return True, t
	
	return False, 0
#Add two vectors
def add(v1, v2):
	return [ v1[0] + v2[0] , v1[1] + v2[1], v1[2] + v2[2] ]

#Subtract v2 from v1
def subtract(v1, v2):
	return [ v1[0] - v2[0] , v1[1] - v2[1], v1[2] - v2[2] ]

#Distance betweem two points
def dist(v1, v2):
	if len(v1) == 3 and len(v2) == 3:
		return math.sqrt( math.pow(v2[0] - v1[0], 2) + math.pow(v2[1] - v1[1], 2) + math.pow(v2[2] - v1[2], 2))
	if len(v1) == 2 and len(v2) == 2:
		return math.sqrt( math.pow(v2[0] - v1[0], 2) + math.pow(v2[1] - v1[1], 2) )

#Multiply a vetor by a scalar
def mult(scalar, v):
	return [ scalar*v[0], scalar*v[1], scalar*v[2] ]
	
#Call to draw a 
def movetool(x, y, z, scale):
	glLineWidth(10) #Make lines very thick
	
	glDisable(GL_DEPTH_TEST)
	
	
	glDisable(GL_LIGHTING)
	glBegin(GL_LINES)
	
	#Y axis
	glColor3f(0,255,0)
	glVertex3f(x, y, z)
	glColor3f(0,255,0)
	glVertex3f(x, y + scale, z)
	
	#Z axis
	glColor3f(0,0,255)
	glVertex3f(x, y, z)
	glColor3f(0,0,255)
	glVertex3f(x, y, z + scale)
	
	#X axis
	glColor3f(255,0,0)
	glVertex3f(x, y, z)
	glColor3f(255,0,0)
	glVertex3f(x + scale, y, z)
	
	glEnd()
	
	glEnable(GL_LIGHTING)
	
	glLineWidth(1) #Return lines to their normal size
	
	glEnable(GL_DEPTH_TEST)