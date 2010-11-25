from math import sqrt
from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from profilingFixedCoordinates import getDendriticProfiles
from profilingFixedCoordinates import getNodeCoordinates
from machine_ import featureVector, createClassifier, trainClassifier, classify
from featureLoader_ import featureList, rawFeatureList, pcaSphereList

#lch5-5 left
IDvector1=[81726, 99771, 99665, 81196, 99519, 99316, 99370, 80317, 99455, 83780, 98971, 
99442, 93311, 98730, 99063, 98929, 89064, 80584, 83486, 98982, 98720, 99348, 99696, 72679, 
99427, 99766, 98882, 82011, 81772, 98268, 81321, 99306, 99092, 99213, 99679, 83695, 99072, 
81886, 81769, 99194, 99200, 98792, 99668, 83677, 98996, 99083, 99216, 99640, 98629, 99095, 
98707, 81739, 83822, 99223, 99617, 72615, 98723, 83070, 99522, 72597, 99283, 98968, 83600, 
99705, 72481, 83772, 81972, 81732, 98913, 70195, 77177, 98733, 99511, 98955, 99580, 71887, 
81969, 81723, 98795, 99684, 99197, 99516, 98932, 99089, 83668, 81916, 99635, 99066, 99203, 
98916, 80741, 83627, 99290, 99267, 99313, 99569, 89066, 98860, 99086, 99495, 80723, 72633]
#lch5-5 right
IDvector2=[97549, 98383, 95421, 98268, 97669, 75408, 94943, 99316, 95674, 96647, 91869, 
97790, 75108, 75466, 92479, 97542, 96580, 91612, 75298, 95812, 91704, 94264, 98494, 83695, 
75193, 97060, 75078, 95000, 97423, 95190, 91884, 95151, 95424, 93131, 98345, 91848, 99481, 
97607, 75169, 97779, 75184, 75102, 97559, 97623, 93195, 91609, 97063, 93048, 98238, 97066, 
99431, 93862, 75096, 96733, 75268, 83000, 97562, 93883, 94948, 93582, 96875, 97572, 93400, 
97073, 96575, 95246, 91973, 98263]


#Idea: compare one entry of list1 with all the other entries of list2.
#If there is a match, output the corresponding IDs

def profilematches(IDvector1, IDvector2, numtree, biniter):
  matches=[]
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434]
  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923]
  matching = pcaSphereList(treeIDsleft, treeIDsright, biniter)
  wrongIDs1=[77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723, 99083]
  wrongIDs2=[77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916, 96536]
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

print profilematches(IDvector1, IDvector2, 500, 100)
