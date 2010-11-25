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
from java.util import ArrayList
from java.text import DecimalFormat
from pcaFinal import pca
from scholl import sphereCount

##IMPORTANT: ID2 ALWAYS HAS TO BE THE TREE FORM THE RIGHT HANDSIDE OF LARVA

#------------Get distances-----------------

def profileDistances(ID, biniter):

  histo=getDendriticProfiles(ID, biniter)

  xhisto=histo[0]
  yhisto=histo[1]
  zhisto=histo[2]

  xdistance=[]
  ydistance=[]
  zdistance=[]

  tree = Display.getFront().getLayerSet().findById(ID)
  coords = Matrix(getNodeCoordinates(tree))
  m=coords.getRowDimension()

  for i in range(0, m):
    xdist = coords.get(i, 1 )
    if xdist > 0 :
      xdistance.append(xdist)
    else:
      xdistance.append((-1)*xdist)

  for i in range(0, m):
    ydist = coords.get(i, 0 )
    if ydist > 0 :
      ydistance.append(ydist)
    else:
      ydistance.append((-1)*ydist)

  for i in range(0, m):
    zdist = sqrt(coords.get(i, 0)**2 + coords.get(i,1)**2)
    zdistance.append(zdist)

  return xdistance, ydistance, zdistance


#--------Compute feature 1 -> Sum of distances-----------------
def sumDist(id1, biniter):

  distance=profileDistances(id1, biniter)
  xdistance=distance[0]
  ydistance=distance[1]
  zdistance=distance[2]
  
  tree = Display.getFront().getLayerSet().findById(id1)
  coords = Matrix(getNodeCoordinates(tree))
  m=coords.getRowDimension()

  xdist=[]
  ydist=[]
  zdist=[]
  
  #Initialize interval size and fix iterations to a specific coordinate position
  xbinleft = -34600.0
  ybinleft = -24200.0
  zbinleft = 0
  #----------PARAMETER FOR MACHINE LEARNING-----
  iterations =biniter
  #---------------------------------------------
 
  xlength = int((35600.0+34600.0)/iterations + 0.5)
  ylength = int((21300.0+24200.0)/iterations + 0.5)
  zlength = int((22500)/iterations + 0.5)
  
  xbinright = xbinleft + xlength
  ybinright = ybinleft + ylength
  zbinright = zbinleft + zlength  

  sumdist=0.0
  
  for i in range(0, iterations):
    for i in range(0, len(xdistance)):
      if xdistance[i] <= xbinright and xdistance[i] >= xbinleft:
        sumdist += xdistance[i]   
    xdist.append(sumdist)
    sumdist=0.0
    xbinleft += xlength
    xbinright += xlength

  for i in range(0, iterations):
    for i in range(0, len(ydistance)):
      if ydistance[i] <= ybinright and ydistance[i] >= ybinleft:
        sumdist += ydistance[i]     
    ydist.append(sumdist)
    sumdist=0.0
    ybinleft += ylength
    ybinright += ylength

  for i in range(0, iterations):
    for i in range(0, len(zdistance)):
      if zdistance[i] <= zbinright and zdistance[i] >= zbinleft:
        sumdist += zdistance[i]     
    zdist.append(sumdist)
    sumdist=0.0
    zbinleft += zlength
    zbinright += zlength

  sumdistance=[]
  sumdistance= [xdist, ydist, zdist]
  return sumdistance

# Own function to reverse elements of list, because of problem with built in .reverse() commmand
def reversing(array):
  liste=array
  reverse=[]
  runs=len(liste)
  for l in range(0, runs):
    element = liste[runs-l-1]
    reverse.append(element)
  return reverse

