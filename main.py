'''
## main.py v7.2.0

__USAGE__

* コマンドライン上で`python main.py`で実行
    * parameter.jsonでfittingする周波数を指定すること
        * パラメータ名はfreqWave, freqCarrier, freqM
        * JSONファイルは後の行にあるものが使用される
    * 必要最低限の周波数でfitするとき
        * 日付をアンダーバーで区切って入力
        * (例)20160101_20160108
    * 全周波数でfitするとき
        * 区別するためにファイル名の頭に"fitall"という名前をつけた。
        * (例)fitall20160101_20160108
        * このときプロットするオプションはオフにする
        > プロットしますか?[y/n?]>>nと入力する

* 表示画面の説明
    * 1行目 区切り
    * 2行目 メッセージ
    * 3行目 日付
    * 4行目 期間の進捗
        > 上の例で言うなら2016年1月1日から2016年1月8日までの何割がfit終わったか
    * 5行目 一日あたりの進捗
        > 最大288ファイル中、何割終わったか
    * 6行目
        > fitする周波数の何割が終わっているのか

```
1 ___________________________________
2 次の年月日のファイルをfittingします。
3 20160816
4 19%|████████████                                                  | 6/31 [12:17<54:17, 130.28s/it]
5 ██████████████████████████████████████████████████████| 287/287 [02:30<00:00,  4.05it/s] 100%|
6 █████████████████████████████████████████████████████████| 6/6 [00:00<00:00, 149.98it/s]
# ↑計算完了


# ↓計算中
1 ___________________________________
2 次の年月日のファイルをfittingします。
3 20160817
4  2%|█▎                                                      | 7/287 [00:06<02:51,  1.63it/s] 100%|
5 █████████████████████████████████████████████████████████| 6/6 [00:0
```


__INTRODUCTION__
SAtraceFitの実行ファイル

1. データソースからのテキストにフィッティングをかけて
2. 結果をcsvに書き込み
3. フィッティング結果を反映したスペクトラム図のpngを吐き出す
    * csvファイル名はユーザーの入力
    * csvファイル出力先はmain.pyに書き込まれている
    * pngファイル出力先はfitting.plotshowing()に書き込まれている。

__ACTION__

<実行したときの、コマンドラインの表示の流れ>

1. データファイル、出力ファイルのディレクトリ指定→parameter.pyで指定
2. SNを書き込むcsvファイル名を聞かれる→入力する
3. powerを書き込むcsvファイル名を聞かれる→入力する
4. csvのフルパス表示
5. 日付を指定(指定方法がメッセージで表示される。詳しくはdatelist.date_range_input()参照)
    6. fitting.fitting()実行。詳しくはfitting.fitting()参照
    7. フィッティング日時表示
    8. フィッティング結果表示(5の日付指定が最後に来るまで繰り返し)

__UPDATE7.3.0__
| * e191401 (HEAD -> release/v7.2.0) fitting call as fitting (not as f)
| * 28561c7 @main.py : input message modify
| * 40c27aa PEP8 CSV_IO.py csv_dict_transfer.py globname.py
| * 367eefb fitting.py comment
| * 7d415f2 fitting.py: PEP8 modify, listdic.py: around function using func argument
| * f23663f remove logprint, use tab-->space
| * 2206988 fitting.py chuncked
| * f11a989 readme
|/
* e0b5e2d readme
* e564bf7 main v7.2.0
* 18b69ba csv out each
* 0ab16fc 逐一書き込む方式at for state
*   6e3361a Merge remote-tracking branch 'origin/develop' into develop
|\
| * 6759545 datelist.date_range_input() shorter modify
* | e37dead import tqdm
|/
* 5e0c61d out_csv, put_png directory added, fitting README modity
*   238246d Merge branch 'feature/allrange' into develop
|\
| * 2598004 unused 'outPath', freqM label commentouted
| * c47aad0 plot close, get method
| * 126d119 ラベル条件変更 type not float==> type ==tuple
| * 763cd66 return integer
| * 6c4d975 pep8 at globname
| * cdc2633 input方式plot
__UPDATE7.2.0__
* 逐一読み込む方式再度廃止(コメントアウトで残してある)
* 1ヵ月ごとに読み込むのがやはり遅い
* csvに保存するまでがこいつの仕事
* データフレームとして複数のcsvを読み込み、1つのcsvにまとめる(pandas.concat)
    * してから保存する(pandas.DataFrame.to_csv())ことでcsvにするのが
    * SAtraceView save_table.concat_table()の仕事


__UPDATE7.1.0__
データの引継ぎ機能復活
old, newのファイル名を入力する
ファイル名の頭につける文字列は
    'SN': SN比
    'P': power

__UPDATE7.1.0__
データの引継ぎ機能復活
old, newのファイル名を入力する
ファイル名の頭につける文字列は
    'SN': SN比
    'P': power

__UPDATE7.0.0__
ファイル名は日時指定で引っ張ってくる

__UPDATE6.1.1__
fot Mfit test

__UPDATE6.1__
fittting の引数に周波数は入れない(fittingのforステートメント中にparameterから直接引っ張る)

__UPDATE6.0__
例外により中断されたら実行するtry~finally文追加


__UPDATE5.0__
ファイル名の指定(コンソールからインプットする)
>第一引数：作成するファイル名
>第二引数：取り込み元のファイル名(オプション)


__UPDATE4.0__
やっぱりwaveとcarrier分ける(fittingDiv3系列の前半のように)
やっぱりcsvの書き込みは1ファイルのfitting後ごとに行う



__UPDATE3.0__

* fittingの廃止→SN_PowerSearchに変更
* SN_PowerSearchに2つの関数
    * SN, Power作成
* csvは２つ吐き出す
    * SN
    * Power


__UPDATE2.4__
ファイル名はフルパスで受ける
globname.pyを新規作成

__UPDATE2.3__
データファイルの場所と注目すべき周波数はparameter.pyに記載

__INTRODUCTION__
各モジュールを動かすメインファイル

__ACTION__
引数:
dateFirst, dateLast : コンソールから入力、テストの際はコード内で書き換える
oldcsvS, newcsvS : コード内で書き換える

戻り値:なし(CSVファイルに書き込む)

1. datelistにより、フィッティングを行う最初の日付から最後の日付までのリストを抽出する。
コンソールに出力
2. (oldcsvS,newcsvS)で、読み込み元CSV, 書き込み先CSVファイルを指定する。
rawdataPathで、データの位置を指定する(日付)
3. parameterにより、inディレクトリとfittingに必要な周波数を指定する。
4. CSV_IOにより、CSVを読み込む。
5. fittingDivにより、fittingを行う。
6. CSV_IOにより、CSVを書き込む。


__USAGE__

* コマンドライン上にて`python main.py`で起動
    * SN, powerを出力するcsvファイル名(ディレクトリパスと拡張子は抜き)
    の入力が求められる(例：ファイル名をhogehoge.csvとしたければ、`hogehoge`と入力する)
    * フィッティング対象のデータの日付の入力が求められる`<最初の日付> <最後の日付>`。
    フォーマットはyymmdd形式(例：2015年11月1日の日付からにしたいときは`151101`と打ちこむ)
* CSV_IO.editCSV内でread, writeメソッドを1つの関数に収めた
    * fitting>read>translate>update>translate>writeの流れは1セット

__PLAN__

* プログラムを途中で止めるとこれまでの計算結果が記録されない
> writeメソッドが走るのはfor文の最後だから
> read, writeメソッドが走るタイミングを調整する
> keyboard interruptされたときにwriteメソッド機能するようにできる?
* 二重起動すると強制終了される
> マルチプロセス化ができない
> 書き込みが2重にくるからいけないんだと思う。
> 仕様として、月々ごとにまとめろ、とある
>> mainの親プロセスを作って、入力したら月々ごとにファイル名指定できるようにする？
* exe化する予定
> py2exe
* GUI化する予定
> TKinter
'''


