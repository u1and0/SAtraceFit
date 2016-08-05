# coding: utf-8
from itertools import *
from more_itertools import *
from datetime import datetime, timedelta
import time

# def daterange(start_date, end_date):
# 	for n in range((end_date - start_date).seconds,,timedelta(minutes=5)):
# 		print(n)
# 		yield start_date + timedelta(seconds=n)

'''
daterange() TEST
start = datetime.strptime('20120601_230505', '%Y%m%d_%H%M%S')
end = datetime.strptime('20120601_235500', '%Y%m%d_%H%M%S')
for i in daterange(start, end):
	print(i)
'''



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




def datetime_to_epoch(d):
	return int(time.mktime(d.timetuple()))

def epoch_to_datetime(epoch):
	return datetime(*time.localtime(epoch)[:6])

def sec_range(start_time,end_time,timedeltatype):
	for i in range(datetime_to_epoch(start_time),datetime_to_epoch(end_time),timedeltatype.seconds):
		yield epoch_to_datetime(i)


start=datetime(2016,2,4,14,38,16)
end=datetime(2016,2,4,18,3,55)
step=timedelta(minutes=5)
# step=timedelta(minutes=5)
seclist=[x for x in sec_range(start,end,step)]
print(seclist)
