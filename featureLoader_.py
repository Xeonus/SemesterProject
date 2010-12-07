from math import sqrt
from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from profilingFixedCoordinates import getDendriticProfiles
from profilingFixedCoordinates import getNodeCoordinates
from machine_ import featureVector, rawHistogramVector, rawFeatureVector, pcaSphereVector,  createClassifier, trainClassifier, classify
from machine_ import iddict

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
  #-----------OLD ROBUST TRAINING SET----------------------------------
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434]
  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923]
  wrongIDs1=[77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723, 99083]
  wrongIDs2=[77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916, 96536]

  #----------NEW TRAINING SET------------------------------------------
  treeIDsleft=[76408, 79954, 74504, 99635, 99431, 89060, 74329]
  treeIDsright=[73230, 92479, 76825, 95668, 99495, 89046, 77041]
  wrongIDs1=[88107, 89046, 94359, 99635, 91993, 74504, 83070]
  wrongIDs2=[89060, 74329, 96733, 83070, 78763, 82897, 73230]

  #-----------OLD TRAINING SET ON NEW MERGED XML FILE (02-12-2010)-----
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434, 79954]
  treeIDsright=[75616, 75783, 76408, 76825, 105203, 74877, 75408, 75949, 76718, 75854, 77041, 76923, 92479]
  wrongIDs1=[77161, 76052, 70195, 89088, 77829, 81321, 89147, 83589, 88107, 94359, 98723, 99045, 99118]
  wrongIDs2=[77155, 82591, 83068, 89094, 79740, 81032, 89245, 85171, 89060, 96733, 101155, 87617, 77177]

"""




#######################################################
#  FUNCTIONS TO LOOK AT THE BEHAVIOUR OF THE OUT OF   #
#  BAG ERROR AND TO BE ABLE TO LOAD THE DATA          #
#  INTO THE RANDOMSEED FUNCTION                       #
#######################################################

#---------- call a featurevector in function and print the oob of it --------
# possible inputs for function: rawFeatureList, featureList, pcaSphereVector

def featuretrainer(f, numiter, biniter, seeds):
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434, 79954]
  treeIDsright=[75616, 75783, 76408, 76825, 105203, 74877, 75408, 75949, 76718, 75854, 77041, 76923, 92479]
  wrongIDs1=[77161, 76052, 70195, 89088, 77829, 81321, 89147, 83589, 88107, 94359, 98723, 99045, 99118]
  wrongIDs2=[77155, 82591, 83068, 89094, 79740, 81032, 89245, 85171, 89060, 96733, 101155, 87617, 77177]
  matching = f(treeIDsleft, treeIDsright, biniter)
  nonmatching=f(wrongIDs1, wrongIDs2, biniter)
  numTrees = numiter #number of trees in randomForest
  numFeatures = len(matching.values()[0])
  classifier = createClassifier(numTrees, numFeatures + 1, seeds) # +1 to include the class
  outofbag = trainClassifier(classifier, matching.values(), nonmatching.values())

  """
  #--------------------List of possible tests--------------
  print "lch55 left right:", classify(classifier, [featureList([72481], [105203], biniter).values()[0]])
  print "random against random tree:", classify(classifier, [featureList([87617], [77155], biniter).values()[0]])
  print "lesA against other lesA:", classify(classifier, [featureList([73337], [75616], biniter).values()[0]])
  print "false positive match?:", classify(classifier, [featureList([83486], [97790], biniter).values()[0]])
  #print "small fragment vs big:", classify(classifier, [featureList([99370], [93400], biniter).values()[0]])
  #print "handle against other:", classify(classifier, [featureList([99580], [99640], biniter).values()[0]])
  """

  return outofbag




def rdmoob(f, numiter, biniter):
  """
  Calculate the mean oob and the standart deviation for 100 randomly
  generated seeds when the trainingset is generated and print those values
  """
  #-------------randomly generated seeds--------------------------------------
  seeds = [835, 942, 548, 331, 20, 476, 736, 235, 554, 951, 99, 562, 
  982, 760, 37, 517, 468, 676, 36, 387, 613, 547, 495, 37, 338, 453, 16, 49, 
  784, 156, 123, 234, 360, 670, 456, 263, 346, 112, 259, 101, 910, 769, 348, 
  807, 998, 525, 853, 978, 350, 319, 678, 800, 754, 350, 72, 248, 794, 98, 662, 
  402, 535, 69, 32, 295, 972, 339, 250, 932, 660, 621, 749, 344, 587, 589, 611, 
  644, 239, 603, 642, 35, 823, 840, 545, 641, 754, 58, 167, 864, 877, 861, 43, 
  666, 336, 405, 410, 830, 675, 917, 443, 768]
  #----------------------------------------------------------------------------
  oobs=[]
  for seed in seeds:
    oob = float(featuretrainer(f, numiter, biniter, seed))
    oobs.append(oob)
    
  n, mean, std = len(oobs), 0, 0
  for a in oobs:
    mean = mean + a
  mean = mean / float(n)
  for a in oobs:
    std = std + (a - mean)**2
  std = sqrt(std / float(n-1))

  return "meanoob +/- stdev =", mean, "+/-", std

#print rdmoob(featureList, 500, 150)
