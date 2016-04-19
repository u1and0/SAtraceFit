'''
csv_dict_transfer.py ver0


フィッティングしたデータをcsvファイルに書き込みたい
このときディクショナリ形式{key:val}の形で表現したとき
	keyはcsvの1列目(見出し)
	valは2列目以降(値)
を意味する。
このディクショナリ形式をn個の要素を持ったリストに収めていくと、n行のcsvが作成される(using CSVweiter.py)

____________________________
データ整理しやすい形式
{	'20151201_000011':{'22.2kHz':-87, '23.0kHz:-40', ...},
	'20151201_000512':{'22.2kHz':-80, '23.0kHz:None, ...},
	...}

			^
			|	csv_dict_transfer.py
			v

csvから読み書きしやすい形式
[	{DateTime:'20151201_000011', '22.2kHz':-87, '23.0kHz:-40',...},
	{DateTime:'20151201_000512', '22.2kHz':-80, '23.0kHz:None,...},
	...]



____________________________
データ形式について少し整理


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


____________________________
要するに、

(pythonのデータ整理用 ディクショナリ in ディクショナリ形式)
{
	{v00:{k1:v10,k2:v20,...,k(n-1):v(n-1,0),k(n):v(n,0)},
	{v01:{k1:v11,k2:v21},...,k(n-1):v(n-1,1),k(n):v(n,1)},
	...,
	{v0m:{k1:v(1,m),k2:v(2,m),...,k(n-1):v(n-1,m),k(n):v(n,m)}
}
	^
	||    <<ココの相互変換するモジュールを作りたい
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
	||    <<ココはpython組み込み関数でできる
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
'''


## ____________________________
# (pythonのデータ整理用 ディクショナリ in ディクショナリ形式)
# ==>(pythonのcsv読み書き用 ディクショナリ in リスト形式)変換
## ____________________________
data={'v00':{'k1':'v10','k2':'v20'},
		'v01':{'k1':'v11','k2':'v21'},
		'v02':{'k1':'v12','k2':'v22'},
		'v0m':{'kn-1':'vn-1m','kn':'vnm'}}
print('\ndata=',data)

# __data整理__________________________
dataSortedList= sorted(list(data.items()))
#items()メソッドを用いて日付(値)とデータ(ディクショナリ型)を1セットのタプルにする
#list()ファンクションを用いてdataのキー:値をリスト化する
#sorted()ファンクションを用いて必ず番号順で並ぶようにしてる
print('\ndataSortedList=',dataSortedList)



csv=[]
for i in range(len(data)):
	csv.append({})
	csv[i]['DateTime']=dataSortedList[i][0]
	csv[i].update(dataSortedList[i][1])
print('\ncsv=',csv)
# 実行結果
# csv= [{'DateTime': 'v00', 'k2': 'v20', 'k1': 'v10'}, {'DateTime': 'v01', 'k2': 'v21', 'k1': 'v11'}, {'DateTime': 'v02', 'k2': 'v22', 'k1': 'v12'}, {'DateTime': 'v0m', 'kn': 'vnm', 'kn-1': 'vn-1m'}]






## ____________________________
# (pythonのcsv読み書き用 ディクショナリ in リスト形式)変換
# ==>(pythonのデータ整理用 ディクショナリ in ディクショナリ形式)
## ____________________________
csvDateTime=[csv[i].pop('DateTime') for i in range(4)]
print('Deleted',csvDateTime)  #DateTimeがキーとなっている値を出力
print('Remained',csv)  # その他のキーをすべて出力

# for key in csvDateTime:
data=dict(zip(csvDateTime,csv))

print(data)









# # __Value Definition1__________________________
# # 3要素くらいでやってみます
# dataInnerDic=({	'd0Key1':'d0Val1'
# 			,'d0Key2':'d0Val2'
# 			,'d0Key3':'d0Val3'}
# 			,
# 			{'d1Key1':'d1Val1'
# 			,'d1Key2':'d1Val2'
# 			,'d1Key3':'d1Val3'}
# 			,
# 			{'d2Key1':'d2Val1'
# 			,'d2Key2':'d2Val2'
# 			,'d2Key3':'d2Val3'})
# # print('This is Innner Dictionary at dataOuterDic.\n',dataInnerDic)



