#Brute force approach: form sum of all Features of initial feature Vector of all possible pairs and store them in an new vector.
#Search for pairs below a certain threshold and look how similar they are.


from math import sqrt
from ini.trakem2.display import Display
from jarray import array
import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from machine_ import featureMeasure


Dleft=[81726, 99771, 99665, 81196, 99519, 99316, 99370, 80317, 99455, 83780, 98971, 
99442, 93311, 98730, 99063, 98929, 89064, 80584, 83486, 98982, 98720, 99348, 99696, 72679, 
99427, 99766, 98882, 82011, 81772, 98268, 81321, 99306, 99092, 99213, 99679, 83695, 99072, 
81886, 81769, 99194, 99200, 98792, 99668, 83677, 98996, 99083, 99216, 99640, 98629, 99095, 
98707, 81739, 83822, 99223, 99617, 72615, 98723, 83070, 99522, 72597, 99283, 98968, 83600, 
99705, 72481, 83772, 81972, 81732, 98913, 70195, 77177, 98733, 99511, 98955, 99580, 71887, 
81969, 81723, 98795, 99684, 99197, 99516, 98932, 99089, 83668, 81916, 99635, 99066, 99203, 
98916, 80741, 83627, 99290, 99267, 99313, 99569, 89066, 98860, 99086, 99495, 80723, 72633]

Dright=[97549, 98383, 95421, 98268, 97669, 75408, 94943, 99316, 95674, 96647, 91869, 
97790, 75108, 75466, 92479, 97542, 96580, 91612, 75298, 95812, 91704, 94264, 98494, 83695, 
75193, 97060, 75078, 95000, 97423, 95190, 91884, 95151, 95424, 93131, 98345, 91848, 99481, 
97607, 75169, 97779, 75184, 75102, 97559, 97623, 93195, 91609, 97063, 93048, 98238, 97066, 
99431, 93862, 75096, 96733, 75268, 83000, 97562, 93883, 94948, 93582, 96875, 97572, 93400, 
97073, 96575, 95246, 91973, 98263]

IDleft=[81726, 99771, 99665, 81196, 99519, 99316, 99370, 80317]

IDright=[97549, 98383, 95421, 98268, 97669, 75408, 94943, 99316, 95674]

def sumOfpair(treesleft, treesright, biniter):
  """ Outputs a list with all possible combinations of pairs of two sides"""
  pairlist={}
  for i in range(0, len(treesleft)):
    for j in range(0, len(treesright)):
      pair=[treesleft[i], treesright[j]]
      measure=featureMeasure(pair, biniter)
      pairlist[str(pair[0]) + "--" + str(pair[1])] = measure
  return pairlist


print sumOfpair(Dleft, Dright, 100)

"""
test={'81726--97669': 17060.142532627906, '99519--98268': 9115.211040129303, '99370--75408': 11603.030011880515, '81196--75408': 8033.667824254077, '99771--75408': 14009.743338117383, '99316--95674': 15601.138748547826, '81196--98268': 5718.202128270244, '81726--95674': 12692.378120962252, '81196--99316': 11630.844951622705, '99316--75408': 13794.52061109606, '99771--97549': 8532.3015270722, '99519--95421': 18444.871768386176, '99519--97669': 18972.883764671973, '99665--98268': 9965.166852971364, '81726--99316': 13462.500519928046, '81196--94943': 12352.936508578838, '81196--97549': 4636.5742835256615, '99370--99316': 14839.082745994387, '99370--95421': 17915.598210278666, '80317--75408': 11789.843421192454, '99519--75408': 12129.779521621067, '99519--99316': 15397.530152075098, '80317--97549': 4588.125742735572, '81196--98383': 7392.446315476041, '80317--97669': 18619.370348994697, '99370--98268': 8547.05539580569, '81726--94943': 14183.613643921544, '81726--95421': 16532.14216953993, '80317--98383': 8674.533233811539, '81726--98268': 12339.37854524512, '99665--97669': 19815.149903588852, '81726--98383': 13715.2204668199, '80317--95421': 18105.499661166385, '99316--94943': 10056.276469039682, '81196--95674': 7673.66363894203, '99665--95674': 2529.749311880218, '99519--97549': 2382.4071089073336, '99665--95421': 19332.223447402175, '99316--97549': 13672.854678927413, '99771--94943': 17371.58361966707, '99771--98383': 12386.474636367535, '99665--94943': 16963.45565544454, '99771--97669': 20232.131686478595, '99519--94943': 16096.344715701425, '80317--95674': 4485.167019671173, '99665--98383': 9520.548145201647, '99370--97669': 18394.177996401926, '99771--95421': 19737.042014144663, '99771--99316': 16652.38242868529, '99316--95421': 12842.076633671795, '99771--98268': 11020.203946628833, '81726--75408': 14859.548252395978, '99665--97549': 3328.1219067532643, '80317--94943': 15751.816752908288, '99519--98383': 9037.881519199396, '80317--98268': 8760.448059647086, '99519--95674': 2994.1690656433234, '81196--95421': 14731.58337757529, '81196--97669': 15230.12270818882, '81726--97549': 9547.381009032408, '99316--97669': 12099.646660119834, '99316--98383': 14305.959956724908, '80317--99316': 15046.839511812424, '99370--95674': 6472.247772182033, '99370--94943': 15542.165475750577, '99370--97549': 3485.132535303112, '99771--95674': 11789.57671566226, '99665--75408': 13020.347149724561, '99665--99316': 16260.34212378421, '99316--98268': 9158.094735380117, '99316--99316': 3800.189119774807, '99370--98383': 8447.452891049557}

values=[]
for t in test:
  value = test[t]
  values.append(value)

for t in test:
  if test[t] == min(values):
    print "lowest value for pair:", t
"""