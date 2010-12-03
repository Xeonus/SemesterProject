#k-fold cross validation of training set
from math import sqrt
from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from profilingFixedCoordinates import getDendriticProfiles
from profilingFixedCoordinates import getNodeCoordinates
from machine_ import featureVector, rawFeatureVector, createClassifier, trainClassifier, classify
from featureLoader_ import pcaSphereList, rawFeatureList, featureList
"""
#----------OLD Training set----------
treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434]
treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923]
wrongIDs1=[77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723, 99083]
wrongIDs2=[77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916, 96536]
#------------------------------------
#---------NEW BIG LIST---------------
treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434,76408, 79954, 74504, 99635, 99431, 89060, 74329]
treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923,73230, 92479, 76825, 95668, 99495, 89046, 77041]
wrongIDs1=[77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723, 99083, 88107, 89046, 94359, 99635, 91993, 74504, 83070]
wrongIDs2=[77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916, 96536, 89060, 74329, 96733, 83070, 78763, 82897, 73230]
#------------------------------------
"""
treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434, 79954, 74504]
treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923, 92479, 76825]
wrongIDs1=[77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723, 99083, 88107, 94359]
wrongIDs2=[77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916, 96536, 89060, 96733]


def kfold(mleft, mright, nmleft, nmright, numtree, biniter):
  """ 
  Defines a kfold cross-validation method where T is the dataset 
  to train the RandomForest algorithm and k is a subelement of T which 
  then is tested on training-set T
  """
  matchesleft = mleft
  matchesright = mright
  nonmatchesleft = nmleft
  nonmatchesright = nmright
  matchresult=[]
  nonmatchresult=[]
  oob=0
  
  for ids in range(0, len(treeIDsleft)):
    biniter=biniter
    matchlistleft=[]
    matchlistright=[]
    nonmatchlistleft=[]
    nonmatchlistright=[]

    for ID in range(0, len(matchesleft)):
      if matchesleft[ID] == matchesleft[ids]:
        continue
      else:
        matchlistleft.append(matchesleft[ID])
        
    for ID in range(0, len(matchesleft)):
      if matchesright[ID] == matchesright[ids]:
        continue
      else:
        matchlistright.append(matchesright[ID])

    for ID in range(0, len(matchesleft)):
      if nonmatchesleft[ID] == nonmatchesleft[ids]:
        continue
      else:
        nonmatchlistleft.append(nonmatchesleft[ID])

    for ID in range(0, len(matchesleft)):
      if nonmatchesright[ID] == nonmatchesright[ids]:
        continue
      else:
        nonmatchlistright.append(nonmatchesright[ID])

    kmatch =[matchesleft[ids], matchesright[ids]]
    knonmatch= [nonmatchesleft[ids], nonmatchesright[ids]]
    matching = featureList(matchlistleft, matchlistright, biniter)
    nonmatching = featureList(nonmatchlistleft, nonmatchlistright, biniter)  
    numTrees = numtree
    numFeatures = len(matching.values()[0])
    classifier = createClassifier(numTrees, numFeatures + 1) # +1 to include the class
    outofbag = trainClassifier(classifier, matching.values(), nonmatching.values())
    oob+=float(outofbag)
    print "oob =", outofbag
    print "kth element of matches tested against training set:", classify(classifier, [featureList([kmatch[0]], [kmatch[1]], biniter).values()[0]])
    print "kth element of nonmatches tested against training set:", classify(classifier, [featureList([knonmatch[0]], [knonmatch[1]], biniter).values()[0]])
    matchresult.append(classify(classifier, [featureList([kmatch[0]], [kmatch[1]], biniter).values()[0]]))
    nonmatchresult.append(classify(classifier, [featureList([knonmatch[0]], [knonmatch[1]], biniter).values()[0]]))

  #print matchresult
  #print nonmatchresult   
  counter=0
  for m in matchresult:
    if m[0] == 1.0:
      counter+=1
  for m in nonmatchresult:
    if m[0] == 0.0:
      counter +=1
  elements = 2 * len(matchresult)
  performance = (float(counter) / float(elements))
  moob = oob / float(elements / 2)  
  return "The performance is:", performance, "and the mean oob is:", moob

print kfold(treeIDsleft, treeIDsright, wrongIDs1, wrongIDs2, 500,  50)
