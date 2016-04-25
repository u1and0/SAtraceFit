'''
## glob_basename.py ver1.0

__UPDATE1.0__
first commit

__USAGE__
mainから呼び出す
引数:
	rootpath: 
	dateFirst:最初の日付yymmdd形式
	dateLast:最後の日付yymmdd形式
戻り値:リストfilebesename
 ~~イテレータでもいいな~~

globのhelpによるとリストを返すらしい
>    glob(pathname, *, recursive=False)
>        Return a list of paths matching a pathname pattern.


__INTRODUCTION__
最初と最後の日付をもらって、その中のfilebasename(拡張子無しのファイル名)

__ACTION__
datetime関数で日付の形式に直して
globの

__PLAN__
none
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








# def filebasename(a):
# 	'''filebasenameを取得'''
# 	for filename in a:
# 		import os
# 		filebasename=[os.path.basename(r)[:-4] for r in filename]    #拡張子'.txt'なので最後は必ず4文字だから-4
# 		return filebasename