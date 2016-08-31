'''
## datelist.py ver1.0

__INTRODUCTION__
main.pyから2つの値が渡される
2つの間の日付のリストを返す

__ACTION__
yymmdd形式の6桁をdatetime関数で日付にする
ddate1,2に代入する
ddate1がddate2になるまで(while)
ddate1を1日ずつ足して、リストに追加する(append)

__USAGE__
引数 : 最初の日付yymmdd形式、最後の日付yymmdd形式
戻り値 : 最初の日付から最後の日付を入れたリストyymmdd形式

__UPDATE1.0__
first commit

## PLAN
none
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



import pandas as pd
def date_range_input():
	'''
	ファイル名のglobに用いる日付を基にした文字列をyieldするgenerator
	引数:なし(ユーザーに入力施す)
	戻り値:
		datestr:文字列(%Y%m%d形式)
	'''
	print('''
ファイル名を日時から指定します。

<使い方>
`始めの日時,終わりの日時,<数字D|数字H>`

* 少なくとも2つの引数
* カンマで区切る
* 時間を指定するときは、日付6文字の後にスペースやハイフンで区切る(例参照)
* 日時指定はpandas.daterangeの形式で指定すること。
	* http://pandas.pydata.org/pandas-docs/stable/generated/pandas.date_range.html
* 3つめの引数はD:day H:hour　ごとにイテレート

(例) 20160101,20160108 <<< 2016年1月1日から2016年1月8日までを1日ずつ出力
(例) 20160101,20160108, 5D <<< 2016年1月1日から2016年1月8日までを5日おきに出力
(例) 20160101 01,20160108 12, H <<< 2016年1月1日1時から2016年1月8日12時までを1時間おきに出力
(例) 20160101 01,20160108 12, 2H <<< 2016年1月1日1時から2016年1月8日12時までを2時間おきに出力

	''')

	while True:
		try:
			inp=input('pandas.date_range型で入力 >>').split(',')   #input().sprit()はスペース区切りでリストの要素として
			if len(inp)==2:
				datelist=pd.date_range(inp[0],inp[1])
				datestr=datelist.strftime('%Y%m%d')
				break
			elif 'D' in inp[2]:
				datelist=pd.date_range(inp[0],inp[1],freq=inp[2])
				datestr=datelist.strftime('%Y%m%d')
				break
			elif 'H' in inp[2]:
				datelist=pd.date_range(inp[0],inp[1],freq=inp[2])
				datestr=datelist.strftime('%Y%m%d_%H')
				break
		except KeyboardInterrupt:
			raise
		except:
			print('入力が間違っています')
	yield datestr

'''TEST date_range_input()
# リスト内包表記
print([i for i  in date_range_input()])
'''

'''TEST date_range_input()
# %Y%m%d形式に直して出力
for i in date_range_input():
	print(i)
'''
