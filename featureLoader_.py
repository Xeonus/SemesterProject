from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from profilingFixedCoordinates import getDendriticProfiles
from profilingFixedCoordinates import getNodeCoordinates
from machine_ import featureVector, rawHistogramVector, rawFeatureVector, pcaSphereVector,  createClassifier, trainClassifier, classify

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

def rawHistogramList(treeIDsleft, treeIDsright, biniter):
  rawfeature = {}
  fpair = []
  result = []
  
  for id1,id2 in zip(treeIDsleft, treeIDsright):
    fpair = rawHistogramVector(id1, id2, biniter)
    rawfeature[str(id1) + "--" + str(id2)] = fpair  
  return rawfeature


"""

  #-----------OLD ROBUST TRAINING SET---------------------
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434]
  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923]
  wrongIDs1=[77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723, 99083]
  wrongIDs2=[77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916, 96536]

  #----------NEW TRAINING SET----------------------
  treeIDsleft=[76408, 79954, 74504, 99635, 99431, 89060, 74329]
  treeIDsright=[73230, 92479, 76825, 95668, 99495, 89046, 77041]
  wrongIDs1=[88107, 89046, 94359, 99635, 91993, 74504, 83070]
  wrongIDs2=[89060, 74329, 96733, 83070, 78763, 82897, 73230]
  
"""



#----------Features 1 to 4 AS A TRAINING VECTOR --------

def featuretrainer(numiter, biniter):
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434, 79954, 74504]
  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923, 92479, 76825]
  wrongIDs1=[77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723, 99083, 88107, 94359]
  wrongIDs2=[77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916, 96536, 89060, 96733]
  matching = featureList(treeIDsleft, treeIDsright, biniter)
  nonmatching=featureList(wrongIDs1, wrongIDs2, biniter)
  numTrees = numiter #number of trees in randomForest
  numFeatures = len(matching.values()[0])
  classifier = createClassifier(numTrees, numFeatures + 1) # +1 to include the class
  outofbag = trainClassifier(classifier, matching.values(), nonmatching.values())

  """
  #--------------------List of possible tests--------------
  print "lch55 left right:", classify(classifier, [featureList([72481], [99481], biniter).values()[0]])
  print "random against random tree:", classify(classifier, [featureList([87617], [77155], biniter).values()[0]])
  print "lesA against other lesA:", classify(classifier, [featureList([73337], [75616], biniter).values()[0]])
  print "false positive match?:", classify(classifier, [featureList([83486], [97790], biniter).values()[0]])
  print "small fragment vs big:", classify(classifier, [featureList([99370], [93400], biniter).values()[0]])
  print "handle against other:", classify(classifier, [featureList([99580], [99640], biniter).values()[0]])
  """

  return outofbag #, classifier


#print featuretrainer(500, 50)




#-------RAW DATA AS A TRAINING VECTOR--------------

def rawFeaturetrainer(numtree, biniter):
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434]
  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923]
  wrongIDs1=[77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723, 99083]
  wrongIDs2=[77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916, 96536]
  matching = rawFeatureList(treeIDsleft, treeIDsright, biniter)
  nonmatching=rawFeatureList(wrongIDs1, wrongIDs2, biniter)
  numTrees = numtree #200 number of generated trees
  numFeatures = len(matching.values()[0])
  classifier = createClassifier(numTrees, numFeatures + 1) # +1 to include the class
  outofbag = trainClassifier(classifier, matching.values(), nonmatching.values())

  """
  #--------------------List of possible tests--------------
  print "lch55 left right:", classify(classifier, [rawFeatureList([72481], [99481], biniter).values()[0]])
  print "random against random tree:", classify(classifier, [rawFeatureList([87617], [77155], biniter).values()[0]])
  print "lesA against other lesA:", classify(classifier, [rawFeatureList([73337], [75616], biniter).values()[0]])
  print "false positive match?:", classify(classifier, [rawFeatureList([83486], [97790], biniter).values()[0]])
  print "small fragment vs big:", classify(classifier, [rawFeatureList([99370], [93400], biniter).values()[0]])
  print "handle against other:", classify(classifier, [rawFeatureList([99580], [99640], biniter).values()[0]])
  """
  
  return outofbag #, classifier

#print rawFeaturetrainer(500, 50)