datetimeをイテレートするrange、名付けて"drange()"作った


__INTRODUCTION__
start_timeからend_timeまでの日時をイテレートするジェネレータ


__USAGE__

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




```python:drange.py
from datetime import datetime, timedelta
import time
import numpy as np

def datetime_to_epoch(d):
	return int(time.mktime(d.timetuple()))

def epoch_to_datetime(epoch):
	return datetime(*time.localtime(epoch)[:6])

def drange(start_time,end_time,step_time=timedelta(seconds=1)):

	for i in np.arange(datetime_to_epoch(start_time),datetime_to_epoch(end_time),step_time.total_seconds()):
		yield epoch_to_datetime(i)
```







```python:引数2つ
s=datetime(2016,2,23,12,56,52)
e=datetime(2016,3,3,12,47,54)
for i in drange(s,e):print(i)

# Out#
# 2016-02-23 12:56:52
# 2016-02-24 12:56:52
# 2016-02-25 12:56:52
# 2016-02-26 12:56:52
# 2016-02-27 12:56:52
# 2016-02-28 12:56:52
# 2016-02-29 12:56:52
# 2016-03-01 12:56:52
# 2016-03-02 12:56:52
```








