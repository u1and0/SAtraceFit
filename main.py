'''
## main.py ver2.3

__UPDATE2.3__
データファイルの場所と注目すべき周波数はconfidential.pyに記載

__INTRODUCTION__
各モジュールを動かすメインファイル

__ACTION__
引数:
dateFirst, dateLast : コンソールから入力、テストの際はコード内で書き換える
oldcsv, newcsv : コード内で書き換える

戻り値:なし(CSVファイルに書き込む)

1. datelistにより、フィッティングを行う最初の日付から最後の日付までのリストを抽出する。
コンソールに出力
2. (oldcsv,newcsv)で、読み込み元CSV, 書き込み先CSVファイルを指定する。
rawdataPathで、データの位置を指定する(日付)
3. confidentialにより、rootディレクトリとfittingに必要な周波数を指定する。
4. CSV_IOにより、CSVを読み込む。
5. fittingDivにより、fittingを行う。
6. CSV_IOにより、CSVを書き込む。


__USAGE__

+ コマンドライン上にて`python main.py <最初の日付> <最後の日付>`
	+ フォーマットはyymmdd形式(例えば2015年11月1日=151101と打ちこむ)
+ CSV_IO.editCSV内でread, writeメソッドを1つの関数に収めた
	+ fitting>read>translate>update>translate>writeの流れは1セット

__PLAN__

+ プログラムを途中で止めるとこれまでの計算結果が記録されない
> writeメソッドが走るのはfor文の最後だから
> read, writeメソッドが走るタイミングを調整する
+ 二重起動すると強制終了される
> マルチプロセスかができない
+ exe化する予定
> py2exe
+ GUI化する予定
> TKinter
'''
from datelist import datelist  #最初と最後の日付(yymmdd形式)を引数に、その間の日付をリストとして返す

## __DATE LIST__________________________
# dateFirst=input('Input First Date>>> ')
# dateLast=input('Input Last Date>>> ')
## ____________________________
dateFirst='160110'
dateLast='160125'

dateList=datelist(dateFirst,dateLast)  #最初から最後の日付のリストを返す
# dateList=datelist(dateBet[0],dateBet[1])  #最初から最後の日付のリストを返す
print('\ndateList\n',dateList)

## __READ DATA FROM OLD CSV__________________________
(oldcsv,newcsv)=('./160419.csv','./160419.csv')
fittingResult={}
from confidential import freq
freqWave=freq()
from confidential import root
rootPath=root()

import CSV_IO as c
c.editCSV(oldcsv,newcsv,fittingResult,freqWave)
	#oldcsvを読み込んでnewcsvに入れる
	#fittingResultは空なのでoldcsvがnewcsvにコピーされるだけ

## __FILE BASE NAME__________________________
for datedir in dateList:
	import glob,os
	rawdataPath=str(rootPath)+str(datedir)+'\\rawdata\\trace'
	print(rawdataPath)
	filename=glob.glob(rawdataPath+'\\*.txt')
	filebasename=[os.path.basename(r)[:-4] for r in filename]    #filebasenameを取得
	if filebasename:
		print('\nfilebasename\n',filebasename)
	else:
		print('\nNo file in',rawdataPath,'!!!\n')




	# __FITTING__________________________
	for fitfile in filebasename :
		from fittingDiv38 import fitting
		fittingResult.update(fitting(rawdataPath,fitfile,freqWave))    #fittingを行い、結果をfittingResultに貯める


		c.editCSV(newcsv,newcsv,fittingResult,freqWave)    #newcsvにフィッティング結果を書き込む
		fittingResult={}    #fittingResultのリセット
