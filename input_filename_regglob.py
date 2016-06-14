'''
## input_filename_regglob.py ver1.0

__UPDATE1.0__
First commit

__USAGE__
コマンドライン上で`input_filename_regglob.py`を走らせる
リスト化するファイル名を聞いてくるので表示される例に倣って入力する

__INTRODUCTION__
rootディレクトリ下のファイルをglobする
globはコマンドラインからユーザーが入力

__ACTION__
input関数
	正規表現でglobするファイル名を決める
yesno関数
	ユーザーからの入力(yまたはn)で次の処理(一覧に加えるか否か)を判断

__TODO__
None
'''
def howtouse():
	print('''
____________________________
<使い方>
グラフ化したいファイルベースネーム(拡張子抜きのファイル名)を入力
ワイルドカードも使えます！
	"*"0文字以上の文字列
	"?"1文字か0文字の文字列
	"[]"の中に書いた文字列一文字ずつ(たとえば[135]は"1か3か5", [2-8]は"2,3,4,5,6,7,8のどれか")
使える正規表現一覧: http://docs.python.jp/3/library/re.html
(例)20151201_000344	<<<2015/12/01 00:03:44のデータ
(例)*151201_000344	<<<2015/12/01 00:03:44のデータ
(例)*151201_000344*	<<<2015/12/01 00:03:44のデータ
(例)*151201_001*	<<<2015/12/01 0時10分～19分のデータ
(例)*151201_00*		<<<2015/12/01 00時台のデータ
(例)*151201_0*		<<<2015/12/01 0～9時台のデータ
(例)*151201*		<<<2015/12/01のデータ
(例)201601??_21*	<<<2016年1月??日のデータのうち、21時台のデータ
(例)*1201_19??56	<<<？年12月1日のデータのうち、19時台で56秒で終わっているデータ
(例)201601??_2[13]*	<<<2016年01月のデータのうち、21時台か23時台のデータ
____________________________''')





import sys, os
# sys.path.append('./SAtraceFit')  #importできるディレクトリ追加
from time import sleep


import globname as g
import confidential as co
def inp():
	filepath=[]
	while True:
		howtouse()
		filename=input('ファイル名を入力、またはEnterで確定>>> ')
		if not filename: 
			print('ファイル名の追加処理を終了します')
			sleep(1)
			break
		temp=g.globregname(co.root(),filename)
		message='''
____________________________
中断するときは`ctrl+c`
以上のファイルをグラフ化するファイル一覧に含めますか？(y/n)>>> '''
		import yesno
		app=yesno.yesno(message)
		if app=='y':
			filepath+=temp
			print('一覧に追加しました')
		elif app=='n':
			print('一覧に追加しませんでした')
		sleep(1)

	print('____________________________')
	for i in filepath:
		print(os.path.basename(i))
	print('''
____________________________
以上のファイルをグラフ化します
中断するときは`ctrl+c`
____________________________
	''')
	return filepath

inp()