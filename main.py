'''
## main.py v7.0.0


__USAGE__
コマンドライン上で`python main.py`で実行

__INTRODUCTION__
SAtraceFitの実行ファイル

1. データソースからのテキストにフィッティングをかけて
2. 結果をcsvに書き込み
3. フィッティング結果を反映したスペクトラム図のpngを吐き出す
	* csvファイル名はユーザーの入力
	* csvファイル出力先はmain.pyに書き込まれている
	* pngファイル出力先はfitting.plotshowing()に書き込まれている。



__ACTION__

<実行したときの、コマンドラインの表示の流れ>

1. データファイル、出力ファイルのディレクトリ指定→parameter.pyで指定
2. SNを書き込むcsvファイル名を聞かれる→入力する
3. powerを書き込むcsvファイル名を聞かれる→入力する
4. csvのフルパス表示
5. 日付を指定(指定方法がメッセージで表示される。詳しくはdatelist.date_range_input()参照)
	6. fitting.fitting()実行。詳しくはfitting.fitting()参照
	7. フィッティング日時表示
	8. フィッティング結果表示(5の日付指定が最後に来るまで繰り返し)



__UPDATE7.0.0__
ファイル名は日時指定で引っ張ってくる

__UPDATE6.1.1__
fot Mfit test

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
'''


# __BUILTIN MODULES__________________________
import pandas as pd
import numpy as np
import glob
# __USER MODULES__________________________
import fitting as f
import parameter
param=parameter.param()   #パラメータの読み込み
import datelist as dl
import CSV_IO as c



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

c.editCSV(oldcsvS,newcsvS,SNResult,freqFreq)
c.editCSV(oldcsvP,newcsvP,powerResult,freqFreq)



try:
	# __FITTING__________________________
	for d in dl.date_range_input():   #pd.date_rangeの引数をinput方式にカスタマイズした
		for i in d:
			print('\n'+'_'*20+'\n次の日時のファイルをfittingします。\n',i)
			for fitfile in glob.iglob(param['in']+i+'*'):
				data=np.loadtxt(fitfile)   #load text data as array
				if not len(data):continue    #dataが空なら次のループ
				fitRtn=f.fitting(fitfile)
				SNResult.update(fitRtn[0])    #fittingを行い、結果をSNResultに貯める
				powerResult.update(fitRtn[1])    #fittingを行い、結果をpowerResultに貯める
				print('')
				print('Now Fitting...',fitfile[-19:])
				print('Write to SN...', list(fitRtn[0].values())[0])
				print('Write to Power...', list(fitRtn[1].values())[0])
except KeyboardInterrupt:
	raise
finally:
	## __WRITEING__________________________
	# print('Write to SN\n', SNResult)   #標準出力に結果を書き込む
	# print('Write to Power\n', powerResult)
	c.editCSV(newcsvS,newcsvS,SNResult,freqFreq)    #newcsvSにフィッティング結果を書き込む
	c.editCSV(newcsvP,newcsvP,powerResult,freqFreq)    #newcsvSにフィッティング結果を書き込む
	print('')
	print('%sにSN値を書き込みました'% newcsvS)
	print('%sにpower値を書き込みました'% newcsvP)
