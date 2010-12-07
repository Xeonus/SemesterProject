from math import sqrt
from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from javax.media.j3d import Transform3D
from ij.io import FileSaver
from machine_ import featureMeasure

#plot the sum of featureVector of pairs found by the random forest algorithm


def measure(matchArray, biniter):
  matchlist = matchArray
  sumList=[]
  for pair in matchlist:
    sumMatches = featureMeasure(pair, biniter)
    #print sumMatches
    sumList.append(sumMatches)
  return sumList
"""
match= []
test = measure(match, 30)
print test
"""

for i in range(0, len(test)):
  if test[i] == min(test):
    print i
    
#x-axis:
xaxis=[]
for i in range(0, len(test)):
  xaxis.append(i)


plot = Plot("pair vs similarity factor", "pair", "similarity factor", xaxis, test)
plot.show()

