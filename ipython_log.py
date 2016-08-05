# IPython log file

get_ipython().magic('cd pwd')
get_ipython().magic('pwd ')
#[Out]# 'E:\\Users\\U1and0\\Dropbox\\Program\\python'
get_ipython().magic('cd SAtraceFit/')
get_ipython().magic('load filler')
# %load filler
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

def drange(start_time,end_time,step_time=timedelta(seconds=1)):
	'''
	__INTRODUCTION__
	**start_timeからend_timeまでの日時をイテレートするジェネレータ**


	__USAGE__

	```python:example
	start=datetime(2016,2,24,14,38,16)
	end=datetime(2016,3,4,14,38,17)
	step=timedelta(days=1)

	for i in drange(start,end,step):
		print(i)

	# --result--
	# 2016-02-24 14:38:16
	# 2016-02-25 14:38:16
	# 2016-02-26 14:38:16
	# 2016-02-27 14:38:16
	# 2016-02-28 14:38:16
	# 2016-02-29 14:38:16
	# 2016-03-01 14:38:16
	# 2016-03-02 14:38:16
	# 2016-03-03 14:38:16
	# 2016-03-04 14:38:16
	```

	* python バージョン2.7移行に対応
	* 引数は最低2つ、オプション1つ
		* start_time:rangeで生成する最初の日時(datetime型)
		* end_time:rangeで生成する最後の日時(datetime型)
		* [オプション]step_time:rangeで生成する日時の間隔(timedelta型)
			* デフォルト値は1秒間隔
			* 小数対応(hours=10.5←10時間30分ずつ増加)
	* 戻り値はイテレータ(datetime型)


	__ACTION__
	1. start_time, end_timeをエポック時間に直す
	2. step_timeをtotal_seconds()で秒に直す
	3. np.arange()関数でエポック秒のイテレータを返し、datetime型に直してイールドする
	'''
	for i in np.arange(datetime_to_epoch(start_time),datetime_to_epoch(end_time),step_time.total_seconds()):
		yield epoch_to_datetime(i)





'''
drange() TEST
'''
start=datetime(2016,2,24,14,38,16)
end=datetime(2016,3,4,14,38,17)
step=timedelta(days=1)

# seclist=[x for x in drange(start,end,step)]
# print(seclist)

for i in drange(start,end,step):
	print(i)
get_ipython().magic('logstart -o')
s=datetime(2016,2,23,12,56,52)
e=datetime(2016,3,3,12,47,54)
for i in drange(s,e):
    print(i)
print('Hello')
x=1
x
#[Out]# 1
t=timedelta(days=1)
drange(s,e,t)
#[Out]# <generator object drange at 0x000002A6AE56B2B0>
for i in drange(s,e,t)
for i in drange(s,e,t):
for i in drange(s,e,t):print(i)
t=timedelta(days=2,hours=1,minutes=5,seconds=2)
for i in drange(s,e,t):print(i)
t=timedelta(days=0.5,seconds=0.5)
for i in drange(s,e,t):print(i)
t=timedelta(days=-1)
for i in drange(s,e,t):print(i)
e=datetime(2016,2,23,12,56,52)
s=datetime(2016,3,3,12,47,54)
for i in drange(s,e,t):print(i)
get_ipython().magic('logstop')
get_ipython().magic('logstart -o')
s=datetime(2016,2,23,12,56,52)
e=datetime(2016,2,23,12,56,58)
for i in drange(s,e):print(i)
get_ipython().magic('logstop')
s=datetime(2016,2,23,12,56,52)
e=datetime(2016,3,3,12,47,54)
for i in drange(s,e):print(i)
get_ipython().magic('reset')
get_ipython().magic('load filter')
get_ipython().magic('load filler')
# %load filler
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

def drange(start_time,end_time,step_time=timedelta(days=1)):
	'''
	__INTRODUCTION__
	**start_timeからend_timeまでの日時をイテレートするジェネレータ**


	__USAGE__

	```python:example
	start=datetime(2016,2,24,14,38,16)
	end=datetime(2016,3,4,14,38,17)
	step=timedelta(days=1)

	for i in drange(start,end,step):
		print(i)

	# --result--
	# 2016-02-24 14:38:16
	# 2016-02-25 14:38:16
	# 2016-02-26 14:38:16
	# 2016-02-27 14:38:16
	# 2016-02-28 14:38:16
	# 2016-02-29 14:38:16
	# 2016-03-01 14:38:16
	# 2016-03-02 14:38:16
	# 2016-03-03 14:38:16
	# 2016-03-04 14:38:16
	```

	* python バージョン2.7移行に対応
	* 引数は最低2つ、オプション1つ
		* start_time:rangeで生成する最初の日時(datetime型)
		* end_time:rangeで生成する最後の日時(datetime型)
		* [オプション]step_time:rangeで生成する日時の間隔(timedelta型)
			* デフォルト値は1秒間隔
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
for i in drange(s,e):print(i)
s=datetime(2016,2,23,12,56,52)
e=datetime(2016,3,3,12,47,54)
for i in drange(s,e):print(i)
get_ipython().magic('logstop')
