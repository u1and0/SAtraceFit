'''
## globname.py ver1.4

__UPDATE1.4__
os.basenameでフルパスではなくファイル名だけを表示

__UPDATE1.3.2__
'ファイル名は`20`で始まる文字列' の文を削除

__UPDATE1.3.1__
ファイル名とディレクトリの表示


__UPDATE1.3__
ファイル名は入力者にもワイルドカード使えるようにした。
filename=glob.glob(rootpath+num)   #上で指定したディレクトリから.txt形式のデータをglob


__UPDATE1.2__
`globregname`関数追加

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
import glob
import os


def globname(rootpath,dateList):
	'''rootpath内のファイルのフルパスを返す
	ただし、ファイル名が日付dateListの中による'''
	filename=[]
	for i in dateList:
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








def globregname(rootpath,num):
	'''rootpath内のファイルのフルパスを返す
	ファイル名は`20`で始まり、`.txt`で終わる文字列'''
	filename=glob.glob(rootpath+num+'.txt')   #上で指定したディレクトリから.txt形式のデータをglob
	print('\n____________________________')
	print('以下のディレクトリ内のファイルを検索します。\n',rootpath,'\n')
	print('____________________________')
	print('受け取ったコマンド:\n', num,'\n')
	print('____________________________\nコマンドから検索されるファイル名:')
	for i in filename:
		print(os.path.basename(i))
	return filename

'''
TEST
import confidential as co
print(globregname(co.root(),'201601??_2[13]*'))
'''
