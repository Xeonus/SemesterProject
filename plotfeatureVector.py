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
from machine_ import featureVector



good = featureVector(72481, 99481, 50)
bad =  featureVector(83160, 99481, 50)





plot = Plot("histogram", "y-coordinates", "count",range(0, 50), good)
plot.setLimits(0.0, 50.0, 0, 60000000.0) 
plot.show()
fs=FileSaver(plot.getImagePlus())
fs.saveAsPng(System.getProperty("user.home") + "/Desktop/Histotest/y" + "good.png")

plot = Plot("histogram", "y-coordinates", "count",range(0, 50), bad)
plot.setLimits(0.0, 50.0, 0, 60000000.0) 
plot.show()
fs=FileSaver(plot.getImagePlus())
fs.saveAsPng(System.getProperty("user.home") + "/Desktop/Histotest/y" + "bad.png")
