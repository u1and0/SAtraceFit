# coding: utf-8
from itertools import *
from more_itertools import *
from datetime import datetime, timedelta
import time
import numpy as np


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



'''TEST
li=[[1,50],[0,8,10,16],[1,5,9,11,14,15]]
for x in li:
	print(fill(x,10))
	# print(bool(fill(x)==list(range(x[0],x[-1]+1))))
'''




def daterange(start_date, end_date,step=1):
	for n in range((end_date - start_date).days):
		yield start_date + timedelta(n)

'''
daterange() TEST
'''
# start=datetime(2016,2,1)
# end=datetime(2016,3,5)

# # for i in daterange(start, end):
# # 	print(i)




def datetime_to_epoch(d):
	return int(time.mktime(d.timetuple()))

def epoch_to_datetime(epoch):
	return datetime(*time.localtime(epoch)[:6])

def datetimerange(start_time,end_time,step_time=timedelta(seconds=1)):
	for i in np.arange(datetime_to_epoch(start_time),datetime_to_epoch(end_time),step_time.total_seconds()):
		yield epoch_to_datetime(i)

'''
datetimerange() TEST
'''
start=datetime(2016,2,4,14,38,16)
end=datetime(2016,2,4,20,39,55)
step=timedelta(minutes=10.5)

# seclist=[x for x in datetimerange(start,end,step)]
# print(seclist)

for i in datetimerange(start,end,step):
	print(i)