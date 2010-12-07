#Invariant tree-analysis with the PCA method
import matrixoperations  
import mdp
import getNodeCoordinates #use later only function
import math  
from ini.trakem2.display import Display
from jarray import array
 
def getNodeCoordinates(tree):
  """ Returns a map of Node instances vs. their X,Y,Z world coordinates. """
  root = tree.getRoot()
  if root is None:
    return {}
  calibration = tree.getLayerSet().getCalibration()
  affine = tree.getAffineTransform()
  coords = {}
  
  for nd in root.getSubtreeNodes():
    fp = array([nd.getX(), nd.getY()], 'f')
    affine.transform(fp, 0, fp, 0, 1)
    x = fp[0] * calibration.pixelWidth
    y = fp[1] * calibration.pixelHeight
    z = nd.getLayer().getZ() * calibration.pixelWidth   # a TrakEM2 oddity
    # data may be a radius or a java.awt.geom.Area 
    coords[nd] = [x, y, z]
  
  return coords

 #Functions to do operations in list elements
def addlists(list1, list2):
  return [x+y for x,y in zip(list1,list2)]

def sublists(list1, list2):
  return [x-y for x,y in zip(list1,list2)]
  
def divlist(liste, n):
  return [ x/n for x in liste]

#Calculate the center of mass
center=[0,0,0]
coords=getNodeCoordinates(tree)  
for node, coord in coords:
  center=addlist(center, coord)
center=divlist(center, len(coords))
print center

# [[row1], [row2], [row3]]

rows=[[0,0,0],[0,0,0],[0,0,0]]
for node, coord in coords:
  diff=sublists(coord, center)
  for i in range(0,len(center)):
    for j in range(0,len(center)):
      rows[i][j] = diff[i]*diff[j]
	
#Eigenvaluedecomposition
 
cova=Matrix(rows) 
 
evaluedecomp = cova.eig()
evalues = evaluedecomp.getRealEigenvalues()
evectors = evaluedecomp.getV()

#Find maximum Eigenvector for maximal Eigenvalue
maxevaluepos=-1
maxevalue=0
for i in range(0, len(evalues)):
	if evalues[i] > maxevalue or maxevaluepos==-1:
		maxevalue=evalue[i]
		maxevaluepos=i
		
maxevector=evectors[i]