#---Compute first feature -> sum of square distance difference------------
"""
def feature1(id1, id2, biniter):
  diff1=sumDist(id1, biniter)
  diff2=sumDist(id2, biniter)

  tree1 = Display.getFront().getLayerSet().findById(id1)
  coords1 = Matrix(getNodeCoordinates(tree1))
  m1=coords1.getRowDimension()

  tree2 = Display.getFront().getLayerSet().findById(id2)
  coords2 = Matrix(getNodeCoordinates(tree2))
  m2=coords2.getRowDimension()
  
  xdiff1=diff1[0]
  ydiff1=diff1[1]
  zdiff1=diff1[2]
  
  xdiff2=diff2[0]
  #xdiff2.reverse() #####
  xdiff2=reversing(xdiff2)
  ydiff2=diff2[1]
  zdiff2=diff2[2]

  xdiff=0
  ydiff=0
  zdiff=0
  euclidean=[]

  for i in range(0, len(xdiff1)): 
      xdiff += sqrt((xdiff1[i]/m1-xdiff2[i]/m2)**2) #Normalize differences with number of nodes! Small trees compared to big ones give a bigger error
      ydiff += sqrt((ydiff1[i]/m1-ydiff2[i]/m2)**2)
      zdiff += sqrt((zdiff1[i]/m1-zdiff2[i]/m2)**2)

  euclidean=[xdiff, ydiff, zdiff]
  return euclidean


  """
#Correct version of feature 1
def feature1(id1, id2, biniter):
  diff1=getDendriticProfiles(id1, biniter)
  diff2=getDendriticProfiles(id2, biniter)

  tree1 = Display.getFront().getLayerSet().findById(id1)
  coords1 = Matrix(getNodeCoordinates(tree1))
  m1=coords1.getRowDimension()

  tree2 = Display.getFront().getLayerSet().findById(id2)
  coords2 = Matrix(getNodeCoordinates(tree2))
  m2=coords2.getRowDimension()
  
  xdiff1=diff1[3]
  ydiff1=diff1[4]
  zdiff1=diff1[5]
  
  xdiff2=diff2[3]
  #xdiff2.reverse() #####
  xdiff2=reversing(xdiff2)
  ydiff2=diff2[4]
  zdiff2=diff2[5]

  xdiff=0
  ydiff=0
  zdiff=0
  euclidean=[]

  for i in range(0, len(xdiff1)): 
      xdiff += sqrt((xdiff1[i]/m1-xdiff2[i]/m2)**2) #Normalize differences with number of nodes! Small trees compared to big ones give a bigger error
      ydiff += sqrt((ydiff1[i]/m1-ydiff2[i]/m2)**2)
      zdiff += sqrt((zdiff1[i]/m1-zdiff2[i]/m2)**2)
      
  """
  #NORMALIZE BY NUMBER OF NODES-----NEW-------
  xdiff=xdiff/m
  ydiff=ydiff/m
  zdiff=zdiff/m
  #--------------------------- 
  """  
  euclidean=[xdiff, ydiff, zdiff]
  return euclidean
 
#----------Compute second feature -> Sum of Euclidean distances bincount-----------
def feature2(id1, id2, biniter):

  histo1=getDendriticProfiles(id1, biniter)
  histo2=getDendriticProfiles(id2, biniter)
  xhisto1=histo1[0]
  yhisto1=histo1[1]
  zhisto1=histo1[2]
  
  xhisto2=histo2[0]
  #xhisto2.reverse() #####
  xhisto2=reversing(xhisto2)
  yhisto2=histo2[1]
  zhisto2=histo2[2]
  
  xdiff=0
  ydiff=0
  zdiff=0
  euclidean=[]
  
  for i in range(0, len(histo1[0])):
      xdiff += (xhisto1[i]-xhisto2[i])**2
      ydiff += (yhisto1[i]-yhisto2[i])**2
      zdiff += (zhisto1[i]-zhisto2[i])**2
  euclidean=[xdiff, ydiff, zdiff]
  
  return euclidean

#---------Compute third feature -> Standart deviation of node-count histogram----
def stdev(id1, biniter):
  histo1=getDendriticProfiles(id1, biniter)
  xhisto=histo1[0]
  yhisto=histo1[1]
  zhisto=histo1[2]
  standard=[]

  n, mean, std = len(xhisto), 0, 0
  for a in xhisto:
    mean = mean + a
  mean = mean / float(n)
  for a in xhisto:
    std = std + (a - mean)**2
  std = sqrt(std / float(n-1))
  standard.append(std)
  
  n, mean, std = len(yhisto), 0, 0
  for a in yhisto:
    mean = mean + a
  mean = mean / float(n)
  for a in yhisto:
    std = std + (a - mean)**2
  std = sqrt(std / float(n-1))
  standard.append(std)

  n, mean, std = len(zhisto), 0, 0
  for a in zhisto:
    mean = mean + a
  mean = mean / float(n)
  for a in zhisto:
    std = std + (a - mean)**2
  std = sqrt(std / float(n-1))
  standard.append(std)

  return standard

