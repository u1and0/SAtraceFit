'''
readCSV.py ver1.0
filenameにいれた名前のファイルを開く
リスト'reader'に格納する
リスト'reader'に対して0要素目をキーに、1要素目以降(リスト形式)を値にしたディクショナリ'mydict'を作成する
引数：ファイル名
戻り値：ディクショナリ'mydict
'''
import csv
# filename='./SN.csv'
def readCSV(filename):
	with open(filename, mode='r') as infile:
		reader = csv.reader(infile)
		mydict={rows[0]:[rows[1:]] for rows in reader}
	return mydict

## __TEST__________________________
print(readCSV('./SN.csv'))
## __RUN RESURT__________________________
# {'20151201_000524': [['3', '7', '', '', '', '', '9', '', '', '', '', '']], 'date_time': [['22.2kHz', '23.0kHz', '23.4kHz', '24.0kHz', '24.1kHz', '24.25kHz', '24.5kHz', '24.8kHz', '25.0kHz', '25.1kHz', '25.2kHz', '25.5kHz']], '20151201_000023': [['4', '5', '', '', '', '', '6', '', '', '', '', '']], '20151201_001022': [['2', '', '', '', '', '', '', '', '', '', '', '']]}