# __BUILTIN MODULES__________________________
import pandas as pd
import numpy as np
import glob
from tqdm import tqdm
import simplejson
# __USER MODULES__________________________
import fitting
import CSV_IO as c

# __PARAMETER DEFINITION__________________________
with open('parameter.json', 'r') as pa:
    param = simplejson.load(pa)


# __CSV NAME__________________________
'''
コンソールからファイル名を指定
新規にファイルを作成するときは古いファイルと新しいファイルの名前を同一にする
新しいファイルの入力を省けば自動的に古い名前と同一にしてくれる
'''
oldinp = input('データ引き継ぎ元: 拡張子抜きのファイル名 >> ')
oldinpS, oldinpP = 'SN' + oldinp, 'P' + oldinp

print('新規作成したいとき or データ引継ぎ元ファイルに上書き => 何も入力せずEnter')
newinp = input('データ引き継ぎ先: 拡張子抜きのファイル名 >> ')
if not newinp:
    newinp = oldinp
newinpS, newinpP = 'SN' + newinp, 'P' + newinp

# newinpS=oldinpS
# newinpP=oldinpP

# 入力したファイルベースネームをフルパスと拡張しつけて返す
inplist = [oldinpS, oldinpP, newinpS, newinpP]
# inplistの各要素を引数に、'.csv'の文字を足してcsvlistに返す
csvlist = [oldcsvS,
           oldcsvP,
           newcsvS,
           newcsvP] = map(
    lambda inplist_element: param['out_csv'] + inplist_element + '.csv', inplist)

