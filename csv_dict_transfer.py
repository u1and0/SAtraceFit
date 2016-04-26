'''
## csv_dict_transfer.py ver1.0

__UPDATE1.0__
first commit

__INTRODUCTION__
関数datatocsv, csvtodataから構成される。

+ datetocsv : dataをcsvファイルに読み書きしやすい、ディクショナリ in リスト形式に変換する
+ csvtodata : csvの内容をデータ整理用の、ディクショナリ in ディクショナリ形式に変換する
> ディクショナリはキーが重複した場合、値を更新する機能、キーでソートする機能をもつ




__ACTION__
フィッティングしたデータをcsvファイルに読み込み(書き込み)たい。

**CSVの表形式**

|DateTime 	|22.2kHz 	|23.0kHz 	|...	|
| ---- | ----------------- | -------------------| -------------------|
|20151201_000011|-87 		|-40 		|...	|
|20151201_000512|-80 		|-40 		|...	|




pythonの組み込み関数csvを用いれば、以下のような形式で取り込まれる。
これを **ディクショナリ in リスト形式** と呼ぶ。

**ディクショナリ in リスト形式**
```python
[	{DateTime:'20151201_000011', '22.2kHz':-87, '23.0kHz:-40',...},
	{DateTime:'20151201_000512', '22.2kHz':-80, '23.0kHz:None,...},
		...]
```





____________________________
一方で、フィッティングの値はフィッティングを担当するモジュール`fittingDiv`から以下のような形式で渡される。
この形式を **ディクショナリ in ディクショナリ形式** と表現する。


**ディクショナリ in ディクショナリ形式**
```python
{	'20151201_000011':{'22.2kHz':-87, '23.0kHz:-40', ...},
	'20151201_000512':{'22.2kHz':-80, '23.0kHz:None, ...},
	...}
```






____________________________
pythonに取り込まれたcsvとフィッティングで得られる値を混ぜ合わせて、python内部でディクショナリ in ディクショナリ形式として集計することで、 **日付時刻の重複データの更新が容易になる。**

そこで、csvから読み込んだディクショナリ in リスト形式とデータ整理用のディクショナリ in ディクショナリ形式の相互変換ができるモジュールが欲しい。

```python
(csvから読み書きしやすい形式)
[	{DateTime:'20151201_000011', '22.2kHz':-87, '23.0kHz:-40',...},
	{DateTime:'20151201_000512', '22.2kHz':-80, '23.0kHz:None,...},
	...]

			^
			|	相互変換できるモジュールが必要
			v

(データ整理しやすい形式)
{	'20151201_000011':{'22.2kHz':-87, '23.0kHz:-40', ...},
	'20151201_000512':{'22.2kHz':-80, '23.0kHz:None, ...},
	...}
```





____________________________
取り扱うデータ形式を一般化して考える。

+ 'k'はcsvの1列目(見出し)
+ 'v'は2列目以降(値)

を意味する。
ディクショナリ in リスト形式がn個の要素を持ったリストに収めていくと、n行のcsvが作成される。
**要するに何を作るべきかというと、ディクショナリ in ディクショナリ形式とディクショナリ in リスト形式の相互変換モジュール**


____________________________


**変換されたCSVの表形式**

|k0|k1|k2 |... |k(n)|
| ---- | ----------------- | -------------------|  
|v00|v10|v20 |... |v(n,0)|
|v01|v11|v21 |... |v(n,1)|
|v02|v12|v22 |... |v(n,2)|
.
.
|v(0,m-1)|v(1,m-1)|v(2,m-1)|...v(n,m-1)|
|v(0,m)|v(1,m)|v(2,m)|...v(n,m)|

		^
		|    <<ココはpython組み込み関数でできる
		v

```python
# csv読み書き用 ディクショナリ in リスト形式
[
	{k0:v00,k1:v10,k2:v20,...,k(n-1):v(n-1,0),k(n):v(n,0)},
	{k0:v01,k1:v11,k2:v21},...,k(n-1):v(n-1,1),k(n):v(n,1)},
	{k0:v02,k1:v12,k2:v22},... 									},
	...,
	{k0:v(0,m-1),k1:v(1,m-1),k2:v(2,m-1),...,k(n-1):v(n-1,m-1)),k(n):v(n,m-1))},
	{k0:v(0,m),k1:v(1,m),k2:v(2,m),...,k(n-1):v(n-1,m),k(n):v(n,m)}
]

```

		^
		|    <<ココの相互変換するモジュールを作りたい
		v

```python
# データ整理用 ディクショナリ in ディクショナリ形式
{
	{v00:{k1:v10,k2:v20,...,k(n-1):v(n-1,0),k(n):v(n,0)},
	{v01:{k1:v11,k2:v21},...,k(n-1):v(n-1,1),k(n):v(n,1)},
	...,
	{v0m:{k1:v(1,m),k2:v(2,m),...,k(n-1):v(n-1,m),k(n):v(n,m)}
}
```



__USAGE__
CSV_IO.pyから呼び出される
各関数のdoc参照
Testはコメントアウト外してbuildするのみ

'''





