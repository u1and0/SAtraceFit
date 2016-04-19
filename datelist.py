'''
datelist.py ver1.0
<INTRODUCTION>
main.pyから2つの値が渡される
2つの間の日付のリストを返す
<ACTION>
yymmdd形式の6桁をdatetime関数で日付にする
ddate1,2に代入する
ddate1がddate2になるまで(while)
ddate1を1日ずつ足して、リストに追加する(append)
<USAGE>
引数 : 最初の日付yymmdd形式、最後の日付yymmdd形式
戻り値 : 最初の日付から最後の日付を入れたリストyymmdd形式
<UPDATE1.0>
first commit
<PLAN>
noen
'''
import datetime
d=datetime

def datelist(date1,date2):
	ddate1=d.datetime.strptime(date1,'%y%m%d')
	ddate2=d.datetime.strptime(date2,'%y%m%d')
	dateList=[ddate1.strftime('%y%m%d')]   #strfrimeでyymmdd形式に変換
	while ddate1!=ddate2:
		ddate1+=d.timedelta(1)   #ddate1の次の日
		dateList.append(ddate1.strftime('%y%m%d'))   #dateListにddate1追加#strfrimeでyymmdd形式に変換
	return dateList

## __TEST__________________________
# date1='160225'
# date2='160302'
# print(datelist(date1,date2))
##____________________________