#------Compute Standartdeviation sum diff of histograms------------

def feature3(id1, id2, biniter):

  histo1=stdev(id1, biniter)
  histo2=stdev(id2, biniter)
  xhisto1=histo1[0]
  yhisto1=histo1[1]
  zhisto1=histo1[2]
  
  xhisto2=histo2[0]
  yhisto2=histo2[1]
  zhisto2=histo2[2]
  
  xdiff=0
  ydiff=0
  zdiff=0
  euclidean=[]
  
  xdiff += (xhisto1-xhisto2)**2
  ydiff += (yhisto1-yhisto2)**2
  zdiff += (zhisto1-zhisto2)**2
  euclidean=[xdiff, ydiff, zdiff]
  
  return euclidean

#----Compute a simple difference of both histograms

def feature4(id1, id2, biniter):
  histo1=getDendriticProfiles(id1, biniter)
  histo2=getDendriticProfiles(id2, biniter)

  xhisto1=histo1[0]
  yhisto1=histo1[1]
  zhisto1=histo1[2]
  
  xhisto2=reversing(histo2[0])
  yhisto2=histo2[1]
  zhisto2=histo2[2]

  xdiff=0
  ydiff=0
  zdiff=0

  histodiff=[]
  x=[]
  y=[]
  z=[]

  for i in range(0, biniter):
    xdiff = xhisto1[i]-xhisto2[i]
    x.append(xdiff)
    ydiff = yhisto1[i]-yhisto2[i]
    y.append(ydiff)
    zdiff = zhisto1[i]-zhisto2[i]
    z.append(zdiff)
  histodiff = x + y + z
  return histodiff

    
#-------Input the raw HistogramVector as training Vector

def rawHistogramVector(id1, id2, biniter):

  histo1=getDendriticProfiles(id1, biniter)
  histo2=getDendriticProfiles(id2, biniter)
  xhisto1=histo1[0]
  yhisto1=histo1[1]
  zhisto1=histo1[2]
  
  xhisto2=histo2[0]
  xhisto2=reversing(xhisto2)
  yhisto2=histo2[1]
  zhisto2=histo2[2]

  trainingvector = []
  trainingvector = xhisto1 + yhisto1 + zhisto1 + xhisto2 + yhisto2 + zhisto2
  return trainingvector

  
def featureSum(id1, id2, biniter):
  summation = 0
  featureV = featureVector(id1, id2, biniter)
  for i in range(0, len(featureV)):
    summation += int(featureV[i])
  return summation

def featureVector(id1, id2, biniter):
  trainingvector = []
  trainingvector =feature1(id1,id2, biniter) + feature2(id1, id2, biniter) + feature3(id1, id2, biniter)
  return trainingvector

def featureMeasure(idpair, biniter):
  """ input a pair of 2 possible matches as follows: [id1, id2]. Return sum of featureVector"""
  trainingvector = featureVector(idpair[0], idpair[1], biniter)
  sumMeasure=0
  for s in trainingvector:
    sumMeasure+=s
  return sumMeasure

def rawFeatureVector(id1, id2, biniter):
  histo1=getDendriticProfiles(id1, biniter)
  xhisto1=histo1[0]
  yhisto1=histo1[1]
  zhisto1=histo1[2]
  
  histo2=getDendriticProfiles(id1, biniter)
  xhisto2=histo2[0]
  yhisto2=histo2[1]
  zhisto2=histo2[2]

  #Calculation of sum of distances in bin is now included in getDendriticProfiles function to reduce runtime
  xsumDist1 = histo1[3]
  ysumDist1 = histo1[4]
  zsumDist1 = histo1[5]

  xsumDist2 = histo2[3]
  ysumDist2 = histo2[4]
  zsumDist2 = histo2[5]
    
  rawVector = []
  rawVector = xhisto1 + xhisto2 + yhisto1 + yhisto2 + zhisto1 + zhisto2 + feature4(id1, id2, biniter) + feature1(id1, id2, biniter) +feature3(id1, id2, biniter) + feature2(id1, id2, biniter)
  return rawVector

