"""csv_dict_test ver0
<INTRODUCTION>
テストコード
csvから読み込み
ディクショナリ in ディクショナリ形式にして更新・ソート
<ACTION>
BLOCK1:各モジュールのインポートインポートする
BLOCK2:csvの読み込みとデータ変換
BLOCK3:データの追加
BLOCK4:データ変換をしてcsvデータに書き込み
<USAGE>
JUST BUILD
<UPDATE 0>
None
<MODIFY PLAN>
BLOCK3にフィッティングを行う機構を組み入れる
もしくはBLOCK3以外をフィッティングするモジュールに組み入れ？
datetime関数を使う
"""
## __BLOCK1__________________________
import CSVwriter as w
import CSVreader as r
import csv_dict_transfer as t

## __BLOCK2__________________________
filename='./SN.csv'
readed=r.readCSV(filename)    #読み込み
dictionary=t.csvtodata(readed)    #データ整理形式に変換

## __BLOCK3__________________________
# 追加データ
fit_result={	'20160302_000023':{'22.2kHz':4,'23.0kHz':5,'24.5kHz':6,'25kHz':8,'10kHz':900},
			'20160302_001022':{'22.2kHz':2,'23.0kHz':-1000,'24.5kHz':-1000,'25kHz':9,'27kHz':7855}}

x={'20151201_000023':{'22.2kHz':None,'23.0kHz':None,'24.5kHz':None,'25kHz':None,'10kHz':None}}
fit_result.update(x)

import datetime
d=datetime.datetime
y=d.strptime(date_time,'%Y%m%d_%H%M%S')
fit_result.update(y)

dictionary.update(fit_result)    # データの追加
freqWave=[22.2,23.4,24.0,24.25,24.8]   #帯域持った周波数
freqWave+=[23.0,24.1,24.5,25.0,25.1,25.2,25.5]   #キャリアのみの周波数
freqWave+=[10,27]

## __BLOCK4__________________________
dictList=t.datatocsv(dictionary)
w.csv_writer(filename,freqWave,dictList)    #書き込み
