'''
## CSV_IO.py ver1.0
__INTRODUCTION__
関数editCSVが関数readCSV,writeCSVを呼び出す。
組み込み関数csv, os.path, datetime.datetimeを使用して、csvにためてある結果を追加する。
各関数の説明は各関数のdocを参照。
'''

import csv
import os.path
from datetime import datetime


def readCSV(filename):
    '''
    ## readCSV.py ver1.1.1

    __UPDATE1.1.1__
    print文コメントアウト

    __UPDATE1.1__
    クラス'csv.DictReader()'を使ってディクショナリ形式でcsvを取り出す。
    キーは見出し(csvの1行目)
    行を読むたびリスト'dictList'へ追加する
    dictListを返す

    __INTRODUCTION__
    csvファイルの中身をディクショナリに入れるpy
    引数：ファイル名
    戻り値：ディクショナリ`dictList`

    __ACTION__
    filenameにいれた名前のファイルを開く
    リスト'reader'に格納する
    リスト'reader'に対して0要素目をキーに、1要素目以降(リスト形式)を値にしたディクショナリ`dictList`を作成する
    '''
    if not os.path.isfile(filename):  # ファイルが存在しなければ
        open(filename, "w").write("")  # 空のファイルを作成する
    infile = open(filename, 'r')
    reader = csv.DictReader(infile)
    dictList = []
    for rows in reader:  # 列のラベルにoutparamを追加
        rows['DateTime'] = datetime.strptime(
            rows['DateTime'], '%Y-%m-%d %H:%M:%S')  # キーがDateTimeの値を文字列から時間に変換
        dictList.append(rows)
    # print('\nRead from',filename)
    # print('\nRead from',filename,'\n',dictList)
    return dictList


def writeCSV(outpath, outparam, dictList):  # ファイル名、csvの見出し行、ディクショナリ in リスト形式
    '''
    ## writeCSV.py ver1.4

    __UPDATE1.4__
    ソートコメントアウト

    __UPDATE1.3.1__
    print文コメントアウト

    __UPDATE1.3__
    周波数の指定は外部ファイルから渡されてくる周波数のリスト'outparam'
    計算結果は外部ファイルから渡されてくる計算結果のリスト'cal_result'

    __INTRODUCTION__
    辞書の内容ををcsvファイルを書き込む

    __ACTION__
    引数として集合'outparam',辞書'cal_result'を渡す
    戻り値なし
    csvを返す
    日付時間のキーは行のラベルにあたる
    周波数のキーは列のラベルにあたる

    __USAGE__
    列のラベル'paramnames'を定義する
    {日付時間,周波数1,周波数2,...}がディクショナリになった'fit_result'を定義する
    csv_writer(引数1,引数2)を実行する

    __PLAN__
    '''

    # outparam.sort()   #outparamを小さい順にソート
    outparam = list(map(lambda n: str(n) + 'kHz', outparam))  # freqWave各要素に文字列'kHz'追加
    paramnames = ['DateTime'] + outparam  # 列のラベルにoutparamを追加
    header = dict([(val, val) for val in paramnames])
    if not os.path.isfile(outpath):  # ファイルが存在しなければ
        open(outpath, "w").write("")  # 空のファイルを作成する
    with open(outpath, mode='w') as f:
        dictList.insert(0, header)
        writer = csv.DictWriter(f, paramnames, extrasaction='ignore', lineterminator='\n')
        writer.writerows(dictList)
        # print('\nWriteing',outpath,'done!\n')


def editCSV(readcsv, writecsv, appendDict, freqWave):
    '''
    ## editCSV ver1.0
    __INTRODUCTION__
    fitting>read>translate>update>translate>writeの流れを一まとめにした
    __ACTION__
    READ FROM CSV
    >CSVファイルを読み込む

    UPDATE DICTIONARY
    >読み込んだcsvとappenddictを併せる
    >>dictionary形式は同一キーが存在した場合、後から来たdictionary内のキーの値に更新する

    WRITE TO CSV
    >更新したdictionaryをcsvに書き込む

    __USAGE__
    引数:

    + readcsv:読み込みcsvファイル名
    + writecsv:書き込みcsvファイル名
    + appendDict:書き込む内容。fittingの結果
    + freqWave:csvの1行目(見出し行)

    戻り値:None(writecsvに書き込み)
    __UPDATE__
    first commit
    __PLAN__
    None
    '''
# __READ FROM CSV__________________________
    readed = readCSV(readcsv)

    import csv_dict_transfer as t
    dictdict = t.csvtodata(readed)  # csvからこれまでのフィッティング結果を読み込む

# __UPDATE DICTIONARY__________________________
    # print('\nAppend dictionary in dictionary\n',appendDict)
    dictdict.update(appendDict)  # mainモジュール内で計算したフィッティングの結果と併せる

# __WRITE TO CSV__________________________
    writing = t.datatocsv(dictdict)
    writeCSV(writecsv, freqWave, writing)  # 書き込み


if __name__ == '__main__':
    dir='./test/'
    rc='P2016_04.csv'
    wc='P2016_0test.csv'
    fl=['22.2kHz', '23.4kHz', '24.0kHz', '24.5kHz', '24.8kHz', '25.2kHz', '23.0kHz', '24.1kHz', '25.0kHz', '25.1kHz', '25.5kHz']
    editCSV(rc, wc, {'DateTime':'hoge', '22.2kHz': 'hogehoge'}, fl)
