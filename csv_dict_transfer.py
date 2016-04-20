'''
## csv_dict_transfer.py ver1.0

__UPDATE1.0__
first commit

__INTRODUCTION__
関数datatocsv, csvtodataから構成される。

+ datetocsv : dataをcsvファイルに読み書きしやすい、ディクショナリ in リスト形式に変換する
+ csvtodata : csvの内容をデータ整理用の、ディクショナリ in ディクショナリ形式
> ディクショナリはキーが重複した場合、値を更新する機能、キーでソートする機能をもつ




__ACTION__
フィッティングしたデータをcsvファイルに書き込みたい
このときディクショナリ形式{key:val}の形で表現したとき

+ keyはcsvの1列目(見出し)
+ valは2列目以降(値)

を意味する。
このディクショナリ形式をn個の要素を持ったリストに収めていくと、n行のcsvが作成される(using CSVweiter.py)

____________________________

```
(データ整理しやすい形式)
{	'20151201_000011':{'22.2kHz':-87, '23.0kHz:-40', ...},
	'20151201_000512':{'22.2kHz':-80, '23.0kHz:None, ...},
	...}


			^
			|	csv_dict_transfer.py
			v


(csvから読み書きしやすい形式)
[	{DateTime:'20151201_000011', '22.2kHz':-87, '23.0kHz:-40',...},
	{DateTime:'20151201_000512', '22.2kHz':-80, '23.0kHz:None,...},
	...]
```


____________________________
データ形式について少し整理


```

(データ整理しやすい形式)
外側ディクショナリの形式
	{ディクショナリ1,ディクショナリ2,...}
		つまり
	{'d0':dataInnerDic[0] ,'d1':dataInnerDic[1] ,'d2':dataInnerDic[2],...}
内側ディクショナリの形式
	ディクショナリ1='20151201_000011':{'22.2kHz':-87, '23.0kHz:-40', ...}
		つまり
	dataInnnerDic[0]={'d0Key1':'d0Val1','d0Key2':'d0Val2',...}


(csvから読み書きしやすい形式)
外側ディクショナリの形式
	[ディクショナリ1,ディクショナリ2,...]
		つまり
	[dic1,dic2,...]
内側ディクショナリの形式
	{DateTime:'20151201_000011', '22.2kHz':-87, '23.0kHz:-40',...},
		つまり
	{DateTime:'20151201_000011', '22.2kHz':-87, '23.0kHz:-40',...},
```


____________________________
要するに、

```
(pythonのデータ整理用 ディクショナリ in ディクショナリ形式)
{
	{v00:{k1:v10,k2:v20,...,k(n-1):v(n-1,0),k(n):v(n,0)},
	{v01:{k1:v11,k2:v21},...,k(n-1):v(n-1,1),k(n):v(n,1)},
	...,
	{v0m:{k1:v(1,m),k2:v(2,m),...,k(n-1):v(n-1,m),k(n):v(n,m)}
}

		^
		|    <<ココの相互変換するモジュールを作りたい
		v
(pythonのcsv読み書き用 ディクショナリ in リスト形式)
[
	{k0:v00,k1:v10,k2:v20,...,k(n-1):v(n-1,0),k(n):v(n,0)},
	{k0:v01,k1:v11,k2:v21},...,k(n-1):v(n-1,1),k(n):v(n,1)},
	{k0:v02,k1:v12,k2:v22},... 									},
	...,
	{k0:v(0,m-1),k1:v(1,m-1),k2:v(2,m-1),...,k(n-1):v(n-1,m-1)),k(n):v(n,m-1))},
	{k0:v(0,m),k1:v(1,m),k2:v(2,m),...,k(n-1):v(n-1,m),k(n):v(n,m)}
]

		^
		|    <<ココはpython組み込み関数でできる
		v

(CSVファイル)
k0,k1,k2 ,... ,k(n)
v00,v10,v20 ,... ,v(n,0)
v01,v11,v21 ,... ,v(n,1)
v02,v12,v22 ,... ,v(n,2)
.
.
v(0,m-1),v(1,m-1),v(2,m-1),...v(n,m-1)
v(0,m),v(1,m),v(2,m),...v(n,m)
```





__USAGE__
各関数のdoc参照
Testはコメントアウト外してbuildするのみ
'''





from datetime import datetime




def datatocsv(data):
	'''
	## datatocsv ver1.0
	__UPDATE1.0__
	first commit

	__INTRODUCTION__
	data(ディクショナリ in ディクショナリ形式)をcsvファイルに読み書きしやすい、ディクショナリ in リスト形式に変換する

	__ACTION__
	1. 引数dataのキー=日付　の小さい順にソートする
	> 関数sorted()はタプルで値を返す
	>> 「文字列」とはこの場合、この場合、日付を文字列化したもの(datetime.strptime(ファイル名))
	2. リストcsvを作成
	3. ここから引数dataの数だけ繰り返す(for i in range(len(data)))
	3.1. リストcsvをディクショナリ in リスト形式にする(appendメソッド)
	3.2. csvというディクショナリ in リスト形式のi番目の要素に対して、「DateTime」をキーに、「日付」を値として追加する。
	> sorted関数でソートされるとタプルが返され、必ず文字列(datetime.strptime(ファイル名))の次にディクショナリ(周波数をキーにしたシグナル強度)の順番になる。故にdataSortedListの0番目の要素は必ず日付。
	3.3. csvというディクショナリ in リスト形式のi番目の要素に対して、「ディクショナリ(周波数をキーにしたシグナル強度)」を追加する。(updateメソッド)
	4. csvを返して終了

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
	csvの内容をデータ整理用の、ディクショナリ in ディクショナリ形式返す
	引数:pythonのcsv読み書き用 ディクショナリ in リスト形式
	戻り値:pythonのデータ整理用 ディクショナリ in ディクショナリ形式
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
