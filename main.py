'''
<<<<<<< HEAD
## main.py ver6.1
=======
## main.py ver6.1.1

__UPDATE6.1.1__
fot Mfit test
>>>>>>> Mfit

__UPDATE6.1__
fittting の引数に周波数は入れない(fittingのforステートメント中にparameterから直接引っ張る)

__UPDATE6.0__
例外により中断されたら実行するtry~finally文追加


__UPDATE5.0__
ファイル名の指定(コンソールからインプットする)
>第一引数：作成するファイル名
>第二引数：取り込み元のファイル名(オプション)


__UPDATE4.0__
やっぱりwaveとcarrier分ける(fittingDiv3系列の前半のように)
やっぱりcsvの書き込みは1ファイルのfitting後ごとに行う



__UPDATE3.0__

* fittingの廃止→SN_PowerSearchに変更
* SN_PowerSearchに2つの関数
	* SN, Power作成
* csvは２つ吐き出す
	* SN
	* Power


__UPDATE2.4__
ファイル名はフルパスで受ける
globname.pyを新規作成

__UPDATE2.3__
データファイルの場所と注目すべき周波数はparameter.pyに記載

__INTRODUCTION__
各モジュールを動かすメインファイル

__ACTION__
引数:
dateFirst, dateLast : コンソールから入力、テストの際はコード内で書き換える
oldcsvS, newcsvS : コード内で書き換える

戻り値:なし(CSVファイルに書き込む)

1. datelistにより、フィッティングを行う最初の日付から最後の日付までのリストを抽出する。
コンソールに出力
2. (oldcsvS,newcsvS)で、読み込み元CSV, 書き込み先CSVファイルを指定する。
rawdataPathで、データの位置を指定する(日付)
3. parameterにより、inディレクトリとfittingに必要な周波数を指定する。
4. CSV_IOにより、CSVを読み込む。
5. fittingDivにより、fittingを行う。
6. CSV_IOにより、CSVを書き込む。


__USAGE__

* コマンドライン上にて`python main.py`で起動
	SN, powerを出力するcsvファイル名(ディレクトリパスと拡張子は抜き)の入力が求められる(例：ファイル名をhogehoge.csvとしたければ、`hogehoge`と入力する)
	フィッティング対象のデータの日付の入力が求められる`<最初の日付> <最後の日付>`。フォーマットはyymmdd形式(例：2015年11月1日の日付からにしたいときは`151101`と打ちこむ)
* CSV_IO.editCSV内でread, writeメソッドを1つの関数に収めた
	* fitting>read>translate>update>translate>writeの流れは1セット

__PLAN__

* プログラムを途中で止めるとこれまでの計算結果が記録されない
> writeメソッドが走るのはfor文の最後だから
> read, writeメソッドが走るタイミングを調整する
> keyboard interruptされたときにwriteメソッド機能するようにできる?
* 二重起動すると強制終了される
> マルチプロセス化ができない
> 書き込みが2重にくるからいけないんだと思う。
> 仕様として、月々ごとにまとめろ、とある
>> mainの親プロセスを作って、入力したら月々ごとにファイル名指定できるようにする？
* exe化する予定
> py2exe
* GUI化する予定
> TKinter
* csvの容量が大きくなるとプロセスの進行が遅れる
> 読み込みに時間がかかる
> 読み込みがfor文ごとにあるのがいけない
>> for文終了後に一気に書き込みできるようにする
>>> keyboard interruptされたときにwriteメソッド機能するようにしないと、プロセス中断すると計算結果がメモリとともに消えてしまう
* 日付だけでなく時間を引数にする
'''

import pandas as pd
import parameter
param=parameter.param()
## __CSV NAME__________________________
'''
# コンソールからファイル名を指定
# 新規にファイルを作成するときは古いファイルと新しいファイルの名前を同一にする
# 新しいファイルの入力を省けば自動的に古い名前と同一にしてくれる
# '''
oldinpS=input('Input SN file base name>>> ')
oldinpP=input('Input power file base name>>> ')

# print('古いファイル名old file base name と新しいファイル名new file base nameを同じにするとき、何も入力せずにEnter.')
# newinpS=input('Input new SN file base name>>> ')
# if not newinpS:newinpS=oldinpS
# print('古いファイル名old file base name と新しいファイル名new file base nameを同じにするとき、何も入力せずにEnter.')
# newinpP=input('Input new power file base name>>> ')
# if not newinpP:newinpP=oldinpP
newinpS=oldinpS
newinpP=oldinpP

