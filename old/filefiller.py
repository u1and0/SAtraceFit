# coding: utf-8
version='filefiller.py ver3.2'
'''

__UPDATE3.2__
外部ファイルから呼び出せるようにMAINも関数化


__UPDATE3.1__
一番最後にプリントしているdatetimeObjectはディレクトリ上のファイルをgrepしたものではないので
再度ファイル数をgrepする
↓
grepする部分を関数化する


__UPDATE3.0__
yieldでファイル名吐き出し
そのたびにmakefile


__UPDATE2.0__
makefileの機能追加


__UPDATE1.0__
First commit

__USAGE__
directoryにはtxtファイルが詰まったディレクトリ名(最後に/必須)
extentionには拡張子
以上を入れてbuild

__INTRODUCTION__
あるディレクトリ内のtxtファイル(ファイル名=yyyymmdd_HHMMSS.txt)が00時00分～00時04分に始まり、23時55分～23時59分に終わるようにファイルを追加していく

__ACTION__
変数セット
datetimeObjectというリスト作成
datetimeObjectが5分間隔に並ぶように以下を行う
	makeStartPoint()
	makeMiddlePoint()
	makeStopPoint()

__TODO__
makeMiddlePoint()が不完全
	最後から2番目以前のデータを2以上消したときに288ファイルに埋めてくれない
	for文の繰り返しがいけないと思う
	while文にすべきか
'''


import numpy as np
import datetime
d=datetime
import glob


def grepfile(directory,extention):
	fullpath=glob.glob(directory+'*'+extention)   #ファイル名をリストに格納

	filename_without_extention=[i[len(directory):-1*len(extention)] for i in fullpath]   #ファイルベースネーム

	datetimeObject=[d.datetime.strptime(i,'%Y%m%d_%H%M%S') for i in filename_without_extention]   #要素がdatetime形式のリスト作成

	return datetimeObject


def makefile(fullpath):
	with open(fullpath,mode='w') as f:
		c='# <This is DUMMY DATA made by %s>\n'% version
		for i in range(1001):
			c+=str(i).rjust(6)+('-1000.00'.rjust(11))*3+'\n'
		c+='# <eof>\n'
		f.write(c)



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




def makeMiddlePoint():
	'''リスト内2個組で差分が6分未満になるように要素を作製'''
	for two in chunks(datetimeObject,2):   #リストの2組ずつgenerate
		print(two)
		if two[-1]-two[0]>=d.timedelta(minutes=6):
			print('\n',two[0],'\n',two[-1],'\n','diff=',two[-1]-two[0])
			where=datetimeObject.index(two[-1])
			time=two[0]+d.timedelta(minutes=5)
			datetimeObject.insert(where,time)   #調べた2くくりの要素間に+5分した要素を追加
			print('Inserted',time)
			yield time.strftime('%Y%m%d_%H%M%S')
	print('\nmakeMiddlePoint END\n')

# def makeMiddlePoint():
# 	'''リスト内2個組で差分が6分未満になるように要素を作製'''
# 	while datetimeObject[-1]-datetimeObject[-2]>=d.timedelta(minutes=6):
# 	# if datetimeObject[-2].hour==23 and 50<=datetimeObject[-2].minute<55:break
# 	for two in chunks(datetimeObject,2):
# 		print(two)
# 		where=datetimeObject.index(two[-1])
# 		time=two[0]+d.timedelta(minutes=5)
# 		datetimeObject.insert(where,time)   #調べた2くくりの要素間に+5分した要素を追加
# 		print('Inserted',time)
# 		yield time.strftime('%Y%m%d_%H%M%S')
# 	print('\nmakeMiddlePoint End\n')




	# 	for two in chunks(datetimeObject,2):   #リストの2組ずつgenerate
	# 		if two[-1]-two[0]>=d.timedelta(minutes=6):
	# 			print('\n',two[0],'\n',two[-1],'\n','diff=',two[-1]-two[0],'\n')
	# 			where=datetimeObject.index(two[-1])
	# 			time=two[0]+d.timedelta(minutes=5)
	# 			datetimeObject.insert(where,time)   #調べた2くくりの要素間に+5分した要素を追加
	# 			print('Inserted',time)
	# 			yield time.strftime('%Y%m%d_%H%M%S')
	# print('\nmakeMiddlePoint End\n')





def makeStartPoint():
	'''始点要素の作製'''
	while True :
		start=datetimeObject[0]   #始点を探す
		if start.hour==0 and 0<=start.minute<5:   #始点の条件クリアでループ終了
			print('\nFirst element is',start)
			print('makeStartPoint END\n')
			break
		datetimeObject.insert(0,start-d.timedelta(minutes=5))   #リストの最初に5分前の値をリストに格納
		print('Inserted',datetimeObject[0])
		yield datetimeObject[0].strftime('%Y%m%d_%H%M%S')


def makeStopPoint():
	'''終点要素の作製'''
	while True :
		stop=datetimeObject[-1]   #始点を探す
		if stop.hour==23 and 55<=stop.minute<60:   #始点の条件クリアでループ終了
			print('\nLast element is',stop)
			print('makeStopPoint END\n')
			break
		datetimeObject.append(stop+d.timedelta(minutes=5))   #リストの最初に5分前の値をリストに格納
		print('Appended',datetimeObject[-1])
		yield datetimeObject[-1].strftime('%Y%m%d_%H%M%S')




# __MAIN__________________________

def filefiller(directory,extention='.txt'):
	datetimeObject=grepfile(directory,extention)
	print('Before:Number of Files is',len(datetimeObject))   #Check number of files
	print('-'*20)
	for i in makeMiddlePoint(datetimeObject):makefile(directory+i+extention)
	print('-'*20)
	for i in makeStartPoint(datetimeObject):makefile(directory+i+extention)
	print('-'*20)
	for i in makeStopPoint(datetimeObject):makefile(directory+i+extention)
	print('-'*20)
	print('After:Number of Files is',len(grepfile(directory,extention)))   #Check number of files





'''
TEST
filefiller('C:/home/gnuplot/SAout/160717/')
'''

'''
TEST2
'''
directory='C:/home/gnuplot/SAout/160717/'
extention='.txt'
datetimeObject=grepfile(directory,extention)
print('Before',len(datetimeObject))

function=['makeMiddlePoint()','makeStartPoint()','makeStopPoint()']
for func in function:
	for filename in eval(func):
		pass
		# makefile(directory+filename+extention)

# datetimeObject=grepfile(directory,extention)
print('After',len(datetimeObject))



