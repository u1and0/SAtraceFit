'''
## globname.py ver1.1

__UPDATE1.1__
拡張子無しファイル名入力`globfullname`関数追加

__UPDATE1.0__
first commit

__USAGE__
mainから呼び出す
引数:
	rootpath: 
	dateFirst:最初の日付yymmdd文字列が入ったリスト形式形式
	dateLast:最後の日付yymmdd文字列が入ったリスト形式形式
戻り値:
	filebesename:リスト形式


__INTRODUCTION__
rootroot()下のファイルのフルパスを返す。
ただし、最初と最後の日付をもらって、その間にある日付のファイルに限る

__ACTION__
datetime関数で日付の形式に直して
globの

__PLAN__
時間を引数にする
'''


def globname(rootpath,dateList):
	'''rootpath内のファイルのフルパスを返す
	ただし、ファイル名が日付dateListの中による'''
	filename=[]
	for i in dateList:
		import glob
		filename+=glob.glob(rootpath+'20'+i+'*.txt')   #上で指定したディレクトリから.txt形式のデータをglob
	return filename






'''
TEST
## __DATE LIST__________________________
from datelist import datelist  #最初と最後の日付(yymmdd形式)を引数に、その間の日付をリストとして返す
# dateFirst=input('Input First Date>>> ')
# dateLast=input('Input Last Date>>> ')
# if not (len(dateFirst)==6 or len(dateLast)==6):
# 	print('Input as \'yymmdd\'')
# 	print('Example >>> 2016/5/12')
# 	print('You must type \'160512\'')
# 	break
## ____________________________
dateFirst='160110'
dateLast='160111'
dateList=datelist(dateFirst,dateLast)  #最初から最後の日付のリストを返す
# dateList=datelist(dateBet[0],dateBet[1])  #最初から最後の日付のリストを返す
print('\ndateList\n',dateList)

import confidential
from confidential import rootroot
print(globname(rootroot(),dateList))
'''



def globfullname(rootpath,f):
	'''rootpath内のファイルのフルパスを返す'''
	filename=rootpath+f+'.txt'
	return filename






# def filebasename(a):
# 	'''filebasenameを取得'''
# 	for filename in a:
# 		import os
# 		filebasename=[os.path.basename(r)[:-4] for r in filename]    #拡張子'.txt'なので最後は必ず4文字だから-4
# 		return filebasename
