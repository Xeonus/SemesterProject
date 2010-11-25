from math import sqrt
from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from matrixoperator import Matrix
from javax.media.j3d import Transform3D
from javax.vecmath import Point3d
from ij.io import FileSaver
from profilingFixedCoordinates import getDendriticProfiles
from profilingFixedCoordinates import getNodeCoordinates
from machine_ import featureVector, rawFeatureVector, pcaSphereVector,  createClassifier, trainClassifier, classify

#Load list of tree pairs into function and get the featureVector as output



def featureList(treeIDsleft, treeIDsright, biniter):
  feature = {}
  fpair = []
  result = []

  for id1,id2 in zip(treeIDsleft, treeIDsright):
    fpair = featureVector(id1, id2, biniter)
    feature[str(id1) + "--" + str(id2)] = fpair
  #for ID in range(0, len(treeIDsleft)):
  #  fpair = featureVector(treeIDsleft[i], treeIDsright[i])    
  #  feature.append(fpair)
  return feature



def rawFeatureList(treeIDsleft, treeIDsright, biniter):
  rawfeature = {}
  fpair = []
  result = []
  
  for id1,id2 in zip(treeIDsleft, treeIDsright):
    fpair = rawFeatureVector(id1, id2, biniter)
    rawfeature[str(id1) + "--" + str(id2)] = fpair  
  return rawfeature


def pcaSphereList(treeIDsleft, treeIDsright, biniter):
  rawfeature = {}
  fpair = []
  result = []
  
  for id1,id2 in zip(treeIDsleft, treeIDsright):
    fpair = pcaSphereVector(id1, id2, biniter)
    rawfeature[str(id1) + "--" + str(id2)] = fpair  
  return rawfeature

"""
-----------12 Matches------------
lists of matching pairs, class=[left, right], **=suboptimal match
lesA=[73337,75616]
lesB=[73698, 75783] **
desC=[73230, 76408]
desD=[74504, 76825]
lch5-5=[72481, 99481]
lch5-3=[72295, 74877]
lch5-1=[71887, 75408]
ddaD class 1=[73544,75949]
ddaE class 1=[73675, 76718]
ddaB class 1=[72743, 75854]
ddaC class 4=[74329, 77041]
dmd1 class 1=[74434, 76923]
treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434]
treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923]
-----------------------------

---------12 Nonmatches----------
fragmentsMark=[90155, 90161]
fragments2=[90168, 90165]
wrongbranches1=[77161, 77155]
wrongbranches2=[76052, 82591]
wrongbranches3=[70195, 83068]
wrongbranches4=[89088, 89094]
basket1 vs looper3=[99495, 79187]
localmismatches=[77829, 79740]
crossA-P=[81321, 81032]
motorneurons=[89147, 89245]
fragments=[83589, 85171]
transversenerveVStargetsofdda=[87617, 90045]
wrongIDsleft=[90155, 90168, 77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617]
wrongIDsright=[90161, 90165, 77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045]

The trees to use as input pairs
1, 2/4, 2/4, 5, 3
treeIDsleft = [71887, 72064, 72175, 72481, 72295]
1, 2/4, 2/4, 5, 3
treeIDsright = [75408, 75307, 74767, 99481, 74877]
The expected correct matches
lch = featureList(treeIDsleft, treeIDsright)
The expected incorrect matches: the first list is shifted by one
wrong_lch = featureList([treeIDsleft[i] for i in [1, 0, 3, 4, 2]], treeIDsright) # shifted by one

def tester(numiter, biniter):
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434, 74434, 73337]
  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923, 74434, 73337]
  matching = featureList(treeIDsleft, treeIDsright, biniter)
  # The expected incorrect matches: recombination
  #nonmatching = featureList([treeIDsleft[i] for i in [11,4,10,5,9,6,8,3,7,0,2,1]], treeIDsright)
  wrongIDs1=[90155, 90168, 77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723]
  wrongIDs2=[90161, 90165, 77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916]
  nonmatching=featureList(wrongIDs1, wrongIDs2, biniter)
  #print "FeatureVectors for matching trees are:", "\n", matching
  numTrees = numiter #200 parameter of machine learning
  numFeatures = len(matching.values()[0])
  #print numFeatures
  #for v1,v2 in zip(matching.values(), nonmatching.values()):
  #  print len(v1), len(v2)
  classifier = createClassifier(numTrees, numFeatures + 1) # +1 to include the class
  #print len(matching.values()), len(nonmatching.values())
  outofbag = trainClassifier(classifier, matching.values(), nonmatching.values())
  
  #lesA = [73337, 75616]
  #handle=[99316, 99580]
  #print "lesA against itself:", classify(classifier, [featureList([73337], [73337], biniter).values()[0]])
  #print "lesA against handle:", classify(classifier, [featureList([73337], [99316], biniter).values()[0]])
  #print "lesA against other lesA", classify(classifier, [featureList([73337], [75616], biniter).values()[0]])
  return outofbag
"""



