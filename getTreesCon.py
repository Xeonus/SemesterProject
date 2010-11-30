from ini.trakem2.display import Display, Connector
from jarray import array
from java.awt.geom import Area
from java.awt import Rectangle
import sys
sys.path.append("/Users/berthola/Desktop/Fiji Scripts")
from dendriticprofiling import getNodeCoordinates
#Obtain all downstream partners of the defined tree 

ID=75408
tree = tree = Display.getFront().getLayerSet().findById(ID)
affine = tree.getAffineTransform()
layerset = tree.getLayerSet()
 
# Maps of nd vs list of trees:
outgoing = {}   # e.g. presynaptic to some trees
 
for nd in tree.getRoot().getSubtreeNodes():
  # Obtain the node position in world coordinates 
  fp = array([nd.getX(), nd.getY()], 'f')
  affine.transform(fp, 0, fp, 0, 1)
  x = int(fp[0])
  y = int(fp[1])
  # Query the LayerSet for Connector objects that intersect it
  cs = layerset.findZDisplayables(Connector, nd.getLayer(), x, y, False)
  if cs.isEmpty():
    continue
  # Else, get the target Tree instances that each connector links to:
  targets = []
  area = Area(Rectangle(x, y, 1, 1))
  for connector in cs:
    if connector.intersects(area): #was before intersectsOrigin: changed in recent update?
      for target in connector.getTargets(Tree):
        targets.append(target)      
  if len(targets) > 0:
    outgoing[nd] = targets
 
# print the map of nodes and the number of trees each connects to:
targetcontainer=[]
for node, targets in outgoing.iteritems():
  targetcontainer+=targets

#Save the IDs of treelines to an array and exclude connectors as well as duplicates
IDs=[]
for i in range(0, len(targetcontainer)):
  if targetcontainer[i].getClass() == Connector:
    continue
  if targetcontainer[i].size() == 0:
    continue
  else:
    ID=(targetcontainer[i].toArray()[0]).getId()
    IDs.append(int(ID))

#Get rid of duplicates and sort the list
ordered=list(set(IDs))

#filter out small fragments <=500 nodes
filtered=[]
for ID in ordered:
  tree = Display.getFront().getLayerSet().findById(ID)
  if len(getNodeCoordinates(tree)) >= 500:
    filtered.append(ID)
  else:
    continue
    
print filtered
 