def pcaSphereVector(id1, id2, biniter):
  sphere1 = sphereCount(id1, biniter)
  sphere2 = sphereCount(id2, biniter)
  s1 = sphere1[0]
  s2 = sphere2[0]
  pca1 = pca(id1, biniter)
  pca2 = reversing(pca(id2, biniter))

  pcadiff=[]
  spherediff=[]
  for i in range(0, len(pca1)):
    pdiff = sqrt((pca1[i] - pca2[i])**2)
    pcadiff.append(pdiff)
    sdiff = sqrt((s1[i] - s2[i])**2)
    spherediff.append(sdiff)
  

  trainingvector=[]
  trainingvector = sphere1[0] + sphere2[0] + pca1 + pca2 +feature4(id1, id2, biniter) 

  return trainingvector


#print pcaSphereVector(72481, 99481, 10)


#-----------------Machine Learning-------------------------------------------

from weka.core import DenseInstance, Instances, Attribute
from weka.classifiers import AbstractClassifier
from hr.irb.fastRandomForest import FastRandomForest


def createClassifier(numTrees, numFeatures):
  rf = FastRandomForest()
  rf.setNumTrees(numTrees)
  rf.setNumFeatures(numFeatures)
  rf.setSeed(123) #initially 123
  return rf

def createAttributes(featureVector):
  numFeatures = len(featureVector)
  attributes = [Attribute(str(i) + " numeric") for i in range(numFeatures)]
  attributes.append(Attribute("class", ArrayList(["true", "false"])))
  instances = Instances("tests", ArrayList(attributes), 1)
  instances.setClassIndex(len(attributes) -1)
  return ArrayList(attributes)

def createTrainingInstances(matchingExamples, mismatchingExamples):
  """ Expects the matchingExamples to be a list of feature lists,
      i.e. the feature vector is a list. """
  numFeatures = len(matchingExamples[0])
  attributes = [Attribute(str(i) + " numeric") for i in range(numFeatures)]
  attributes.append(Attribute("class", ArrayList(["true", "false"])))
  trainingData = Instances("matches", ArrayList(attributes), len(matchingExamples) + len(mismatchingExamples))
  trainingData.setClassIndex(len(attributes) -1) # the last index
  for f in matchingExamples:
    trainingData.add(DenseInstance(1.0, f + [1])) # 1 is True
  for f in mismatchingExamples:
    trainingData.add(DenseInstance(1.0, f + [0])) # 0 is False
  return trainingData
  
def trainClassifier(classifier, matchingExamples, mismatchingExamples):
  ti = createTrainingInstances(matchingExamples, mismatchingExamples)
  classifier.buildClassifier(ti)
  df = DecimalFormat("0.0000")
  return df.format(classifier.measureOutOfBagError()) #print

"""
def trainClassifier(classifier, matchingExamples, mismatchingExamples):
  try:
    ti = createTrainingInstances(matchingExamples, mismatchingExamples)
    classifier.buildClassifier(ti)
    df = DecimalFormat("0.0000")
    print "out of bag error:", df.format(classifier.measureOutOfBagError()) #print
  except:
   import sys, traceback
   print 'error:', traceback.print_exc(file=sys.stdout) # sys.exc_info()
"""  

def classify(classifier, matches):
  """ Expects one vector numFeatures length """
  attributes = createAttributes(matches[0])
  instances = Instances("tests", attributes, 1)
  instances.setClassIndex(len(attributes) -1)
  results = []
  for match in matches:
    instances.add(DenseInstance(1.0, match + [0]))
  for i in range(len(matches)):
    results.append(classifier.classifyInstance(instances.instance(i)))
  return results


  