#Invariant tree-analysis with the PCA method
from math import sqrt  
from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append(System.getProperty("user.home") + "/Desktop/Fiji Scripts")
from matrixoperator import Matrix
from javax.media.j3d import Transform3D
from javax.vecmath import Point3d
from ij.io import FileSaver

from org.jfree.data.statistics import HistogramDataset

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

#---------Select tree-----------------  
#tree = Display.getFront().getActive()
ID = 74329
tree = Display.getFront().getLayerSet().findById(ID)
#-------------------------------------


#Calculate the center of mass
center = Matrix( [[0,0,0]] )
coords = Matrix(getNodeCoordinates(tree))
m=coords.getRowDimension()

for i in range(0, coords.getRowDimension()):
  center += Matrix([coords.getRow( i )])
center /= float(m)

print center

"""
x, y, z = 0, 0, 0
nc = getNodeCoordinates(tree)
for c in nc:
  x += c[0]
  y += c[1]
  z += c[2]
print "center:", x/len(nc), y/len(nc), z/len(nc)
"""

#Define covvariance matrix
cova = Matrix([[0,0,0],[0,0,0],[0,0,0]])
diff= Matrix ( [[0,0,0]])
for i in range(0, m):
  diff = Matrix([coords.getRow( i )]) - center
  cova += diff.transpose() * diff
cova /= float(m)


#Evaluedecomposition 
evaluedecomp = cova.eig()
evalues = evaluedecomp.getRealEigenvalues()
evectors = evaluedecomp.getV() # is a Matrix instance


#Find maximum Eigenvector for maximal Eigenvalue
maxevaluepos = -1
maxevalue = 0
for i in range(0, len(evalues)):
	if evalues[i] > maxevalue or maxevaluepos==-1:
		maxevalue=evalues[i]
		maxevaluepos=i

		
maxevector=evectors.getColumn(maxevaluepos)  #HAVE TO GET VALUES OF COLUMN of evector matrix  i NOT ROW



#--------------------TEST if Eigenvaluedecomposition is correct-----------
#vectormatrix=Matrix([evectors.getColumn(maxevaluepos)])
#test=cova * vectormatrix.transpose()
#test2=vectormatrix*maxevalue
#print test
#print test2
#-------------------------------------------------------------------------

#Define a vector over the point cloud and count points in defined interval
#Normalize vector
length=sqrt(maxevector[0]**2 + maxevector[1]**2 + maxevector[2]**2)
normvector = map(lambda x: x / length, maxevector)


normvectormatrix = Matrix([normvector])
pca=[]
m=coords.getRowDimension()
for i in range(0, m):
  pcastore = (Matrix([coords.getRow( i )]) - center ) * normvectormatrix.transpose()
  pca.append(pcastore.getRow(0))


#Count number of nodes which fall in defined interval of pca projection
counter = 0
histovector = []
pca=[ x[0] for x in pca] #get it back in array form (get rid of list in list)
binleft = min(pca)
iterations=20
length = int((max(pca)-min(pca))/iterations + 0.5)
binright = binleft + length


print iterations

for i in range(0,iterations):
  for i in range(0, len(pca)):
    if pca[i] <= binright and pca[i] >= binleft:
      counter += 1    
  histovector.append(counter)
  counter=0
  binleft+=length
  binright+=length

#histomirror=histovector.reverse()
print "The histogram vector is:", histovector


"""
#Plot center

from java.awt import Color
from ini.trakem2.display import Display3D
Display3D.addFatPoint("eigen center", tree.getLayerSet(), center.get(0, 0), center.get(0, 1), center.get(0, 2), 10, Color.red)
"""

plot = Plot("histogram", "bins", "count", range(iterations), histovector)
plot.show()
fs=FileSaver(plot.getImagePlus())
fs.saveAsPng(System.getProperty("user.home") + "/Desktop/Histotest/pcaleft" + str(ID) + ".png")

histovector.reverse()
plot = Plot("histogram", "bins", "count", range(iterations), histovector)
plot.show()
fs=FileSaver(plot.getImagePlus())
fs.saveAsPng(System.getProperty("user.home") + "/Desktop/Histotest/pcaright" + str(ID) + ".png")
