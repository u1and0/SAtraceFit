'''
main.py ver2.1
<INTRODUCTION>
2つの日付を表す引数からその間にある日付のリストを返す
<ACTION>
引数:最初の日付、最後の日付
戻り値:最初の日付から最後の日付まで1日ずつ足していったリスト
<USAGE>
コマンドライン上にて
python main.py <最初の日付> <最後の日付>
フォーマットはyymmdd形式
<UPDATE>
CSVread, CSVwriteは最後に出力
それまではfittingResultにためる
書き込みファイルと読み込みファイルを分けた
<PLAN>
プログラムを途中で止めるとこれまでの計算結果が記録されない
>>>writeメソッドが走るのはfor文の最後だから
read, writeメソッドが走るタイミングを調整する
read, writeメソッドを1つの関数に収めた
	fitting>read>translate>update>translate>writeの流れは1セット
'''
from datelist import datelist  #最初と最後の日付(yymmdd形式)を引数に、その間の日付をリストとして返す

## __DATE LIST__________________________
dateBet=('160101','160101')  #最初の日付、最後の日付を入力
dateList=datelist(dateBet[0],dateBet[1])  #最初から最後の日付のリストを返す
print('\ndateList\n',dateList)

## __READ DATA FROM OLD CSV__________________________
(oldcsv,newcsv)=('./SN160401_1.csv','./SN160401_1.csv')
fittingResult={}
freqWave=[22.2,23.4,24.0,24.25,24.8]   #帯域持った周波数
freqWave+=[23.0,24.1,24.5,25.0,25.1,25.2,25.5]   #キャリアのみの周波数
import CSV_IO as c
c.editCSV(oldcsv,newcsv,fittingResult,freqWave)
	#oldcsvを読み込んでnewcsvに入れる
	#fittingResultは空なのでoldcsvがnewcsvにコピーされるだけ

## __FILE BASE NAME__________________________
for datedir in dateList:
	import glob,os
	rawdataPath='\\\\sampanet.gr.jp\\DFS\\ShareUsers\\UserTokki\\Personal\\Maeno\\VLFsasebo'+'\\'+datedir+'\\rawdata\\trace'
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
