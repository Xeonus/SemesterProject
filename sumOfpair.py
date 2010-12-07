#Brute force approach: form sum of all Features of initial feature Vector of all possible pairs and store them in an new vector.
#Search for pairs below a certain threshold and look how similar they are.


from math import sqrt
from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from machine_ import featureMeasure, feature2


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

def sumOfpair(treesleft, treesright, biniter):
  """ Outputs a list of the featurefactor of all possible combinations of pairs of two sides"""
  #pairlist={}
  pairlist=[]
  pairs=[]
  sumM=0
  for id1 in treesleft:
    for id2 in treesright:
      pair=[id1, id2]
      measure=featureMeasure(pair,  biniter)
      pairlist.append(measure)
      pairs.append(pair)
  print "The pairs are:", pairs
  print "The sum of pairs on same position in list are:", pairlist



print sumOfpair(lch51l, lch51r, 30)

"""
test=
values=[]
for t in test:
  value = test[t]
  values.append(value)

for t in test:
  if test[t] == min(values):
    print "lowest value for pair:", t
"""