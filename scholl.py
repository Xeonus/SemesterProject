#Pseudo Scholl Analysis
#Count all nodes inbetween two spheres and plot a histogram of that
from math import sqrt  
from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from matrixoperator import Matrix
from javax.media.j3d import Transform3D
from javax.vecmath import Point3d
from ij.io import FileSaver

#-------------Transformation-------------------------------------

m = [0.9509217490842972, 0.24926674965164644, -0.18334097915241027, -51626.05759575438,
     -0.2722540786706435, 0.9555797748775074, -0.11289380183274611, -28182.499757448437,
     0.14705626054561627, 0.15726850086128405, 0.9765454801857332, -12950.550433910958,
     0.0, 0.0, 0.0, 1.0]
wt = Transform3D(m)

def correct(pa):
  global wt
  p = Point3d(pa[0], pa[1], pa[2])
  wt.transform(p)
  return [p.x, p.y, p.z]

#-----------Get Coordinates of tree------------------------------------

def getNodeCoordinates(tree):
  """ Returns a map of Node instances vs. their X,Y,Z world coordinates. """
  root = tree.getRoot()
  if root is None:
    return {}
  calibration = tree.getLayerSet().getCalibration()
  affine = tree.getAffineTransform()
  coords = []
  
  for nd in root.getSubtreeNodes():
    fp = array([nd.getX(), nd.getY()], 'f')
    affine.transform(fp, 0, fp, 0, 1)
    x = fp[0] * calibration.pixelWidth
    y = fp[1] * calibration.pixelHeight
    z = nd.getLayer().getZ() * calibration.pixelWidth   # a TrakEM2 oddity
    # data may be a radius or a java.awt.geom.Area 
    coords.append( correct([x, y, z]) )
    #print coords[len(coords)-1]
  return coords

def sphereCount(ID, biniter):
  #find center of mass
  tree = Display.getFront().getLayerSet().findById(ID)
  coords = Matrix(getNodeCoordinates(tree))
  center = Matrix( [[0,0,0]] )
  m=coords.getRowDimension()


  for i in range(0, m):
    center += Matrix([coords.getRow( i )])
  center /= float(m)

  #calculate all distances of all points to center of mass and put them in a list
  xdist=[]
  ydist=[]
  zdist=[]
  for i in range(0, m):
    xdiff=[]
    if coords.get(i,0) > center.get(0,0):
      xdiff = coords.get(i,0) - center.get(0,0)
    else:
      xdiff = center.get(0,0) - coords.get(i,0)
    xdist.append(xdiff)

  for i in range(0, m):
    ydiff=[]
    if coords.get(i,1) > center.get(0,1):
      ydiff = coords.get(i,1) - center.get(0,1)
    else:
      ydiff = center.get(0,1) - coords.get(i,1)
    ydist.append(ydiff)

  for i in range(0, m):
    zdiff=[]
    if coords.get(i,2) > center.get(0,2):
      zdiff = coords.get(i,2) - center.get(0,2)
    else:
      zdiff = center.get(0,2) - coords.get(i,2)
    zdist.append(zdiff)

  nodeDist=[]
  dist=[]
  for i in range(0, m):
    dist=sqrt(xdist[i]**2 + ydist[i]**2 + zdist[i]**2)
    nodeDist.append(dist)

  iterations=biniter
  Ri=0 #inner radius
  """
  The maximum distance can only be achieved in the xy-plane
  With "fixed" coordinates this will approx. be 35000nm
  To make the scholl-profiles comparable this length has to be used.
  """ 
  scholl=[]
  xaxis=[]
  counter=0
  length= int(35000 / biniter + 0.5)
  Ra=length #outer radius

  for i in range(0, biniter):
    for i in range(0, len(nodeDist)):
      if nodeDist[i] <= Ra and nodeDist[i] >= Ri:  
        counter += 1   
    scholl.append(counter)
    counter=0
    xaxis.append(Ri) # adapt THIS position in all other scripts! Otherwise 1 datapoint is missing!!
    Ri += length
    Ra += length
    
  return scholl, xaxis
  
#plot = Plot("histogram", "distance from center", "count",xaxis, scholl)
#plot.show()











