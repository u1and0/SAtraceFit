'''
csv_writer.py ver1.0
<何してくれるか>
辞書の内容をoutpathで定義したcsvファイルに書き込む
<動作>
列のラベル'paramnames'を定義する
{日付時間,周波数1,周波数2,...}がセットになった'fit_result'を定義する
日付時間のキーは行のラベルにあたる
周波数のキーは列のラベルにあたる
<USAGE>
buildするだけ
<UPDATE1.0>
初
'''
import csv
outpath = './SN.csv'

paramnames = ('date_time','22.2kHz','23.0kHz','24.5kHz')
fit_result = [{'date_time':'20151201_000023','22.2kHz':4,'23.0kHz':5,'24.5kHz':6,'25kHz':8}
,{'date_time':'20151201_000524','22.2kHz':3,'23.0kHz':7,'24.5kHz':9,'25kHz':9}   	#25kHzはリストに入ってないからcsvに書き込まれない
,{'date_time':'20151201_001022','22.2kHz':2,'23.0kHz':None,'24.5kHz':'None','25kHz':9}]   #Noneは空白、'None'はNoneとして書き込まれる

header = dict([(val,val)for val in paramnames])
with open(outpath, mode='w') as f:
	fit_result.insert(0,header)
	writer = csv.DictWriter(f, paramnames, extrasaction='ignore',lineterminator='\n')
	writer.writerows(fit_result)
