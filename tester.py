container={}
condition=[]


for nt in range(50,250, 5):
  result=[]
  for i in range(10, 200, 5):
    condition= nt/i #tester(nt, i)
    result.append(condition)
  container[nt]=result
print container

