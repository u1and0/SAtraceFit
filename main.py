'''
## main.py ver3.0

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
データファイルの場所と注目すべき周波数はconfidential.pyに記載

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
3. confidentialにより、rootディレクトリとfittingに必要な周波数を指定する。
4. CSV_IOにより、CSVを読み込む。
5. fittingDivにより、fittingを行う。
6. CSV_IOにより、CSVを書き込む。


__USAGE__

* コマンドライン上にて`python main.py <最初の日付> <最後の日付>`
	* フォーマットはyymmdd形式(例えば2015年11月1日=151101と打ちこむ)
* CSV_IO.editCSV内でread, writeメソッドを1つの関数に収めた
	* fitting>read>translate>update>translate>writeの流れは1セット

__PLAN__

* プログラムを途中で止めるとこれまでの計算結果が記録されない
> writeメソッドが走るのはfor文の最後だから
> read, writeメソッドが走るタイミングを調整する
* 二重起動すると強制終了される
> マルチプロセスかができない
* exe化する予定
> py2exe
* GUI化する予定
> TKinter
* ファイル名の指定
>第一引数：作成するファイル名
>第二引数：取り込み元のファイル名(オプション)
'''


## __READ DATA FROM OLD CSV__________________________
import confidential as co
# inp=input('Input File name>>> ')
# oldcsvS=newcsvS=co.root()+inp+'.csv'
## ____________________________
(oldcsvS,newcsvS)=(co.root()+'\\SN.csv',co.root()+'\\SN.csv')
(oldcsvP,newcsvP)=(co.root()+'\\P.csv',co.root()+'\\P.csv')
(fittingResult,powerResult)=({},{})
freqFreq=co.freqWave()+co.freqCarrier()
rootPath=co.root()

import CSV_IO as c
c.editCSV(oldcsvS,newcsvS,fittingResult,freqFreq)
c.editCSV(oldcsvP,newcsvP,powerResult,freqFreq)
	#oldcsvSを読み込んでnewcsvSに入れる
	#fittingResultは空なのでoldcsvSがnewcsvSにコピーされるだけ


## __DATE LIST__________________________
from datelist import datelist  #最初と最後の日付(yymmdd形式)を引数に、その間の日付をリストとして返す
# dateFirst=input('Input First Date>>> ')
# dateLast=input('Input Last Date>>> ')
## ____________________________
dateFirst='160129'
dateLast='160130'
dateList=datelist(dateFirst,dateLast)  #最初から最後の日付のリストを返す
# dateList=datelist(dateBet[0],dateBet[1])  #最初から最後の日付のリストを返す
print('\nNow extracting from these dates.\n',dateList)

import globname as g
filepath=g.globname(co.rootroot(),dateList)

# __FITTING__________________________
for fitfile in filepath :
	import SN_PowerSearch as s
	import numpy as np
	data=np.loadtxt(fitfile)   #load text data as array
	if not len(data):continue    #dataが空なら次のループ
	fittingResult.update(s.SNSearch(fitfile,co.freqWave(),co.freqCarrier()))    #fittingを行い、結果をfittingResultに貯める
	powerResult.update(s.PowerSearch(fitfile,co.freqWave(),co.freqCarrier()))    #fittingを行い、結果をfittingResultに貯める

print('Write to SN', fittingResult)
print('Write to Power', powerResult)

c.editCSV(newcsvS,newcsvS,fittingResult,freqFreq)    #newcsvSにフィッティング結果を書き込む
c.editCSV(newcsvP,newcsvP,powerResult,freqFreq)    #newcsvSにフィッティング結果を書き込む
(fittingResult,powerResult)=({},{})    #fittingResultのリセット
