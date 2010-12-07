import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from dendriticprofiling import correct
from javax.vecmath import Point3f
from ij3d import Image3DUniverse, Content
from customnode import CustomPointMesh
from matrixoperator import Matrix
from dendriticprofiling import getNodeCoordinates

def testprofiling(ID):
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

  #get it back in array form (get rid of list in list of Jarray)

  dpx=[ x[0] for x in dpx]
  dpy=[ x[0] for x in dpy]
  dpz=[ x[0] for x in dpz]
  zipped=zip(dpx, dpy, dpz)
  
  return zipped
"""
def testprofilingmesh(treeID):
  points=testprofiling(treeID)
  return CustomPointMesh(points)

def testvisualize():
  univ=Image3DUniverse(512,512)
  for ID in [71887]:
    mesh = testprofilingmesh(ID)
    c = univ.createContent(mesh, str(ID))
    univ.addContent(c)
  univ.show()

testvisualize()
"""

points = [(1,2,2),(2,2,2)]
mesh = CustomPointMesh(points)
univ = Image3DUniverse(512,512)
c = univ.createContent(mesh, str(12))
univ.addContent(c)
univ.show()