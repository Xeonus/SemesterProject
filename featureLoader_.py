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
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 73544, 73675, 72743, 74434, 89208, 99580, 71887]
  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75949, 76718, 75854, 76923, 89606, 92796, 75408]
  wrongIDs1=[89385, 76052, 89088, 77829, 87617, 98723, 99083, 73337, 99370, 83486, 99370, 99316, 85573]
  wrongIDs2=[78763, 82591, 89094, 79740, 90045, 98916, 96536, 99501, 93400, 97790, 99316, 96733, 74732]
  
"""



#----------PCA AND SPHERECOUNT AS A TRAINING VECTOR --------

def pcaSpheretrainer(numiter, biniter):
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434, 89208, 99580, 99455, 99580]
  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923, 89606, 92796, 99501, 99640]
  wrongIDs1=[77161, 76052, 70195, 89088, 77829, 81321, 83589, 87617, 98723, 99083, 73337, 99370, 83486, 99370, 99316, 81196]
  wrongIDs2=[77155, 82591, 83068, 89094, 79740, 81032, 85171, 90045, 98916, 96536, 99501, 93400, 97790, 99316, 96733, 97790]
  matching = pcaSphereList(treeIDsleft, treeIDsright, biniter)
  nonmatching=pcaSphereList(wrongIDs1, wrongIDs2, biniter)
  numTrees = numiter #number of trees in randomForest
  numFeatures = len(matching.values()[0])
  classifier = createClassifier(numTrees, numFeatures + 1) # +1 to include the class
  outofbag = trainClassifier(classifier, matching.values(), nonmatching.values())

  """
  #--------------------List of possible tests--------------
  print "lch55 left right:", classify(classifier, [pcaSphereList([72481], [99481], biniter).values()[0]])
  print "random against random tree:", classify(classifier, [pcaSphereList([87617], [77155], biniter).values()[0]])
  print "lesA against other lesA:", classify(classifier, [pcaSphereList([73337], [75616], biniter).values()[0]])
  print "false positive match?:", classify(classifier, [pcaSphereList([83486], [97790], biniter).values()[0]])
  print "small fragment vs big:", classify(classifier, [pcaSphereList([99370], [93400], biniter).values()[0]])
  print "handle against other:", classify(classifier, [pcaSphereList([99580], [99640], biniter).values()[0]])
  """

  return outofbag #, classifier


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
  
  return outofbag, classifier