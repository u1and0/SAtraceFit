# coding: utf-8
from itertools import *
from more_itertools import *
import datetime
d=datetime

def fill(li,ins):
	'''
	引数:
		li:リスト
		ins:int
	戻り値：編集を加えた、引数と同じリスト
	'''
	for two in list(pairwise(li)):   #liの中身を2つずつにわける
		print(two)
		if two[-1]-two[0]>ins:   #抜き出したタプルの要素の差がins上であれば
			for i in range(two[0]+ins,two[-1],ins):
				li.insert(li.index(two[-1]),i)   #タプルの要素間の場所にinsずつ増やした値を入れる
				print('insert',i)
		else:print('OK!')
	return li



'''TEST'''
li=[[1,50],[0,8,10,16],[1,5,9,11,14,15]]
for x in li:
	print(fill(x,10))
	# print(bool(fill(x)==list(range(x[0],x[-1]+1))))