# dataOuterDic={	'd0':dataInnerDic[0]
# 		,'d1':dataInnerDic[1]
# 		,'d2':dataInnerDic[2]}    #データ編集用ディクショナリ形式
# print('\nIN DATA\n',dataOuterDic)

# #必要ない
# # print('\nListing to dataOuterDic\'s keys\n' ,sorted(list(dataOuterDic.keys())))
# 	#keys()メソッドを用いてdataOuterDicのキーだけを抜き出す
# 	#list()ファンクションを用いてdataOuterDicのキーをリスト化する
# 	#sorted()ファンクションを用いて必ず番号順で並ぶようにしてる


# dataOuterDicTuple= sorted(list(dataOuterDic.items()))    #
# 	#items()メソッドを用いて日付(値)とデータ(ディクショナリ型)を1セットのタプルにする
# 	#list()ファンクションを用いてdataOuterDicのキーをリスト化する
# 	#sorted()ファンクションを用いて必ず番号順で並ぶようにしてる
# # print('\ndataOuterDicTuple is\n',dataOuterDicTuple)




# dic1={}
# dic1['DateTime']=dataOuterDicTuple[0][0]    #dic1の0要素目としてDateTimeをキーにして日付を値にする
# # print('\ndic1 is\n',dic1)



# dic1.update(dataInnerDic[0])
# print('\nOUT DATA\n',dic1)



# dictList=[{},{},{}]
# for i in range(3):
# 	pass
# dictList[0]['DateTime']=dataOuterDicTuple[0][0]
# dictList[0].update(dataInnerDic[0])
# dictList[1]['DateTime']=dataOuterDicTuple[1][0]
# dictList[1].update(dataInnerDic[1])
# dictList[2]['DateTime']=dataOuterDicTuple[2][0]
# dictList[2].update(dataInnerDic[2])
# print('\ndictList\n',dictList)



# print('\nI want to change from [d(n):{d(n)Key(m):d(n)Val(m) ,...}] to {DateTime:d(n),d(n)Key(m):d(n)Val(m) ,...} and its reverse style.')


















'''ゴミ '''
# dList=list(range(3))
# vList=[j for j in range(3)]
# for i in range(3) :
# 	for j in range(3) :
# 		dataInnerDic[i]=('d'+str(dList[i])+'Key'+str(vList[j]))



# ({	'd0Key1':'d0Val1'
# 			,'d0Key2':'d0Val2'
# 			,'d0Key3':'d0Val3'}
# 			,
# 			{'d1Key1':'d1Val1'
# 			,'d1Key2':'d1Val2'
# 			,'d1Key3':'d1Val3'}
# 			,
# 			{'d2Key1':'d2Val1'
# 			,'d2Key2':'d2Val2'
# 			,'d2Key3':'d2Val3'})
# print('This is Innner Dictionary at dataOuterDic.\n',dataInnerDic)



# dataOuterDic={	'd0':dataInnerDic[0]
# 		,'d1':dataInnerDic[1]
# 		,'d2':dataInnerDic[2]}    #データ編集用ディクショナリ形式
# print('\nEditing data use this style.\n',dataOuterDic)


# print('\nListing to dataOuterDic\'s keys\n' ,sorted(list(dataOuterDic.keys())))
# 	#keys()メソッドを用いてdataOuterDicのキーだけを抜き出す
# 	#list()ファンクションを用いてdataOuterDicのキーをリスト化する
# 	#sorted()ファンクションを用いて必ず番号順で並ぶようにしてる


# dataOuterDicTuple= sorted(list(dataOuterDic.items()))    #
# 	#items()メソッドを用いて日付(値)とデータ(ディクショナリ型)を1セットのタプルにする
# 	#list()ファンクションを用いてdataOuterDicのキーをリスト化する
# 	#sorted()ファンクションを用いて必ず番号順で並ぶようにしてる
# print('\ndataOuterDicTuple is\n',dataOuterDicTuple)




# dic1={}
# dic1['DateTime']=dataOuterDicTuple[0][0]    #dic1の0要素目としてDateTimeをキーにして日付を値にする
# print('\ndic1 is\n',dic1)



# dic1.update(dataInnerDic[0])
# print('\nAppended dic1 is\n',dic1)
# print('Then I want to this style {DateTime:d(n),d(n)Key(m):dnVal(m),...}')