# ____________________________
print('SN value :\n\t読込元 %s\n\t書込先: %s' %
      (oldcsvS, newcsvS))  # 読み込み元ファイル名(フルパス)、書き込み先ファイル名(フルパス)表示
print('Power value :\n\t読込元 %s\n\t書込先: %s' %
      (oldcsvP, newcsvP))  # 読み込み元ファイル名(フルパス)、書き込み先ファイル名(フルパス)表示


# __fitting parameterの読み込み、結果の初期化__________________________
freqFreq = np.r_[param['freqWave'], param['freqCarrier']]   # np.r_クラスで行列の横向き結合
freqFreq = np.unique(freqFreq)  # np.unique重複する値削除
freqFreq.sort()  # 周波数のソート
# np.r_[freqFreq,['%s_0kHz,%s_1kHz'%(i,i) for i in param['freqM']]]   # freqMのラベル作成
print('fitting対象の周波数: %s' % freqFreq)

SNResult, powerResult = {}, {}  # fitting結果の初期化
# freqFreq=param['freqWave']+param['freqCarrier']


# __MAKE CSV__________________________
'''
oldcsvSを読み込んでnewcsvSに入れる
SNResultは空なのでoldcsvSがnewcsvSにコピーされるだけ
freqFreqで見出し行を作る
'''
c.editCSV(oldcsvS, newcsvS, SNResult, freqFreq)
c.editCSV(oldcsvP, newcsvP, powerResult, freqFreq)


try:
    # __FITTING__________________________
    plot = True if input('プロットしますか？ y/n >') == 'y' else False
    # for date in dl.date_range_input():  # pd.date_rangeの引数をinput方式にカスタマイズした
    inp_date = input('最初の日付, 最後の日付(カンマ区切りでyymmdd形式) >> ').split(',')  # カンマ区切りでリストの要素として拾う
    inp_date_nospace = [i.strip() for i in inp_date]  # リスト各要素の両端の空白を削除
    for da in tqdm(pd.date_range(*inp_date_nospace)):
        randate = da.strftime('%Y%m%d')
        print('''

___________________________________
次の年月日のファイルをfittingします。
            ''')
        print(randate)
        for fitfile in tqdm(glob.glob(param['in'] + randate + '*')):
            data = np.loadtxt(fitfile)  # load text data as array
            if not len(data):
                continue  # dataが空なら次のループ

            fitRtn = fitting.fitting(fitfile, plot_switch=plot)  # fitting.pyへフルパス渡す

            SNResult.update(fitRtn[0])  # fittingを行い、結果をSNResultに貯める
            powerResult.update(fitRtn[1])  # fittingを行い、結果をpowerResultに貯める
            # print('')
            # print('Now Fitting...', fitfile[-19:])
            # print('Write to SN...', list(fitRtn[0].values())[0])
            # print('Write to Power...', list(fitRtn[1].values())[0])

            # __WRITEING__________________________
            '''
            for文の中でc.editCSVを行うと
            逐一書き込むので処理の最中にctrl+Cで中断できるが
            (しかもfinallyステート内で最後に書き込みを行わせる)
            逐一ファイルの読み込みを行うので、
            csvファイルが巨大になっていくごとにc.editCSVの処理に時間がかかる

            **なるべく小分けに計算してあとでcsvを統合した方がいい。**

            '''
            # c.editCSV(newcsvS, newcsvS, SNResult, freqFreq)  # newcsvSにフィッティング結果を書き込む
            # c.editCSV(newcsvP, newcsvP, powerResult, freqFreq)  # newcsvSにフィッティング結果を書き込む
            # print('')
            # print('%sにSN値を書き込みました' % newcsvS)
            # print('%sにpower値を書き込みました' % newcsvP)
except KeyboardInterrupt:
    raise
finally:
    c.editCSV(newcsvS, newcsvS, SNResult, freqFreq)  # newcsvSにフィッティング結果を書き込む
    c.editCSV(newcsvP, newcsvP, powerResult, freqFreq)  # newcsvSにフィッティング結果を書き込む
    print('')
    print('%sにSN値を書き込みました' % newcsvS)
    print('%sにpower値を書き込みました' % newcsvP)
    print('fittingを終了します')
