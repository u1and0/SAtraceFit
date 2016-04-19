'''
csv_writer.py ver1.1
<What do you do?>
辞書の内容ををcsvファイルを書き込む
<BEHAVIOR>
列のラベル'paramnames'を定義する
{日付時間,周波数1,周波数2,...}がセットになった'fit_result'を定義する
日付時間のキーは行のラベルにあたる
周波数のキーは列のラベルにあたる
<USAGE>
freqをこのファイル内で定義する
引数としてfit_resultを渡す
<UPDATE1.1>
関数として独立させた
'''
import csv
outpath = './SN.csv'

'''テスト変数
freq=('date_time','22.2kHz','23.0kHz','24.5kHz')
fit_result=[{'date_time':'20151201_000023','22.2kHz':4,'23.0kHz':5,'24.5kHz':6,'25kHz':8}
,{'date_time':'20151201_000524','22.2kHz':3,'23.0kHz':7,'24.5kHz':9,'25kHz':9}   	#25kHzはリストに入ってないからcsvに書き込まれない
,{'date_time':'20151201_001022','22.2kHz':2,'23.0kHz':None,'24.5kHz':'None','25kHz':9}]   #Noneは空白、'None'はNoneとして書き込まれる
'''

def csv_writer(paramnames,ddict):
	header = dict([(val,val)for val in paramnames])
	with open(outpath, mode='w') as f:
		ddict.insert(0,header)
		writer = csv.DictWriter(f, paramnames, extrasaction='ignore',lineterminator='\n')
		writer.writerows(ddict)

'''テスト実行
csv_writer(freq,fit_result)
