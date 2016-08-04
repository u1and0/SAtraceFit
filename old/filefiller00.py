# coding: utf-8
import numpy as np
import datetime
d=datetime
import glob



'''
リストの最初(0)と最後(5)とリストの長さ(5)を与えて、4要素しかないリストを5要素に穴埋め
'''

# sample='20151201_000500'
# print(d.datetime.strptime(sample,'%Y%m%d_%H%M%S'))

# a=[0,5,15,20]
# b=np.linspace(a[0],a[3],5)
# print(b)







'''
リストの最初と最後を与えて、288データに補完する
→最初と最後の差が大きく、linespace()では全体が書き換わってしまう
'''

directory='C:/home/gnuplot/SAout/160607/rawdata/trace/'
extention='.txt'

fullpath=glob.glob(directory+'*'+extention)   #ファイル名をリストに格納

filename_without_extention=[i[len(directory):-1*len(extention)] for i in fullpath]   #ファイルベースネーム

datetimeObject=[d.datetime.strptime(i,'%Y%m%d_%H%M%S') for i in filename_without_extention]   #要素がdatetime形式のリスト作成

datetimeObjectHourmin=[int(i.strftime('%H%M')) for i in datetimeObject]   #要素が"時間と分"のリスト作成

# [start,stop]=[datetimeObjectHourmin[0],datetimeObjectHourmin[-1]]
# datetimeObjectHourminFix=np.linspace(start,stop,288)



# datetimeObjectHourminFixRound=[round(i) for i in datetimeObjectHourminFix]


# print(datetimeObjectHourmin)
# print(datetimeObjectHourminFix)
# print(datetimeObjectHourminFixRound)
# print('Length',len(datetimeObjectHourmin),'>>>',len(datetimeObjectHourminFixRound))













'''
リストの2要素ずつチェックしていく
→部分的に1ファイル抜けていれば補完してくれる
→まとめて2以上抜けていても1個しか補完してくれない
'''
# directory='C:/home/gnuplot/SAout/160607/rawdata/trace/'
# extention='.txt'


# fullpath=glob.glob(directory+'*'+extention)

# filename_without_extention=[i[len(directory):-1*len(extention)] for i in fullpath]

# datetimeObject=[d.datetime.strptime(i,'%Y%m%d_%H%M%S') for i in filename_without_extention]

# datetimeObjectHourmin=[int(i.strftime('%H%M')) for i in datetimeObject]






# '''リスト内包表記で2グループに分割'''
# dif=d.timedelta(minutes=5)
# # dif2=d.timedelta(minutes=5)
# twolist=[datetimeObject[i:i+2] for i in range(len(datetimeObject))]
# del twolist[-1]   #2個ずつまとめたとき、最後の要素は必ず「一人ぼっち」だから消す
# for i in twolist:
# 	if not dif-d.timedelta(minutes=1)<i[-1]-i[0]<dif+d.timedelta(minutes=1):   #前の計測から次の計測間隔が4~6分以内でなければ
# 		# print(i)
# 		# print(i[-1]-i[0]!=dif)
# 		# print(i[-1]-i[0])
# 		datetimeObject.append(i[0]+dif)
# # print(datetimeObject,len(datetimeObject))








def chunks(l, n):
	'''
	l:リスト
	n:数字
	lからnずつgenerate
	'''
	for i in range(len(l)):
		yield l[i:i + n]

'''chunks TEST
ll=[1,5,23,6,3,6,7]
print(list(chunks(ll,2)))
# Excute Result
# [[1, 5], [5, 23], [23, 6], [6, 3], [3, 6], [6, 7], [7]]
'''




def twoGroups():
	'''リスト内2個組で差分が6分未満になるように要素を作製'''
	for two in chunks(datetimeObject,2):   #リストの2組ずつgenerate
		# if two[0]==datetimeObject[-1]:break   #
		if two[-1]-two[0]>=d.timedelta(minutes=6):
			print(two[-1],two[0],two[-1]-two[0])
			where=datetimeObject.index(two[-1])
			time=two[0]+d.timedelta(minutes=5)
			datetimeObject.insert(where,time)   #調べた2くくりの要素間に+5分した要素を追加
			print('Inserted',time,'next to',two[0])
		# elif two[-1]-two[0]<d.timedelta(minutes=4):break
	print('Insert element End')







def makeStartPoint():
	'''始点要素の作製'''
	while True :
		start=datetimeObject[0]   #始点を探す
		if start.hour==0 and 0<=start.minute<5:   #始点の条件クリアでループ終了
			print('Insert start END')
			break
		datetimeObject.insert(0,start-d.timedelta(minutes=5))   #リストの最初に5分前の値をリストに格納
		print('Inserted',datetimeObject[0])


def makeStopPoint():
	'''終点要素の作製'''
	while True :
		stop=datetimeObject[-1]   #始点を探す
		if stop.hour==23 and 55<=stop.minute<60:   #始点の条件クリアでループ終了
			print('insert stop END')
			break
		datetimeObject.append(stop+d.timedelta(minutes=5))   #リストの最初に5分前の値をリストに格納
		print('Appended',datetimeObject[-1])





# __main__________________________
print('Before',datetimeObject,len(datetimeObject))
makeStartPoint()
twoGroups()
makeStopPoint()
print('After',datetimeObject,len(datetimeObject))










