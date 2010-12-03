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
from featureLoader_ import featureList, rawFeaturetrainer, rawFeatureList, pcaSpheretrainer

#print all results of all possible combinations into a dictionary
container={}
condition=[]
#for all possible numbers of trees
for nt in range(50, 625, 25):
  result=[]
  #test all iterations
  for i in range(10, 305, 5):
    condition= float(pcaSpheretrainer(nt, i))
    print condition
    result.append(condition)
  container[nt]=result
print container


"""
#after getting the result from above, look for optimal results
container={}

mins=[]
iterations=[]
binvector=[]
position=0
for i in range(50, 625, 25):
    for j in range(0, 59):  
      minimum=min(container[i])
      mins.append(minimum)
      binvector=container[i]
      if binvector[j] == min(binvector):
        position=j
    iterations.append(position)
    position=0
      
print mins
print iterations
"""




