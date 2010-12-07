from ini.trakem2.display import Display
from jarray import array
from math import sqrt
 
def getNodeCoordinates(tree):
  """ Returns a map of Node instances vs. their X,Y,Z world coordinates. """
  root = tree.getRoot()
  if root is None:
    return {}
  calibration = tree.getLayerSet().getCalibration()
  affine = tree.getAffineTransform()
  coords = {}
  #
  for nd in root.getSubtreeNodes():
    fp = array([nd.getX(), nd.getY()], 'f')
    affine.transform(fp, 0, fp, 0, 1)
    x = fp[0] * calibration.pixelWidth
    y = fp[1] * calibration.pixelHeight
    z = nd.getLayer().getZ() * calibration.pixelWidth   # a TrakEM2 oddity
    # data may be a radius or a java.awt.geom.Area 
    coords[nd] = [x, y, z]
  #
  return coords
 
# Obtain the tree selected in the canvas:
tree = Display.getFront().getActive()
 
# Print all its node coordinates:

for node, coord in getNodeCoordinates(tree).iteritems():
  x, y, z = coord
  print "Coords for node", node,  " : ", x, y, z
