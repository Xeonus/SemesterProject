#Easy case: all PCAs have a z-direction
#Distance between sections: 12.5
vectorlength=(maximum[2]-minimum[2]) / 12.5

histogramvector=[]
section=1
counter=0
for node, coord in getNodeCoordinates(tree).iteritems():
 x, y, z = coord
 section+=1
 distance=section*12.5
 if coord[3]=distance:
  counter+=1
  histogramvector.append(counter)
 counter=0
 if len(histogramvector)=lectorlength
  return histogramvector