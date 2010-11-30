#Project all nodes on to the 3 main axis and calculate the sum of the distances of all points to that axis in the bin

from math import sqrt  
from ini.trakem2.display import Display
from jarray import array, zeros
import sys
#sys.path.append(System.getProperty("user.home") + "/Desktop/Fiji Scripts")
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from matrixoperator import Matrix
from javax.media.j3d import Transform3D
from javax.vecmath import Point3d
from ij.io import FileSaver
from java.util import HashSet
from ini.trakem2.vector import VectorString3D, VectorString, Editions

from org.jfree.data.statistics import HistogramDataset

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




#-----------Get Dendritic Profiles-------------------------------------
# Included additional string to count the distances of all nodes to the axis in that bin

def getDendriticProfiles(ID, biniter):

  tree = Display.getFront().getLayerSet().findById(ID)

  coords = Matrix(getNodeCoordinates(tree))

  #Define axis vectors and origin
  xnorm = Matrix([[1,0,0]])
  ynorm = Matrix([[0,1,0]])
  znorm = Matrix([[0,0,1]])
  center= Matrix([[0,0,0]])

  #Project nodes onto axis
  dpx=[]
  dpy=[]
  dpz=[]
  m=coords.getRowDimension()
  for i in range(0, m):
    xstore = Matrix([coords.getRow( i )]) * xnorm.transpose()
    ystore = Matrix([coords.getRow( i )]) * ynorm.transpose()
    zstore = Matrix([coords.getRow( i )]) * znorm.transpose()
    dpx.append(xstore.getRow(0))
    dpy.append(ystore.getRow(0))
    dpz.append(zstore.getRow(0))

  #Count number of nodes which fall in defined interval of pca projection
  counter = 0
  xhistovector = []
  yhistovector = []
  zhistovector = []

  #get it back in array form (get rid of list in list of Jarray)

  dpx=[ x[0] for x in dpx]
  dpy=[ x[0] for x in dpy]
  dpz=[ x[0] for x in dpz]

  #Initialize interval size and fix iterations to a specific number
  xbinleft = -34600.0
  ybinleft = -24200.0
  zbinleft = 0
  #--------PARAMETER FOR MACHINE LEARNING-----
  iterations = biniter
  #-------------------------------------------
  xlength = int((35600.0+34600.0)/iterations + 0.5)
  ylength = int((21300.0+24200.0)/iterations + 0.5)
  zlength = int((22500)/iterations + 0.5)
  xbinright = xbinleft + xlength
  ybinright = ybinleft + ylength
  zbinright = zbinleft + zlength

  #Count elements in bins
  xaxis=[]

  #Count lengths in bins
  xdiff=0
  ydiff=0
  zdiff=0
  xdist=[]
  ydist=[]
  zdist=[]

  for i in range(0,iterations):
    for i in range(0, len(dpx)):
      if dpx[i] <= xbinright and dpx[i] >= xbinleft:
        counter += 1
        xdiff += sqrt(dpy[i]**2) #xdist is yvalue
    xdist.append(xdiff)        
    xhistovector.append(counter)
    counter=0
    xdiff=0
    xaxis.append(xbinleft)
    xbinleft += xlength
    xbinright += xlength
  
  yaxis=[]

  for i in range(0,iterations):
    for i in range(0, len(dpy)):
      if dpy[i] <= ybinright and dpy[i] >= ybinleft:
        counter += 1    
        ydiff += sqrt(dpx[i]**2)
    ydist.append(ydiff)
    yhistovector.append(counter)
    counter=0
    ydiff = 0
    yaxis.append(ybinleft)
    ybinleft += ylength
    ybinright += ylength

  zaxis=[]

  for i in range(0,iterations):
    for i in range(0, len(dpz)):
      if dpz[i] <= zbinright and dpz[i] >= zbinleft:
        counter += 1    
        zdiff = sqrt(dpx[i]**2 + dpy[i]**2)
    zdist.append(zdiff)
    zhistovector.append(counter)
    counter=0
    zdiff=0
    zaxis.append(zbinleft)
    zbinleft += zlength
    zbinright += zlength

    #Normalize
  for i in range(0, iterations):
    xhistovector[i]/=float(xlength)
    yhistovector[i]/=float(ylength)
    zhistovector[i]/=float(zlength)
    
  return xhistovector , yhistovector, zhistovector, xdist, ydist, zdist