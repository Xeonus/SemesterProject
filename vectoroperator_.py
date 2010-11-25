#test of class-environment
class v_operator:
	def __init__(self, x, x1, x2, y1, y2):
		self.x= [x1, x2]
		self.y= [y1, y2]
		
	def __mult__(self):
	for x, y in zip([x1, x2], [y1, y2]):
		return self.x * self.y
	def __add__(self):
		return self.x + self.y

test1 = v_operator([1,2], [1,2])
print test1.mult()