#----------test for approach where the pca method and the spherecount is loaded into the training vector --------

def pcaSpheretrainer(numiter, biniter):
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434]
  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923]
  matching = pcaSphereList(treeIDsleft, treeIDsright, biniter)

  wrongIDs1=[77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723, 99083]
  wrongIDs2=[77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916, 96536]
  nonmatching=pcaSphereList(wrongIDs1, wrongIDs2, biniter)
  numTrees = numiter #200 number of generated trees
  numFeatures = len(matching.values()[0])
  classifier = createClassifier(numTrees, numFeatures + 1) # +1 to include the class
  outofbag = trainClassifier(classifier, matching.values(), nonmatching.values())

  print "lch55 left right:", classify(classifier, [pcaSphereList([72481], [99481], biniter).values()[0]])
  print "random against random tree:", classify(classifier, [pcaSphereList([87617], [77155], biniter).values()[0]])
  print "lesA against other lesA:", classify(classifier, [pcaSphereList([73337], [75616], biniter).values()[0]])
  print "false positive match?:", classify(classifier, [pcaSphereList([83486], [97790], biniter).values()[0]])
  print "small fragment vs big:", classify(classifier, [pcaSphereList([99370], [93400], biniter).values()[0]])
  print "handle against other:", classify(classifier, [pcaSphereList([99580], [99640], biniter).values()[0]])


  return outofbag, classifier

#print pcaSpheretrainer(500, 100)

#-------Test for approach where raw data is put into training set--------------

def rawFeaturetrainer(numtree, biniter):
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434]
  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923]
  matching = rawFeatureList(treeIDsleft, treeIDsright, biniter)
  wrongIDs1=[77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723, 99083]
  wrongIDs2=[77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916, 96536]
  nonmatching=rawFeatureList(wrongIDs1, wrongIDs2, biniter)
  numTrees = numtree #200 number of generated trees
  numFeatures = len(matching.values()[0])
  classifier = createClassifier(numTrees, numFeatures + 1) # +1 to include the class
  outofbag = trainClassifier(classifier, matching.values(), nonmatching.values())

  print "lch55 left right:", classify(classifier, [rawFeatureList([72481], [99481], biniter).values()[0]])
  print "random against random tree:", classify(classifier, [rawFeatureList([87617], [77155], biniter).values()[0]])
  print "lesA against other lesA:", classify(classifier, [rawFeatureList([73337], [75616], biniter).values()[0]])
  print "false positive match?:", classify(classifier, [rawFeatureList([83486], [97790], biniter).values()[0]])
  print "small fragment vs big:", classify(classifier, [rawFeatureList([99370], [93400], biniter).values()[0]])
  print "handle against other:", classify(classifier, [rawFeatureList([99580], [99640], biniter).values()[0]])
  return outofbag, classifier

#print rawFeaturetrainer(500, 100)


  










