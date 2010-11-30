from math import sqrt
from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from profilingFixedCoordinates import getDendriticProfiles
from profilingFixedCoordinates import getNodeCoordinates
from machine_ import featureVector, createClassifier, trainClassifier, classify
from featureLoader_ import featureList, rawFeatureList, pcaSphereList, rawHistogramList

"""
IDvector1 has to be a list of neurons from the left side
IDvector2 has to be a list of neurons from the right side
"""

#lch5-1 left
IDvector1=[83160, 81196, 81321, 99501, 85174, 99455, 83695, 99442, 93311, 
81056, 83785, 99063, 89064, 83370, 89024, 98996, 80463, 80108, 83822, 81916, 
99635, 89072, 82926, 82082, 83070, 79954, 83627, 83437, 81550, 83772, 72481, 
89066, 70195, 99511, 82757, 99495, 80333, 71887, 98795]
#lch5-1 right
IDvector2=[95421, 98268, 93662, 97669, 75408, 94943, 95674, 99490, 97790, 
92479, 95788, 91612, 94264, 95812, 83695, 93311, 95190, 95056, 95668, 95151, 
95424, 92485, 99481, 94859, 94364, 92799, 93195, 91609, 96114, 93048, 98238, 
93883, 95887, 93582, 94359, 96513, 93400, 95246]


#Compare one entry of IDvector1 with all the other entries of IDvector2.
#If there is a match, output the corresponding IDs as a list [ID1, ID2]

def profilematches(IDvector1, IDvector2, numtree, biniter):
  matches=[]
  #----------Training set------------
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434]
  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923]
  wrongIDs1=[77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723, 99083]
  wrongIDs2=[77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916, 96536]
  
  matching = pcaSphereList(treeIDsleft, treeIDsright, biniter)
  nonmatching = pcaSphereList(wrongIDs1, wrongIDs2, biniter)
  numTrees = numtree #200 number of generated trees
  numFeatures = len(matching.values()[0])
  classifier = createClassifier(numTrees, numFeatures + 1) # +1 to include the class
  outofbag = trainClassifier(classifier, matching.values(), nonmatching.values())
  print "The out of bag error is:", outofbag
  for i in range(0, len(IDvector1)):
    for j in range(0, len(IDvector2)):
      if classify(classifier, [pcaSphereList([IDvector1[i]], [IDvector2[j]], biniter).values()[0]]) == [1.0]:
        match=[IDvector1[i], IDvector2[j]]
        print match
        matches.append(match)
  return matches

print profilematches(IDvector1, IDvector2, 500, 50)
