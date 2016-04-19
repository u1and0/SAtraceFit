'''dataglob.py ver0.2
ファイルパスを入れて
その中にあるすべてのテキストファイル名(hoegehoge.txt)をリストとして返すpy

1. glob関数の指定
2. rawdata_directoryでディレクトリの指定
3.
'''
import glob

## __DEFINITION__________________________
def dataglob(directory):
	dataname=glob.glob(directory+'\\*.txt')   #上で指定したディレクトリから.txt形式のデータをglob
	return dataname


## __TEST__________________________
# rawdata_directory=('C:\\home\\gnuplot\\SAout\\151201\\rawdata\\trace')   #データの入ったディレクトリ
# print(dataglob(rawdata_directory))
# print('First of list',dataglob(rawdata_directory)[1])
# print('Last 3 of list',dataglob(rawdata_directory)[285:])
