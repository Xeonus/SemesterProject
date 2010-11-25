#Invariant tree-analysis with the PCA method
from math import sqrt  
from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from matrixoperator import Matrix
from javax.media.j3d import Transform3D
from javax.vecmath import Point3d
#from org.jfree.data.statistics import HistogramDataset

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

#--------PCA-------------
def pca(ID, biniter):
  tree = Display.getFront().getLayerSet().findById(ID)

  #Calculate the center of mass
  center = Matrix( [[0,0,0]] )
  coords = Matrix(getNodeCoordinates(tree))
  m=coords.getRowDimension()

  for i in range(0, coords.getRowDimension()):
    center += Matrix([coords.getRow( i )])
  center /= float(m)

  #print center

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

  #Count number of nodes which fall in defined interval of pca projection -> has to be fixed globally when to compare PCAs!
  counter = 0
  histovector = []
  pca=[ x[0] for x in pca] #get it back in array form (get rid of list in list)
  binleft = -12500 #binleft = min(pca)
  iterations = biniter
  length = int(25000/iterations + 0.5) #int((max(pca)-min(pca))/iterations + 0.5)
  binright = binleft + length

  for i in range(0,iterations):
    for i in range(0, len(pca)):
      if pca[i] <= binright and pca[i] >= binleft:
        counter += 1    
    histovector.append(counter)
    counter=0
    binleft+=length
    binright+=length
  #print "The histogram vector is:", histovector
  return histovector

#print pca(93400, 10)

"""
def pcaFeatures(id1, id2, biniter):
  histo1 = pca(id1, biniter)
  histo2 = pca(id2, biniter)
  histos = histo1 + histo2
  return histos
 
def pcaList(treeIDsleft, treeIDsright, biniter):
  pcafeature = {}
  fpair = []
  result = []
  
  for id1,id2 in zip(treeIDsleft, treeIDsright):
    fpair = pcaFeatures(id1, id2, biniter)
    pcafeature[str(id1) + "--" + str(id2)] = fpair  
  return pcafeature


#------test of training set--------
def pcatrainer(numtree, biniter):
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434]
  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923]
  matching = pcaList(treeIDsleft, treeIDsright, biniter)
  wrongIDs1=[90168, 77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723, 99083]
  wrongIDs2=[90165, 77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916, 96536]
  nonmatching=pcaList(wrongIDs1, wrongIDs2, biniter)
  numTrees = numtree #200 number of generated trees
  numFeatures = len(matching.values()[0])
  classifier = createClassifier(numTrees, numFeatures + 1) # +1 to include the class
  outofbag = trainClassifier(classifier, matching.values(), nonmatching.values())

  #print "lesA against itself:", classify(classifier, [pcaList([73337], [73337], biniter).values()[0]])
  #print "random against random tree:", classify(classifier, [pcaList([87617], [77155], biniter).values()[0]])
  #print "lesA against other lesA", classify(classifier, [pcaList([73337], [75616], biniter).values()[0]])
  return outofbag, classifier

#-------------PCA comparison script---------------------
#lch5-1 left
IDvector1=[83756, 83160, 81726, 85171, 81196, 81939, 83660, 81321, 85199, 77324, 99501, 81955, 
80324, 85174, 99455, 80317, 99449, 83759, 83695, 83753, 99442, 81056, 83785, 99063, 98929, 83674, 
83677, 80413, 89064, 83486, 83370, 81942, 89024, 83662, 98996, 83671, 80463, 99083, 83665, 80108, 
81739, 83822, 83668, 81916, 83421, 99635, 72026, 79740, 89072, 83692, 82082, 82926, 83070, 91249, 
79954, 83627, 83437, 89034, 81932, 81550, 83600, 72481, 83772, 81972, 99486, 81732, 89066, 70485, 
83743, 70195, 99511, 83589, 82757, 99495, 80333, 71887, 85196, 98795, 81723]

#lch5-1 right
IDvector2=[83737, 93403, 92482, 98268, 95421, 93662, 75469, 97669, 75408, 94943, 95674, 99490, 97790, 
92479, 95788, 93550, 97542, 91612, 94264, 95812, 95010, 83695, 95000, 95190, 95056, 95151, 95668, 95424, 
91848, 92485, 95799, 96341, 99481, 94845, 92028, 93578, 94992, 94859, 93573, 96536, 96370, 94364, 91997, 
93195, 95802, 96114, 91609, 91686, 93048, 98238, 99431, 75096, 93862, 92031, 95007, 95877, 89034, 93883, 
93092, 94948, 96526, 95887, 93582, 94359, 95809, 96513, 93592, 93400, 95246, 95180, 96229]


#Idea: compare one entry of list1 with all the other entries of list2.
#If there is a match, output the corresponding IDs

def pcamatches(IDvector1, IDvector2, numtree, biniter):
  matches=[]
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434]
  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923]
  matching = pcaList(treeIDsleft, treeIDsright, biniter)
  wrongIDs1=[90168, 77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723]
  wrongIDs2=[90165, 77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916]
  nonmatching=pcaList(wrongIDs1, wrongIDs2, biniter)
  numTrees = numtree #200 number of generated trees
  numFeatures = len(matching.values()[0])
  classifier = createClassifier(numTrees, numFeatures + 1) # +1 to include the class
  outofbag = trainClassifier(classifier, matching.values(), nonmatching.values())
  print "The out of bag error is:", outofbag
  for i in range(0, len(IDvector1)):
    for j in range(0, len(IDvector2)):
      if classify(classifier, [pcaList([IDvector1[i]], [IDvector2[j]], biniter).values()[0]]) == [1.0]:
        match=[IDvector1[i], IDvector2[j]]
        print match
        matches.append(match)
  return matches

print pcamatches(IDvector1, IDvector2, 500, 500)











#Plotting

#Plot center
from java.awt import Color
from ini.trakem2.display import Display3D
Display3D.addFatPoint("eigen center", tree.getLayerSet(), center.get(0, 0), center.get(0, 1), center.get(0, 2), 10, Color.red)


plot = Plot("histogram", "bins", "count", range(100), pca(71887, 100))
plot.show()
fs=FileSaver(plot.getImagePlus())
fs.saveAsPng(System.getProperty("user.home") + "/Desktop/Histotest/pcaleft" + str(ID) + ".png")

histovector.reverse()
plot = Plot("histogram", "bins", "count", range(iterations), histovector)
plot.show()
fs=FileSaver(plot.getImagePlus())
fs.saveAsPng(System.getProperty("user.home") + "/Desktop/Histotest/pcaright" + str(ID) + ".png")
"""