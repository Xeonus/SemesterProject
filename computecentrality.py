from ini.trakem2.display import Display
from java.awt import Color
 
def computeColor(centrality, highest):
  red = centrality / float(highest)
  blue = 1 - red
  return Color(red, red, blue)
 
# Obtain the currently selected Tree in the canvas:
tree = Display.getFront().getActive()
 
# Compute betweenness centrality
bc = tree.computeCentrality()   # a java.util.Map
 
# Find out the maximum centrality value, to scale:
maximum = reduce(max, bc.values())
 
# Colorize each node according to its centrality
for e in bc.entrySet():
  node = e.getKey()
  centrality = e.getValue()
  node.setColor(computeColor(centrality, maximum))
 
# Update display
Display.repaint()
 
# Show the tree in the 3D Viewer
Display3D.show(tree.getProject().findProjectThing(tree))