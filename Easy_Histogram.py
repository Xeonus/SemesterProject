# A simple example showing how to draw histograms using JFreeChart
# from Jython.  This is based heavily on the pure Java example found
# here: http://www.roseindia.net/tutorial/java/jfreechart/createhistogram.html

from org.jfree.data.statistics import HistogramDataset
from org.jfree.data.statistics import HistogramType
from org.jfree.chart.plot import PlotOrientation
from org.jfree.chart import ChartFactory
from org.jfree.chart import ChartUtilities
from org.jfree.data.xy import IntervalXYDataset


from java.io import File
from java.awt import Dimension
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
ID=75408
tree = Display.getFront().getLayerSet().findById(ID)

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
iterations =20
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

#--------------------Plot with jfreeChart environment-----------

values = xhistovector
bins = 20

dataset = HistogramDataset()
dataset.setType( HistogramType.FREQUENCY ) #other options: RELATIVE_FREQUENCY, SCALE_AREA_TO_1

dataset.addSeries( "Node count", values, bins)

chart = ChartFactory.createHistogram(
	"Node Count Histogram",
	"Bins",
	"Node count",
	dataset,
	PlotOrientation.VERTICAL,
	True,  # showLegend
	True,  # toolTips
	True,) # urls

# Save it as a PNG:
ChartUtilities.saveChartAsPNG(
  File("/Users/berthola/Desktop/Histotest/foo.png"),
  chart,
  800,
  600)

from org.jfree.chart import ChartPanel
from javax.swing import JFrame

class SimpleChart(JFrame):
	def __init__(self,chart):
		chartPanel = ChartPanel(chart)
		chartPanel.setPreferredSize(Dimension(800,600))
		chartPanel.setMouseZoomable(True,False)
		self.setContentPane(chartPanel)

s = SimpleChart(chart)
s.pack()
s.setVisible(True)
