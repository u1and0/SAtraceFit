'''
## globname.py ver1.0

__UPDATE1.0__
first commit

__USAGE__
mainから呼び出す
引数:
    rootpath:
    dateFirst:最初の日付yymmdd文字列が入ったリスト形式形式
    dateLast:最後の日付yymmdd文字列が入ったリスト形式形式
戻り値:
    filebesename:リスト形式


__INTRODUCTION__
rootroot()下のファイルのフルパスを返す。
ただし、最初と最後の日付をもらって、その間にある日付のファイルに限る

__ACTION__
datetime関数で日付の形式に直して
globの

__PLAN__
時間を引数にする
'''
import glob


def globname(rootpath, dateList):
    '''rootpath内のファイルのフルパスを返す
    ただし、ファイル名が日付dateListの中による'''
    filename = []
    for i in dateList:
        filename += glob.glob(rootpath + '20' + i + '*.txt')  # 上で指定したディレクトリから.txt形式のデータをglob
    return filename


'''
TEST globname()
指定した日付の間のファイルを取り出す

parameter.param()['in']というディレクトリからglob
ディレクトリ内には"ファイルベースネーム=タイムスタンプ"のファイルが詰まっている
import datelist as dl
import parameter
path=parameter.param()['in']
for d in dl.date_range_input():
    for i in d:
        for g in glob.iglob(path+i+'*'):
            print(g)
'''
