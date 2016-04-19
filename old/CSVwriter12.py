'''
csv_writer.py ver1.2
<INTRODUCTION>
辞書の内容ををcsvファイルを書き込む
<OPERATION>
引数としてoutparam,cal_resultを渡す
戻り値なし
csvを返す
日付時間のキーは行のラベルにあたる
周波数のキーは列のラベルにあたる
<USAGE>
列のラベル'paramnames'を定義する
{日付時間,周波数1,周波数2,...}がセットになった'fit_result'を定義する
csv_writer(引数1,引数2)を実行する
<UPDATE1.2>
周波数の指定は外部ファイルから渡されてくる周波数のリスト'outparam'
計算結果は外部ファイルから渡されてくる計算結果のリスト'cal_result'
'''
import csv
outpath = './SN.csv'

def plus(n):
	return str(n)+'kHz'


##テスト変数
# freqWave=[22.2,23.4,24.0,24.25,24.8]   #帯域持った周波数
# freqWave+=[23.0,24.1,24.5,25.0,25.1,25.2,25.5]   #キャリアのみの周波数

# fit_result=[{'date_time':'20151201_000023','22.2kHz':4,'23.0kHz':5,'24.5kHz':6,'25kHz':8}
# ,{'date_time':'20151201_000524','22.2kHz':3,'23.0kHz':7,'24.5kHz':9,'25kHz':9}   	#25kHzはリストに入ってないからcsvに書き込まれない
# ,{'date_time':'20151201_001022','22.2kHz':2,'23.0kHz':None,'24.5kHz':None,'25kHz':9}]   #Noneは空白、'None'はNoneとして書き込まれる
############



def csv_writer(outparam,cal_result):
	outparam.sort()   #outparamを小さい順にソート
	outparam=list(map(plus,outparam))   #freqWave各要素に文字列'kHz'追加
	paramnames=['date_time']+outparam   #列のラベルにoutparamを追加
	header = dict([(val,val)for val in paramnames])
	with open(outpath, mode='w') as f:
		cal_result.insert(0,header)
		writer = csv.DictWriter(f, paramnames, extrasaction='ignore',lineterminator='\n')
		writer.writerows(cal_result)

##テスト実行
# csv_writer(freqWave,fit_result)
########