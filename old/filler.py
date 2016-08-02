def chunks(l, n):
	'''
	l:リスト
	n:数字
	lからnずつgenerate
	'''
	for i in range(len(l)):
		yield l[i:i + n]

def fill(x):
	x.append(x[-1]+1)
	for two in chunks(x,2):
		print(two)
		if two[-1]-two[0]>1:
			x.insert(x.index(two[-1]),two[0]+1)
			print('insert',two[0]+1)
	x.pop()




x=[0,3,4,5,5]
fill(x)
print(x)
