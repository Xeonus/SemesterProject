#Brute force approach: form sum of all Features of initial feature Vector of all possible pairs and store them in an new vector.
#Search for pairs below a certain threshold and look how similar they are.


from math import sqrt
from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from machine_ import featureMeasure, feature2


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

def sumOfpair(treesleft, treesright, biniter):
  """ Outputs a list with all possible combinations of pairs of two sides"""
  #pairlist={}
  pairlist=[]
  pairs=[]
  sumM=0
  for id1 in IDvector1:
    for id2 in IDvector2:
      pair=[id1, id2]
      measure=feature2(id1, id2, biniter)
      for m in measure:
        sumM +=m 
      print sumM
      pairlist.append(sumM)
      pairs.append(pair)
      sumM=0
  print "The pairs are:", pairs
  print "The sum of pairs on same position in list are:", pairlist



print sumOfpair(IDvector1, IDvector2, 170)

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