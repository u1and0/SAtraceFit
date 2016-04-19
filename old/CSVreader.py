'''
readCSV.py ver1.1
<INTRODUCTION>
csvファイルの中身をディクショナリに入れるpy
引数：ファイル名
戻り値：ディクショナリ'mydict
<ACTION>
filenameにいれた名前のファイルを開く
リスト'reader'に格納する
リスト'reader'に対して0要素目をキーに、1要素目以降(リスト形式)を値にしたディクショナリ'mydict'を作成する
<UPDATE1.1>
クラス'csv.DictReader()'を使ってディクショナリ形式でcsvを取り出す。
キーは見出し(csvの1行目)
行を読むたびリスト'dictList'へ追加する
dictListを返す
'''
import csv
# filename='./SN.csv'
def readCSV(filename):
	infile=open(filename, 'r')
	reader = csv.DictReader(infile)
	dictList=[]
	for rows in reader:   #列のラベルにoutparamを追加
		dictList.append(rows)
	print('Read from',filename,'\n',dictList)
	return dictList


## __TEST__________________________
# filename='./SN.csv'
# readCSV(filename)
## __RESULT__________________________
## [{'22.2kHz': '4', '24.5kHz': '6', '24.1kHz': '', '24.25kHz': '', '25.0kHz': '', '23.0kHz': '5', '25.5kHz': '', '23.4kHz': '', '25.1kHz': '', 'date_time': '20151201_000023', '24.0kHz': '', '25.2kHz': '', '24.8kHz': ''}, {'22.2kHz': '3', '24.5kHz': '9', '24.1kHz': '', '24.25kHz': '', '25.0kHz': '', '23.0kHz': '7', '25.5kHz': '', '23.4kHz': '', '25.1kHz': '', 'date_time': '20151201_000524', '24.0kHz': '', '25.2kHz': '', '24.8kHz': ''}, {'22.2kHz': '2', '24.5kHz': '', '24.1kHz': '', '24.25kHz': '', '25.0kHz': '', '23.0kHz': '', '25.5kHz': '', '23.4kHz': '', '25.1kHz': '', 'date_time': '20151201_001022', '24.0kHz': '', '25.2kHz': '', '24.8kHz': ''}]
