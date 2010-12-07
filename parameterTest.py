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
from machine_ import featureVector, createClassifier, trainClassifier, classify
from featureLoader_ import featureList, rawFeaturetrainer, rawFeatureList, featuretrainer


#Make a list of all parameters and oob at the end and save those lists to another list
#print all results of all possible combinations into a dictionary
container=[]
def parametertest(i): #have to adjust this so the ID library is build up newly
  #for all possible numbers of trees
  for nt in range(50, 625, 25):
    #test all iterations
      #against possible initial seeds
    conditions=[]
    for seed in range(0, 200):
      condition = float(featuretrainer(nt, i, seed))
      print "For", nt, "trees, and", i, "iterations, and seed", seed, " the oob is:", condition
      conditions = [nt, i, seed, condition]
      container.append(conditions)
    return container

test=[]
for i in range(10, 305, 5):
   test.append(parametertest(i))
   print parametertest(i)
   iddict={}
print test




