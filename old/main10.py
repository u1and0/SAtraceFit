'''
main.py ver1.0
<INTRODUCTION>
2つの日付を表す引数からその間にある日付のリストを返す
<ACTION>
引数:最初の日付、最後の日付
戻り値:最初の日付から最後の日付まで1日ずつ足していったリスト
<USAGE>
コマンドライン上にて
python main.py <最初の日付> <最後の日付>
フォーマットはyymmdd形式

'''
from datelist import datelist  #最初と最後の日付(yymmdd形式)を引数に、その間の日付をリストとして返す

## __DATE LIST__________________________
dateBet=('151201','160301')  #最初の日付、最後の日付を入力
dateList=datelist(dateBet[0],dateBet[1])  #最初から最後の日付のリストを返す
print('\ndateList\n',dateList)
a=dateList
## __FILE BASE NAME__________________________
for datedir in a:
	import glob,os
	rawdataPath='C:\\home\\gnuplot\\SAout\\'+datedir+'\\rawdata\\trace'
	filename=glob.glob(rawdataPath+'\\*.txt')
	filebasename=[os.path.basename(r)[:-4] for r in filename]    #filebasenameを取得
	print('\nfilebasename\n',filebasename)



	# __FITTING__________________________
	for fitfile in filebasename:
		from fittingDiv36 import fitting
		freqWave=[22.2,23.4,24.0,24.25,24.8]   #帯域持った周波数
		freqWave+=[23.0,24.1,24.5,25.0,25.1,25.2,25.5]   #キャリアのみの周波数
		print('\nFitting Result\n',)
		fittingResult=fitting(rawdataPath,fitfile,freqWave)



		## __READ FROM CSV__________________________
		import CSV_IO as c
		csvfile='./SNn.csv'
		readed=c.readCSV(csvfile)

		import csv_dict_transfer as t
		dictdict=t.csvtodata(readed)    #csvからこれまでのフィッティング結果を読み込む
		dictdict.update(fittingResult)    #フィッティングの結果と併せる



		## __WRITE TO CSV__________________________
		dictList=t.datatocsv(dictdict)
		c.writeCSV(csvfile,freqWave,dictList)    #書き込み

