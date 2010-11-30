import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from dendriticprofiling import correct
from javax.vecmath import Point3f
from ij3d import Image3DUniverse, Content
from customnode import CustomLineMesh
from java.awt.event import KeyListener

#randomForest has to be a list which contains lists of pairs which can be computet with testforcomparison.py
randomForest = [[83695, 83695], [83695, 93311], [83695, 93883], [99442, 92485], [99442, 92799], [93311, 83695], [93311, 93883], [83370, 92479], [79954, 92479], [72481, 99481], [82757, 92485], [99495, 92799], [71887, 75408]]
matches=[]
nomatches=[]
pos=0

class MyKeyListener(KeyListener):
  def __init__ (self, univ):
    self.univ = univ
    
  def keyTyped(self, e):
    global pos
    keychar = e.getKeyChar()
    if keychar == str(4):
      match = randomForest[pos]
      pos+=1
      matches.append(match)
      print "list of matches:", matches
      print "list of false matches:", nomatches
      visualize(randomForest[pos], self.univ)
    if keychar == str(5):
      nomatch = randomForest[pos]
      nomatches.append(nomatch)
      pos+=1
      print "list of false matches:", nomatches
      print "list of matches:", matches
      visualize(randomForest[pos], self.univ)

     
def createMesh(treeID):
  tree = Display.getFront().getLayerSet().findById(treeID)
  points = tree.generateSkeleton(1, 12, 1).verts
  for p in set(points):
    c = correct([p.x, p.y, p.z])
    p.x = float(c[0])
    p.y = float(c[1])
    p.z = float(c[2])
  return CustomLineMesh(points, CustomLineMesh.PAIRWISE)

#visualizes a pair of 2 IDs in the manner [id1, id2]
def visualize(pair, univ):
  if univ is None:
    univ =  Image3DUniverse(512, 512)
    univ.show()
    canvas = univ.getCanvas() 
    canvas.addKeyListener(MyKeyListener(univ))
  else:
    univ.removeAllContents()
  for ID in pair:
    mesh = createMesh(ID)
    c = univ.createContent(mesh, str(ID))
    univ.addContent(c)  

#Initialize first 3D-Universe
visualize(randomForest[0], None)
