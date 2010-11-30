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
  
#----------------PLOT histograms-----------------------------------
#  treeIDsleft=[73337, 73698, 73230, 74504, 72481, 72295, 71887, 73544, 73675, 72743, 74329, 74434, 74434, 73337]
#  treeIDsright=[75616, 75783, 76408, 76825, 99481, 74877, 75408, 75949, 76718, 75854, 77041, 76923, 74434, 73337]
#  wrongIDs1=[90155, 90168, 77161, 76052, 70195, 89088, 99495, 77829, 81321, 89147, 83589, 87617, 98723]
#  wrongIDs2=[90161, 90165, 77155, 82591, 83068, 89094, 79187, 79740, 81032, 89245, 85171, 90045, 98916]

ID=75616
tree = Display.getFront().getLayerSet().findById(ID)
#print feature4(73337, 75616, 55)

coords = Matrix(getNodeCoordinates(tree))

#Define axis vectors and origin
xnorm = Matrix([[1,0,0]])
ynorm = Matrix([[0,1,0]])
znorm = Matrix([[0,0,1]])
center= Matrix([[0,0,0]])

#Project nodes onto axis
dpx=[]
dpy=[]
dpz=[]
m=coords.getRowDimension()
for i in range(0, m):
  xstore = Matrix([coords.getRow( i )]) * xnorm.transpose()
  ystore = Matrix([coords.getRow( i )]) * ynorm.transpose()
  zstore = Matrix([coords.getRow( i )]) * znorm.transpose()
  dpx.append(xstore.getRow(0))
  dpy.append(ystore.getRow(0))
  dpz.append(zstore.getRow(0))

#Count number of nodes which fall in defined interval of pca projection
counter = 0
xhistovector = []
yhistovector = []
zhistovector = []

#get it back in array form (get rid of list in list of Jarray)

dpx=[ x[0] for x in dpx]
dpy=[ x[0] for x in dpy]
dpz=[ x[0] for x in dpz]

#Initialize interval size and fix iterations to a specific number
xbinleft = -34600.0
ybinleft = -24200.0
zbinleft = 0
iterations =100
xlength = int((35600.0+34600.0)/iterations + 0.5)
ylength = int((21300.0+24200.0)/iterations + 0.5)
zlength = int((22500)/iterations + 0.5)
xbinright = xbinleft + xlength
ybinright = ybinleft + ylength
zbinright = zbinleft + zlength

#Count elements in bins
xaxis=[]

for i in range(0,iterations):
  for i in range(0, len(dpx)):
    if dpx[i] <= xbinright and dpx[i] >= xbinleft:
      counter += 1    
  xhistovector.append(counter)
  counter=0
  xbinleft += xlength
  xbinright += xlength
  xaxis.append(xbinleft)
  
yaxis=[]

for i in range(0,iterations):
  for i in range(0, len(dpy)):
    if dpy[i] <= ybinright and dpy[i] >= ybinleft:
      counter += 1    
  yhistovector.append(counter)
  counter=0
  ybinleft += ylength
  ybinright += ylength
  yaxis.append(ybinleft)

zaxis=[]

for i in range(0,iterations):
  for i in range(0, len(dpz)):
    if dpz[i] <= zbinright and dpz[i] >= zbinleft:
      counter += 1    
  zhistovector.append(counter)
  counter=0
  zbinleft += zlength
  zbinright += zlength
  zaxis.append(zbinleft)

for i in range(0, iterations):
  xhistovector[i]/=float(xlength)
  yhistovector[i]/=float(ylength)
  zhistovector[i]/=float(zlength)
"""  
#Normalize vector
for i in range(0, len(yhistovector)):
  yhistovector[i] /=xlength

for i in range(0, len(xhistovector)):
  xhistovector[i] /=ylength
  
for i in range(0, len(zhistovector)):
  zhistovector[i] /=zlength

#print "The histogram vector for x-axis is:", xhistovector
#print "The histogram vector for y-axis is:", yhistovector
#print "The histogram vector for z-axis is:", zhistovector
"""

#Plot absolute coordinates versus node-count in a histogram

plot = Plot("histogram", "y-coordinates", "count",yaxis, yhistovector)
plot.show()
fs=FileSaver(plot.getImagePlus())
fs.saveAsPng(System.getProperty("user.home") + "/Desktop/Histotest/y" + str(ID) + ".png")

plot = Plot("histogram", "z-coordinates", "count", zaxis, zhistovector)
plot.show()
fs=FileSaver(plot.getImagePlus())
fs.saveAsPng(System.getProperty("user.home") + "/Desktop/Histotest/z" + str(ID) + ".png")

plot = Plot("histogram", "x-coordinates", "count", xaxis, xhistovector)
plot.show()
fs=FileSaver(plot.getImagePlus())
fs.saveAsPng(System.getProperty("user.home") + "/Desktop/Histotest/xleft" + str(ID) + ".png")

#Mirror on x-axis

xhistomirror=[]
xhistovector.reverse()
for i in range(0, len(xhistovector)):
  xhistomirror.append(xhistovector[i])

xaxismirror=[]
xaxis.reverse()
for i in range(0, len(xaxis)):
  xaxismirror.append(xaxis[i]*(-1))

plot = Plot("histogram", "x-coordinates", "count", xaxismirror, xhistomirror)
plot.show()
fs=FileSaver(plot.getImagePlus())
fs.saveAsPng(System.getProperty("user.home") + "/Desktop/Histotest/xright" + str(ID) + ".png")
