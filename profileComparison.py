#Subpart to extract coordinates of tree
from machine_ import trainClassifier

IDvector1=[] #laoded in from function of extractor for now it is empty
IDvector2=[] #has other trees downstream in it
matches=[]

#def profileComparison(list1, list2)
#Idea: compare one entry of list1 with all the other entries of list2.
#If there is a match, output the corresponding IDs
def matchFinder(list1, list2):
  for i in range(0, len(list1)):
    for j in range(0, len(list2)):
      if trainClassifier([list1[i].verts, list2[j].verts) ==1:
        match=[list1[i], list2[j]]
        print match

mismatches=(float(len(list1)))**2 - matches
print "There were", len(matches), "matches, and", mismatches, "mismatches found."
print "Following IDs match:", matchFinder(list1, list2) 