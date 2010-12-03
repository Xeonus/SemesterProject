import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from dendriticprofiling import correct
from javax.vecmath import Point3f
from ij3d import Image3DUniverse, Content
from customnode import CustomLineMesh
from java.awt.event import KeyListener

#randomForest has to be a list which contains lists of pairs which can be computet with testforcomparison.py
randomForest = [[83160, 99481], [81196, 75408], [81321, 99481], [99501, 99481], [85174, 99481], [99455, 97790], [83695, 97790], [99442, 92479], [93311, 97790], [81056, 75408], [83785, 99481], [99063, 75408], [89064, 91609], [83370, 94359], [89024, 99481], [98996, 75408], [80463, 75408], [80108, 75408], [83822, 99481], [81916, 99481], [99635, 75408], [89072, 91609], [82926, 99481], [82082, 75408], [83070, 75408], [79954, 99481], [83627, 99481], [83437, 75408], [81550, 99481], [83772, 75408], [72481, 99481], [89066, 99481], [70195, 75408], [99511, 99481], [82757, 99481], [99495, 99481], [80333, 75408], [71887, 91609], [98795, 75408]]
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

def makePairs(ids1, ids2):
  pairs=[]
  for id1 in ids1:
    for id2 in ids2:
      pair=[id1, id2]
      pairs.append(pair)
  return pairs

ids1=[83160, 81196, 81321, 99501, 85174, 99455, 83695, 99442, 93311, 
81056, 83785, 99063, 89064, 83370, 89024, 98996, 80463, 80108, 83822, 81916, 
99635, 89072, 82926, 82082, 83070, 79954, 83627, 83437, 81550, 83772, 72481, 
89066, 70195, 99511, 82757, 99495, 80333, 71887, 98795]
#lch5-1 right
ids2=[95421, 98268, 93662, 97669, 75408, 94943, 95674, 99490, 97790, 
92479, 95788, 91612, 94264, 95812, 83695, 93311, 95190, 95056, 95668, 95151, 
95424, 92485, 99481, 94859, 94364, 92799, 93195, 91609, 96114, 93048, 98238, 
93883, 95887, 93582, 94359, 96513, 93400, 95246]

#print makePairs(ids1, ids2)

#Initialize first 3D-Universe
visualize(randomForest[0], None)
