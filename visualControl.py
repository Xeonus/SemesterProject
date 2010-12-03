import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from dendriticprofiling import correct
from javax.vecmath import Point3f, Color3f
from ij3d import Image3DUniverse, Content
from customnode import CustomLineMesh
from java.awt.event import KeyListener
from java.awt import Color

#randomForest has to be a list which contains lists of pairs which can be computet with testforcomparison.py
randomForest = [[83160, 75408], [83160, 99481], [83160, 97790], [83160, 97790], [83160, 92479], [83160, 95788], [83160, 94264], [83160, 99481], [83160, 94859], [83160, 94364], [83160, 92799], [83160, 93195], [81196, 75408], [81196, 99481], [81196, 97790], [81196, 97790], [81196, 92479], [81196, 95788], [81196, 94264], [81196, 99481], [81196, 94859], [81196, 94364], [81196, 92799], [81196, 93195], [81321, 75408], [81321, 99481], [81321, 97790], [81321, 97790], [81321, 92479], [81321, 95788], [81321, 94264], [81321, 99481], [81321, 94859], [81321, 94364], [81321, 92799], [81321, 93195], [99501, 75408], [99501, 99481], [99501, 97790], [99501, 97790], [99501, 92479], [99501, 95788], [99501, 94264], [99501, 99481], [99501, 94859], [99501, 94364], [99501, 92799], [99501, 93195], [85174, 75408], [85174, 99481], [85174, 97790], [85174, 97790], [85174, 92479], [85174, 95788], [85174, 94264], [85174, 99481], [85174, 94859], [85174, 94364], [85174, 92799], [85174, 93195], [99455, 75408], [99455, 99481], [99455, 97790], [99455, 97790], [99455, 92479], [99455, 95788], [99455, 94264], [99455, 99481], [99455, 94859], [99455, 94364], [99455, 92799], [99455, 93195], [83695, 75408], [83695, 99481], [83695, 97790], [83695, 97790], [83695, 92479], [83695, 95788], [83695, 94264], [83695, 99481], [83695, 94859], [83695, 94364], [83695, 92799], [83695, 93195], [99442, 75408], [99442, 99481], [99442, 97790], [99442, 97790], [99442, 92479], [99442, 95788], [99442, 94264], [99442, 99481], [99442, 94859], [99442, 94364], [99442, 92799], [99442, 93195], [93311, 75408], [93311, 99481], [93311, 97790], [93311, 97790], [93311, 92479], [93311, 95788], [93311, 94264], [93311, 99481], [93311, 94859], [93311, 94364], [93311, 92799], [93311, 93195], [81056, 75408], [81056, 99481], [81056, 97790], [81056, 97790], [81056, 92479], [81056, 95788], [81056, 94264], [81056, 99481], [81056, 94859], [81056, 94364], [81056, 92799], [81056, 93195], [83785, 75408], [83785, 99481], [83785, 97790], [83785, 97790], [83785, 92479], [83785, 95788], [83785, 94264], [83785, 99481], [83785, 94859], [83785, 94364], [83785, 92799], [83785, 93195], [99063, 75408], [99063, 99481], [99063, 97790], [99063, 97790], [99063, 92479], [99063, 95788], [99063, 94264], [99063, 99481], [99063, 94859], [99063, 94364], [99063, 92799], [99063, 93195], [89064, 75408], [89064, 99481], [89064, 97790], [89064, 97790], [89064, 92479], [89064, 95788], [89064, 94264], [89064, 99481], [89064, 94859], [89064, 94364], [89064, 92799], [89064, 93195], [83370, 75408], [83370, 99481], [83370, 97790], [83370, 97790], [83370, 92479], [83370, 95788], [83370, 94264], [83370, 99481], [83370, 94859], [83370, 94364], [83370, 92799], [83370, 93195], [89024, 75408], [89024, 99481], [89024, 97790], [89024, 97790], [89024, 92479], [89024, 95788], [89024, 94264], [89024, 99481], [89024, 94859], [89024, 94364], [89024, 92799], [89024, 93195], [98996, 75408], [98996, 99481], [98996, 97790], [98996, 97790], [98996, 92479], [98996, 95788], [98996, 94264], [98996, 99481], [98996, 94859], [98996, 94364], [98996, 92799], [98996, 93195], [80463, 75408], [80463, 99481], [80463, 97790], [80463, 97790], [80463, 92479], [80463, 95788], [80463, 94264], [80463, 99481], [80463, 94859], [80463, 94364], [80463, 92799], [80463, 93195], [80108, 75408], [80108, 99481], [80108, 97790], [80108, 97790], [80108, 92479], [80108, 95788], [80108, 94264], [80108, 99481], [80108, 94859], [80108, 94364], [80108, 92799], [80108, 93195], [83822, 75408], [83822, 99481], [83822, 97790], [83822, 97790], [83822, 92479], [83822, 95788], [83822, 94264], [83822, 99481], [83822, 94859], [83822, 94364], [83822, 92799], [83822, 93195], [81916, 75408], [81916, 99481], [81916, 97790], [81916, 97790], [81916, 92479], [81916, 95788], [81916, 94264], [81916, 99481], [81916, 94859], [81916, 94364], [81916, 92799], [81916, 93195], [99635, 75408], [99635, 99481], [99635, 97790], [99635, 97790], [99635, 92479], [99635, 95788], [99635, 94264], [99635, 99481], [99635, 94859], [99635, 94364], [99635, 92799], [99635, 93195], [89072, 75408], [89072, 99481], [89072, 97790], [89072, 97790], [89072, 92479], [89072, 95788], [89072, 94264], [89072, 99481], [89072, 94859], [89072, 94364], [89072, 92799], [89072, 93195], [82926, 75408], [82926, 99481], [82926, 97790], [82926, 97790], [82926, 92479], [82926, 95788], [82926, 94264], [82926, 99481], [82926, 94859], [82926, 94364], [82926, 92799], [82926, 93195], [82082, 75408], [82082, 99481], [82082, 97790], [82082, 97790], [82082, 92479], [82082, 95788], [82082, 94264], [82082, 99481], [82082, 94859], [82082, 94364], [82082, 92799], [82082, 93195], [83070, 75408], [83070, 99481], [83070, 97790], [83070, 97790], [83070, 92479], [83070, 95788], [83070, 94264], [83070, 99481], [83070, 94859], [83070, 94364], [83070, 92799], [83070, 93195], [79954, 75408], [79954, 99481], [79954, 97790], [79954, 97790], [79954, 92479], [79954, 95788], [79954, 94264], [79954, 99481], [79954, 94859], [79954, 94364], [79954, 92799], [79954, 93195], [83627, 75408], [83627, 99481], [83627, 97790], [83627, 97790], [83627, 92479], [83627, 95788], [83627, 94264], [83627, 99481], [83627, 94859], [83627, 94364], [83627, 92799], [83627, 93195], [83437, 75408], [83437, 99481], [83437, 97790], [83437, 97790], [83437, 92479], [83437, 95788], [83437, 94264], [83437, 99481], [83437, 94859], [83437, 94364], [83437, 92799], [83437, 93195], [81550, 75408], [81550, 99481], [81550, 97790], [81550, 97790], [81550, 92479], [81550, 95788], [81550, 94264], [81550, 99481], [81550, 94859], [81550, 94364], [81550, 92799], [81550, 93195], [83772, 75408], [83772, 99481], [83772, 97790], [83772, 97790], [83772, 92479], [83772, 95788], [83772, 94264], [83772, 99481], [83772, 94859], [83772, 94364], [83772, 92799], [83772, 93195], [72481, 75408], [72481, 99481], [72481, 97790], [72481, 97790], [72481, 92479], [72481, 95788], [72481, 94264], [72481, 99481], [72481, 94859], [72481, 94364], [72481, 92799], [72481, 93195], [89066, 75408], [89066, 99481], [89066, 97790], [89066, 97790], [89066, 92479], [89066, 95788], [89066, 94264], [89066, 99481], [89066, 94859], [89066, 94364], [89066, 92799], [89066, 93195], [70195, 75408], [70195, 99481], [70195, 97790], [70195, 97790], [70195, 92479], [70195, 95788], [70195, 94264], [70195, 99481], [70195, 94859], [70195, 94364], [70195, 92799], [70195, 93195], [99511, 75408], [99511, 99481], [99511, 97790], [99511, 97790], [99511, 92479], [99511, 95788], [99511, 94264], [99511, 99481], [99511, 94859], [99511, 94364], [99511, 92799], [99511, 93195], [82757, 75408], [82757, 99481], [82757, 97790], [82757, 97790], [82757, 92479], [82757, 95788], [82757, 94264], [82757, 99481], [82757, 94859], [82757, 94364], [82757, 92799], [82757, 93195], [99495, 75408], [99495, 99481], [99495, 97790], [99495, 97790], [99495, 92479], [99495, 95788], [99495, 94264], [99495, 99481], [99495, 94859], [99495, 94364], [99495, 92799], [99495, 93195], [80333, 75408], [80333, 99481], [80333, 97790], [80333, 97790], [80333, 92479], [80333, 95788], [80333, 94264], [80333, 99481], [80333, 94859], [80333, 94364], [80333, 92799], [80333, 93195], [71887, 75408], [71887, 99481], [71887, 97790], [71887, 97790], [71887, 92479], [71887, 95788], [71887, 94264], [71887, 99481], [71887, 94859], [71887, 94364], [71887, 92799], [71887, 93195], [98795, 75408], [98795, 99481], [98795, 97790], [98795, 97790], [98795, 92479], [98795, 95788], [98795, 94264], [98795, 99481], [98795, 94859], [98795, 94364], [98795, 92799], [98795, 93195]]
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
  for i, ID in enumerate(pair):
    mesh = createMesh(ID)
    c = univ.createContent(mesh, str(ID))
    univ.addContent(c)
    if i ==0:
      c.setColor(Color3f(Color.BLUE))

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
