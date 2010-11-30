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

#----------Functions for branchwise analysis / Backbone extraction-------------

def asSequence(nds):
  """ Take a list of nodes that are known to define a branch and return a list of nodes sorted by parent-child. """
  if 1 == len(nds) or 2 == len(nds):
    return nds  
  ends = []
  nds = HashSet(nds)
  for nd in nds:
    children = nd.getChildren().keySet()
    children.retainAll(nds)
    # If the parent is in the set,
    if nds.contains(nd.parent):
      # ... and does not have children in the set
      if 0 == children.size():
        # Then it's an end
        ends.append(nd)
    # Else if the parent is not in the set
    else:
      # ... but it has at least one child in the set
      if 1 == children.size():
        # then it's an end
        ends.append(nd)
  #print "ends:", len(ends)
  #print ends
  return Node.findPath(ends[0], ends[1])

def getBranches(tree):
  tree = Display.getFront().getLayerSet().findById(tree)
  """ Return a list of remaining branch vertices and lists of lists of Point3f, each inner list representing a branch with Point3d. """
  m = tree.asVertices() # map of Node keys vs. Vertex values
  steps = Centrality.branchWise(m.values(), 2)
  branches = []
  for step in steps:
    s = []
    for branch in step.branches:
      nds = [vertex.data for vertex in branch]
      b = []
      for nd in asSequence(nds):
        # transfrom nd to Point3d
        calibration = tree.getLayerSet().getCalibration()
        affine = tree.getAffineTransform()
        fp = array([nd.getX(), nd.getY()], 'f')
        affine.transform(fp, 0, fp, 0, 1)
        x = fp[0] * calibration.pixelWidth
        y = fp[1] * calibration.pixelHeight
        z = nd.getLayer().getZ() * calibration.pixelWidth
        tfm = correct([x, y, z])
        p = Point3d(tfm[0], tfm[1], tfm[2])    #and transform in new coordinates  
        b.append(p)
      s.append(b)
    branches.append([step.remaining_branch_vertices, s])
  return branches

def asVectorString(tree): #only looks now at backbone
  """ Given a sorted sequence of Point3d, return a new VectorString3D """
  #Convert list of list of list of list into list with coordinates
  branches = getBranches(tree)
  treeList = branches[-1] #BACKBONE!!
  listList = treeList[1]
  coords = listList[0]
  n = len(coords)
  x = zeros(n, 'd')
  y = zeros(n, 'd')
  z = zeros(n, 'd')
  vectors=[]
  for i in range(n):
    p = coords[i]
    x[i] = p.x
    y[i] = p.y
    z[i] = p.z
  return VectorString3D(x, y, z, 0) #do mirror operation for other tree!

def asVectorStringMirror(tree):
  """ Given a sorted sequence of Point3d, return a new VectorString3D of mirrored sequence """
  #Convert list of list of list of list into list with coordinates
  branches = getBranches(tree)
  treeList = branches[-1] #BACKBONE!!
  listList = treeList[1]
  coords = listList[0]
  n = len(coords)
  x = zeros(n, 'd')
  y = zeros(n, 'd')
  z = zeros(n, 'd')
  vectors=[]
  for i in range(n):
    p = coords[i]
    x[i] = (-1) * p.x
    y[i] = p.y
    z[i] = p.z  
  return VectorString3D(x, y, z, 0)

#print asVectorStringMirror(99684)

#---------Values of getStatistics() Output -----------
"""
Returns {average distance, cummulative distance, stdDev, median, prop_mut} which are:
[0] - average distance: the average physical distance between mutation pairs
[1] - cummulative distance: the sum of the distances between mutation pairs
[2] - stdDev: of the physical distances between mutation pairs relative to the average
[3] - median: the average medial physical distance between mutation pairs, more robust than the average to extreme values
[4] - prop_mut: the proportion of mutation pairs relative to the length of the queried sequence vs1.
[5] - Levenshtein's distance
[6] - Similarity:  1 - (( N_insertions + N_deletions ) / max(len(seq1), len(seq2)))
[7] - Proximity: cummulative distance between pairs divided by physical sequence length
[8] - Proximity of mutation pairs
[9] - Ratio of sequence lengths: vs1.length / vs2.length
[10] - Tortuosity: squared ratio of the difference of the euclidian distances from first to last point divided by the euclidian length of the sequence.
"""

def compareVectorStrings(vs1, vs2, resample):
  vs1 = asVectorString(vs1)
  vs2 = asVectorStringMirror(vs2) #if asVectorStringMirror: has to be from other side
  print vs1.length(), vs2.length()
  
  e = Editions(vs1, vs2, resample, False, 1.1, 1.1, 1.1)
  return e.getStatistics(False, 0, 0, False)

#print compareVectorStrings(71887, 75408, 1)





#------------Get all nodes of subtrees from branchwise analysis--------------------
def getNodes(tree):
  """Return a list of remaining vertices and lists of lists of all nodes representing a branch"""
  tree = Display.getFront().getLayerSet().findById(tree)
  m = tree.asVertices() # map of Node keys vs. Vertex values
  steps = Centrality.branchWise(m.values(), 2) 
  branches = []
  saveNodes = []
  for step in steps:
    for branch in step.branches:
      b = []
      branchNodes = []
      for vertex in branch:
        nd = vertex.data
        branchNodes.append(nd)
    saveNodes.append([step.remaining_branch_vertices, branchNodes])
  return saveNodes
