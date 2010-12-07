#Invariant tree-analysis with the PCA method
from math import sqrt  
from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append(System.getProperty("user.home") + "/Desktop/Fiji Scripts")
from matrixoperator import Matrix

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
    coords.append(Matrix([[x, y, z]]))
  
  return coords

  
tree = Display.getFront().getActive()

m = Matrix( [ [1, 2, 3], [4, 5, 6], [ 7, 8, 10 ] ] )
print "m is:", m
m= m.append( [1,1,1] )
print m
#Calculate the center of mass
center = Matrix([[0,0,0]])
coords = getNodeCoordinates(tree)
for coord in coords:
  center += coord
center /= float(len(coords)) 
print center


#Define covvariance matrix
# [[row1], [row2], [row3]]
cova = Matrix([[0,0,0],[0,0,0],[0,0,0]])
for coord in coords:
  diff = coord - center
  cova += diff * diff.transpose()

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
		
maxevector=evectors.getRow(maxevaluepos)  # its a list of 3 values

#Define a vector over the point cloud and count points in defined interval
#Normalize vector
length=sqrt(maxevector[0]**2 + maxevector[1]**2 + maxevector[2]**2)
normvector = Matrix([maxevector]) / length
#normvector = map(lambda x: x / length, maxevector)

#--------------------------------------code OK------------------------------
#Project all points to line of PCA vector
pca=[]
for coord in coords:
  pca=(coord-center) * (normvector)
  #pca.append.((coord-center).arraytimes(normvector))

print pca[0].getRowDimension(), pca[0].getColumnDimension()

#Find points with maximum distance from center = boundaries
#distance=[]
#for coord in coords:
#  if center > coord:
#    dist=center-coord
#  else:
#    dist=coord-center
#    distreal=


#Count number of nodes which fall in defined interval of pca projection
#counter = 0
#histovector = []
#binleft = pcamin
#binright = pcamin + 12.5

#Count all elements in defined interval -> make histogram vector
#iterations=(pcamax-pcamin)/12.5


#for i in range(0,iterations):
#  binleft=i*12.5
#  binright=binleft+12.5
#  for i in range(0, len(pca)):
#    if pca[i] <= binright and pca[i] >= binleft:
#      counter += 1    
#  histovector.append(counter)
#  counter=0

#print histovector
#Low cost version of above calculation:
