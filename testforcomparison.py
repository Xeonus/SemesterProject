from math import sqrt
from ini.trakem2.display import Display
from jarray import array
import sys
import os
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from profilingFixedCoordinates import getDendriticProfiles
from profilingFixedCoordinates import getNodeCoordinates
from machine_ import featureVector, createClassifier, trainClassifier, classify
from featureLoader_ import featureList, rawFeatureList, pcaSphereList, rawHistogramList
from machine_ import iddict

"""
IDvector1 has to be a list of neurons from the left side
IDvector2 has to be a list of neurons from the right side
"""

#lch5-1 left
lch51l=[83160, 81321, 105311, 99501, 85174, 98494, 99455, 99442, 93311, 81056, 
83785, 105166, 89064, 98996, 80463, 80108, 83822, 81916, 89072, 101157, 100823, 82926, 
82082, 83070, 79954, 83627, 83437, 81550, 72481, 77167, 89066, 70195, 105193, 99511, 
100714, 82757, 80333, 71887, 98795]

#lch5-1 right
lch51r=[95421, 75408, 94943, 95674, 99490, 92479, 91612, 99958, 95010, 93311, 
99784, 99898, 100515, 95190, 105166, 95056, 95668, 95151, 95424, 92485, 92799, 94364, 
98268, 93662, 97669, 99867, 97790, 100400, 95788, 94264, 94859, 100131, 100550, 93195, 
96114, 91609, 93048, 98238, 99943, 100818, 100314, 105203, 100091, 99821, 95887, 93582, 
97572, 94359, 100162, 96513, 95246, 99648]

#lch5-5 left
lch55l=[98882, 100346, 98268, 99316, 105311, 99501, 98494, 99455, 99442, 93311, 
99194, 99898, 99063, 105166, 89064, 100978, 101155, 98996, 83822, 99223, 100847, 
83070, 72481, 77167, 100868, 70195, 77177, 98733, 99511, 100714, 71887, 98795, 
100865, 81916, 101157, 101147, 83627, 89066]

lch55r=[100346, 95421, 75408, 99316, 95674, 92479, 96580, 91612, 98494, 99958, 
99784, 100515, 97423, 99898, 95190, 105166, 95424, 95151, 100270, 99981, 97607, 
99755, 92799, 100552, 98268, 97669, 99867, 96647, 97790, 100400, 94264, 105157, 
100140, 98345, 99850, 100131, 93195, 91609, 93048, 96733, 99769, 100818, 100314, 
99821, 93582, 97572, 99603, 97073, 95246, 99648, 97623, 100550, 98238, 100456, 
99590, 99943, 105203, 100091, 100162]

l5155 = [93311, 105166]
r5155 = [100346, 98268, 99316, 98494, 99898, 105166]



#Compare one entry of IDvector1 with all the other entries of IDvector2.
#If there is a match, output the corresponding IDs as a list [ID1, ID2]

#f is a featurevector to call: either featureList, pcaSphereList, rawHistogramList, rawFeatureList

def profilematches(f, IDvector1, IDvector2, numtree, biniter, seeds):
  matches=[]
  allmatches=[]
  #----------OLD Training set------------
  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434, 79954]
  treeIDsright=[75616, 75783, 76408, 76825, 105203, 74877, 75408, 75949, 76718, 75854, 77041, 76923, 92479]
  wrongIDs1=[77161, 76052, 70195, 89088, 77829, 81321, 89147, 83589, 88107, 94359, 98723, 99045, 99118]
  wrongIDs2=[77155, 82591, 83068, 89094, 79740, 81032, 89245, 85171, 89060, 96733, 101155, 87617, 77177]

  matching = f(treeIDsleft, treeIDsright, biniter)
  nonmatching = f(wrongIDs1, wrongIDs2, biniter)
  numTrees = numtree
  numFeatures = len(matching.values()[0])
  classifier = createClassifier(numTrees, numFeatures + 1, seeds) # +1 to include the class
  outofbag = trainClassifier(classifier, matching.values(), nonmatching.values())
  #print "The out of bag error is:", outofbag
  for id1 in IDvector1:
    m=[]
    fcl=[]
    for id2 in IDvector2:
      fclass = classify(classifier, [f([id1], [id2], biniter).values()[0]])
      if fclass[0] == 1.0:
        match = [id1, id2]
        allmatches.append(match)
        visualMatch = [id1, id2, fclass]
        #print "A match:", visualMatch
        m.append(match)
        fcl.append(fclass)
    if m == []:
      continue
    else:
      m = m[fcl.index(max(fcl))]
      #print "High confidence match", m       
      matches.append(m)
  #print "The matches with HIGHEST DISTRIBUTION CONFIDENCE:",matches
  #print "All found matches:", allmatches
  return allmatches
  
#print profilematches(featureList, IDvector1, IDvector2, 500, 50, 123)


#run the randomForest algorithm 100 times with a randomly generated seed-list
#and search for those pairs, that are found in all 100 runs
#save the dictionary of all runs and the result in 2 textfiles in the result folder

def rdmSeedRuns(f, IDvector1, IDvector2, numtree, biniter):
  
  seedresults={}
  #-------------randomly generated seeds--------------------------------------
  seeds = [835, 942, 548, 331, 20, 476, 736, 235, 554, 951, 99, 562, 
  982, 760, 37, 517, 468, 676, 36, 387, 613, 547, 495, 37, 338, 453, 16, 49, 
  784, 156, 123, 234, 360, 670, 456, 263, 346, 112, 259, 101, 910, 769, 348, 
  807, 998, 525, 853, 978, 350, 319, 678, 800, 754, 350, 72, 248, 794, 98, 662, 
  402, 535, 69, 32, 295, 972, 339, 250, 932, 660, 621, 749, 344, 587, 589, 611, 
  644, 239, 603, 642, 35, 823, 840, 545, 641, 754, 58, 167, 864, 877, 861, 43, 
  666, 336, 405, 410, 830, 675, 917, 443, 768]
  #----------------------------------------------------------------------------
  for seed in seeds:
    runMatches = profilematches(f, IDvector1, IDvector2, numtree, biniter, seed)
    seedresults[seed]=runMatches

  #filter for only those pairs, that are found in all runs
  overallmatch=[]
  init = seedresults[seeds[0]] #take the pairs of the first seed and compare them against all others
  for pair in init:
    counter = 0
    for seed in seeds:
      if pair in seedresults[seed]:
        counter +=1
    if counter == len(seeds):
      overallmatch.append(pair)
    
  #save the results            
  results = open("/Users/berthola/Desktop/Results/lch51ALLresults.txt", "w") #define filename here
  results.write(str(seedresults))
  results.close()
  #and save all matches
  overall = results = open("/Users/berthola/Desktop/Results/lch51overall.txt", "w")
  overall.write(str(overallmatch))
  overall.close()

  return overallmatch

print rdmSeedRuns(featureList, lch51l, lch51r, 500, 70)












