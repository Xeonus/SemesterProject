from ini.trakem2.display import Display, Connector
from jarray import array
from java.awt.geom import Area
from java.awt import Rectangle
 
# Obtain the currently defined treeline or areatree:
ID=99481
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

"""
singleIDs=[]
singleIDs.append(IDs[0])
for j in range(1, len(IDs)):
  for i in range(0, len(singleIDs)):
    if singleIDs[i] == IDs[j]:
      singleIDs.append(IDs[j])
    else:
      continue

print singleIDs
"""
ordered=list(set(IDs))
print ordered
print len(ordered)
 