inplist=[oldinpS,oldinpP,newinpS,newinpP]
csvlist=[oldcsvS,oldcsvP,newcsvS,newcsvP]=map(lambda inp: param['out']+'\\CSV\\'+inp+'.csv' ,inplist)    #入力したファイルベースネームをフルパスと拡張しつけて返す

## ____________________________
print('SN value :\n\tRead from %s\n\tWrite to %s'% (oldcsvS,newcsvS))    #読み込み元ファイル名(フルパス)、書き込み先ファイル名(フルパス)表示
print('Power value :\n\tRead from %s\n\tWrite to %s'% (oldcsvP,newcsvP))    #読み込み元ファイル名(フルパス)、書き込み先ファイル名(フルパス)表示





##__MAKE CSV__________________________
'''
oldcsvSを読み込んでnewcsvSに入れる
SNResultは空なのでoldcsvSがnewcsvSにコピーされるだけ
freqFreqで見出し行を作る
'''
SNResult,powerResult={},{}
freqFreq=param['freqWave']+param['freqCarrier']
freqFreq.sort()   #周波数のソート
outPath=param['out']    #出力先の親ディレクトリ

import CSV_IO as c
c.editCSV(oldcsvS,newcsvS,SNResult,freqFreq)
c.editCSV(oldcsvP,newcsvP,powerResult,freqFreq)









# ## __DATE LIST__________________________
# from datelist import datelist  #最初と最後の日付(yymmdd形式)を引数に、その間の日付をリストとして返す
# ## ____________________________
# '''コンソールから入力'''
# dateFirst=input('Input First Date>>> ')
# print('IF you wish Last Date=First Date THEN Enter without input.')
# dateLast=input('Input Last Date>>> ')
# if not dateLast:    #dateLastの入力がなければdateFirstと同じにする
# 	dateLast=dateFirst
# ## ____________________________
# '''開発環境内でリストの最初と最後を指定'''
# # dateFirst='151201'
# # dateLast='151201'
# dateList=datelist(dateFirst,dateLast)  #最初から最後の日付のリストを返す
# ## ____________________________
# # '''リストで指定'''
# # dateList=['151201']
# ## ____________________________

print('''
\n
<データファイルの選択方法>
データファイルのファイル名はタイムスタンプ(yyyymmdd_HHMMSS形式)で決められているので
ファイル名は時間で指定する。
pandas.daterangeの形式で指定すること。
http://pandas.pydata.org/pandas-docs/stable/generated/pandas.date_range.html

(例) 20160101,20160108 <<< 2016年1月1日から2016年1月8日までを1日ずつ出力
(例) 20160101,20160108, freq="H" <<< 2016年1月1日から2016年1月8日までを1時間ずつ出力
(例) 
''')
inp=input('Input date pandas format >>').split()
'''
input().sprit()はスペース区切りでリストの要素として
'''
dateList=d.date_range(inp)

print('\nNow extracting from these dates\n%s\n'% dateList)
import globname as g
filepath=g.globname(param['in'],dateList)    #dateList内の日付に測定されたファイル名のリスト(20151111_??????.txtが288×たくさん個)

try:
	# __FITTING__________________________
	for fitfile in filepath[0:] :
		import fitting as f
		import numpy as np
		data=np.loadtxt(fitfile)   #load text data as array
		if not len(data):continue    #dataが空なら次のループ
		fitRtn=f.fitting(fitfile)
		SNResult.update(fitRtn[0])    #fittingを行い、結果をSNResultに貯める
		powerResult.update(fitRtn[1])    #fittingを行い、結果をSNResultに貯める
		print('Now Fitting',fitRtn[0].keys())
		# print('Write to SN\n', fitRtn[0])
		# print('Write to Power\n', fitRtn[1])

except KeyboardInterrupt:
	print('Why do you interrupt me!?')


finally:
	## __WRITEING__________________________
	# print('Write to SN\n', SNResult)   #標準出力に結果を書き込む
	# print('Write to Power\n', powerResult)
	c.editCSV(newcsvS,newcsvS,SNResult,freqFreq)    #newcsvSにフィッティング結果を書き込む
	c.editCSV(newcsvP,newcsvP,powerResult,freqFreq)    #newcsvSにフィッティング結果を書き込む
