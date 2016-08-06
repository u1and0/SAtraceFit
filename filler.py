# coding: utf-8
# from itertools import *
# from moreitertools import *
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




def datetime_to_epoch(d):
	return int(time.mktime(d.timetuple()))

def epoch_to_datetime(epoch):
	return datetime(*time.localtime(epoch)[:6])

def drange(end_time,start_time=epoch_to_datetime(0),step_time=timedelta(days=1)):
	'''
	__INTRODUCTION__
	start_timeからend_timeまでの日時をイテレートするジェネレータ


	__USAGE__

	```python:example
	start=datetime(2016,2,24,14,38,16)
	end=datetime(2016,3,4,14,38,17)
	step=timedelta(days=2)

	for i in drange(start,end,step):
		print(i)

	# --result--
	# 2016-02-24 14:38:16
	# 2016-02-26 14:38:16
	# 2016-02-28 14:38:16
	# 2016-03-01 14:38:16   # ←うるう年なので2/29が間に入っている
	# 2016-03-03 14:38:16
	```

	* python バージョン2.7移行に対応
	* 引数は最低2つ、オプション1つ
		* start_time:rangeで生成する最初の日時(datetime型)
		* end_time:rangeで生成する最後の日時(datetime型)
		* [オプション]step_time:rangeで生成する日時の間隔(timedelta型)
			* デフォルト値は1日間隔
			* 小数対応
				* hours=10.5←10時間30分ずつ増加)
			負の実数対応
				* hours=-1←1時間ずつ戻す。
				* ただし、start_timeよりend_timeが早い時間でないと何も返さない)
	* 戻り値はイテレータ(datetime型)


	__ACTION__

	1. start_time, end_timeをエポック時間に直す
	2. step_timeをtotal_seconds()で秒に直す
	3. np.arange()関数でエポック秒のイテレータを返し、datetime型に直してイールドする
	'''
	for i in np.arange(datetime_to_epoch(start_time),datetime_to_epoch(end_time),step_time.total_seconds()):
		yield epoch_to_datetime(i)


'''
TEST
'''
e=datetime(1971,1,1)
s=datetime(1972,1,1)

for i in drange(s,e):
	print(i)