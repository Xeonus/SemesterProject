import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from dendriticprofiling import correct
from javax.vecmath import Point3f
from ij3d import Image3DUniverse, Content
from customnode import CustomLineMesh

def createMesh(treeID):
  tree = Display.getFront().getLayerSet().findById(treeID)
  points = tree.generateSkeleton(1, 12, 1).verts
  for p in set(points):
    c = correct([p.x, p.y, p.z])
    p.x = float(c[0])
    p.y = float(c[1])
    p.z = float(c[2])
  return CustomLineMesh(points, CustomLineMesh.PAIRWISE)


def visualize():
  univ = Image3DUniverse(512, 512)
  for ID in [99442, 96580]:
    mesh = createMesh(ID)
    c = univ.createContent(mesh, str(ID))
    univ.addContent(c)
  univ.show()

visualize()