from datetime import datetime




def datatocsv(data):
	'''
	### datatocsv ver1.0
	__UPDATE1.0__
	first commit

	__INTRODUCTION__
	data(ディクショナリ in ディクショナリ形式)をcsvファイルに読み書きしやすい、ディクショナリ in リスト形式に変換する

	__ACTION__

	0. 引数dataは{'日付':{周波数1:パワー1,周波数2:パワー2,...,周波数n:パワーn,}}で渡されてくる
	1. 引数dataを2要素のリストにしてdataSortedListに代入する。`dataSortedList= sorted(list(data.items()))`
	> items()メソッドを用いて日付(値)とデータ(ディクショナリ型)を1セットのタプルにする
	> list()ファンクションを用いてタプル形式をリスト形式にする。(sorted関数を使いたいため。)
	> sorted()ファンクションを用いて文字列(日付)→ディクショナリの順番で並ぶようにしてる
	2. 空のリストcsvを作成
	3. ここから引数dataの数だけ繰り返す`for i in range(len(data))`
		3. リストcsvをディクショナリ in リスト形式にする`csv.append({})`
		3. csvというディクショナリ in リスト形式のi番目の要素に対して、「DateTime」をキーに、dataSortedListの0番目の要素=「日付」を値として追加する。`csv[i]['DateTime']=dataSortedList[i][0] `
	> ソートされたので0番目の要素は文字列
		3. csvというディクショナリ in リスト形式のi番目の要素に対して、「ディクショナリ(周波数をキーにしたシグナル強度)」を追加する。`csv[i].update(dataSortedList[i][1])`
	>ソートされたので1番目の要素はディクショナリ(周波数をキーにしたシグナル強度)。
	4. リスト in ディクショナリcsvを返して終了


	__USAGE__
	引数:pythonのデータ整理用 ディクショナリ in ディクショナリ形式
	戻り値:pythonのcsv読み書き用 ディクショナリ in リスト形式

	__PLAN__
	none
	'''
	dataSortedList= sorted(list(data.items()))
	##items()メソッドを用いて日付(値)とデータ(ディクショナリ型)を1セットのタプルにする
	##list()ファンクションを用いてdataのキー:値をリスト化する
	##sorted()ファンクションを用いて文字列(日付)→ディクショナリの順番で並ぶようにしてる
	csv=[]
	for i in range(len(data)):
		csv.append({})
		csv[i]['DateTime']=dataSortedList[i][0]  #タプルの要素0は必ず日付
		csv[i].update(dataSortedList[i][1])  #タプルの要素1は周波数とパワー
	# print('\nData to CSV\n',csv)
	return csv


def csvtodata(csv):
	'''
	### csvtodata ver1.0

	__UPDATE1.0__
	first commit

	__INTRODUCTION__
	csvの内容をデータ整理用の、ディクショナリ in ディクショナリ形式返す

	__ACTION__

	0. 引数はリスト in ディクショナリ形式で入ってくる
	1. キーがDateTimeである値=日付　をcsvの行数文だけ`for i in range(len(csv))`抽出`pop`し、リストcsvDateTimeに代入していく
	2. 項目1で抽出した値(日付)と抽出する前野引数の残りをタプルにまとめ`zip`、ディクショナリ形式にする`dict`

	__USAGE__
	引数:pythonのcsv読み書き用 ディクショナリ in リスト形式
	戻り値:pythonのデータ整理用 ディクショナリ in ディクショナリ形式

	__PLAN__
	none
	'''
	csvDateTime=[csv[i].pop('DateTime') for i in range(len(csv))]
		# popによりDateTimeがキーとなっている要素をcsvDateTimeへ抽出・csvから削除
		# 内包表記でリスト化する
	# print('Deleted',csvDateTime)
	# print('Remained',csv)  # その他のキーをすべて出力
	data=dict(zip(csvDateTime,csv))
		# zipによってcsvDateTimeとcsvに残ったものを組にする
		# dictでタプルをディクショナリにする
	# print('\nCSV to Data\n',data)
	return data






# # Test
# from datetime import datetime
# d=datetime

# data={d(2015, 12, 12, 12, 12, 12).strftime('%Y/%m/%d %H:%M:%S'):{'k1':'v10','k2':'v20'},
# 		d(2015, 12, 12, 12, 12, 13).strftime('%Y/%m/%d %H:%M:%S'):{'k1':'v11','k2':'v21'},
# 		d(2015, 12, 12, 12, 12, 14).strftime('%Y/%m/%d %H:%M:%S'):{'k1':'v12','k2':'v22'},
# 		d(2015, 12, 12, 12, 12, 15).strftime('%Y/%m/%d %H:%M:%S'):{'kn-1':'vn-1m','kn':'vnm'}}
# print('\ndata=',data)
# print('\ndata to csv=',datatocsv(data))

# # Test result がTrueならば、dataがcsvに変換されて逆変換されてそのまま戻ってきたということ
# print('\nBefore==After?:',csvtodata(datatocsv(data)) == data)
