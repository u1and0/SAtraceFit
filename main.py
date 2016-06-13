'''
## main.py ver7.2.1

__UPDATE7.2.2__
例文をraw文で表示(print(トリプルクォート文字列 トリプルクォート))

__UPDATE7.2.1__
コマンドライン表示文の変更

__UPDATE7.2__
入力の冗長化
globregname関数
rootpath内のファイルのフルパスを返す
ファイル名は`20`で始まり、`.txt`で終わる文字列
ワイルドカードを入力者にも使えるようにした

### 使い方
1. cmdなどのターミナルを開く
2. このファイルのあるディレクトリまでcdする
3. **開始**  ターミナルに`python main.py`と入力
> 値が入力されるcsvファイルのフルパスが表示される
4. 以下のように表示されるので、**拡張子無しのファイル名**(=日時)を例に倣って入力する
>____________________________
>使い方
>グラフ化したいファイルベースネーム(拡張子抜きのファイル名)を入力
>ワイルドカードも使えます！
>"*"0文字以上の文字列
>"?"1文字か0文字の文字列
>使える正規表現一覧: http://docs.python.jp/3/library/re.html
>(例)20151201_000344		<<<2015/12/01 00:03:44のデータ
>(例)*151201_000344		<<<2015/12/01 00:03:44のデータ
>(例)*151201_000344*		<<<2015/12/01 00:03:44のデータ
>(例)*151201_001*			<<<2015/12/01 0時10分～19分のデータ
>(例)*151201_00*			<<<2015/12/01 00時台のデータ
>(例)*151201_0*			<<<2015/12/01 0～9時台のデータ
>(例)*151201*				<<<2015/12/01のデータ
>(例)201601??_21*			<<<2016年1月??日のデータのうち、21時台のデータ
>(例)*1201_19??56			<<<？年12月1日のデータのうち、19時台で56秒で終わっているデータ
>(例)201601??_2[13]*			<<<2016年01月のデータのうち、21時台か23時台のデータ
>ファイル名を入力して下さい>>>
5. `Enter`キーを押す
>グラフ化するデータのフルパスがすべて表示される
5. 別ウィンドウでグラフが表示され、ターミナルにはファイル名とプロットした座標が描かれる。グラフの拡大縮小、保存等の操作を行う
6. **次のグラフへ移行**  グラフをバツ印で消す
>項目3の注釈にあるcsvファイルにプロットされたSN比とシグナル強度が書き込まれる。
7. **終了操作**  ターミナル上で`ctrl+c`でループの中断、またはループが最後まで行く
8. 項目3操作に戻る




__UPDATE7.0__
ファイル名を呼び出して1ファイルだけmatplotlibに表示する用

### 使い方
1. cmdなどのターミナルを開く
2. このファイルのあるディレクトリまでcdする
3. ターミナルに`python main.py`と入力
> 値が入力されるcsvファイルのフルパスが表示される
4. 以下のように表示されるので、**拡張子無しのファイル名**(=日時)を例に倣って入力する
> ____________________________
> 使い方
> グラフ化したいファイル名を"拡張子無しで"入力
> (例)20151201_000344
> ファイル名を入力して下さい>>>
5. 別ウィンドウでグラフが表示され、ターミナルにはファイル名とプロットした座標が描かれる。グラフの拡大縮小、保存等の操作を行う
6. グラフをバツ印で消す
7. 項目3の注釈にあるcsvファイルにプロットされたSN比とシグナル強度が書き込まれる。
8. 項目3操作に戻る



__UPDATE6.1.1__
fot Mfit test

__UPDATE6.1__
fittting の引数に周波数は入れない(fittingのforステートメント中にconfidentialから直接引っ張る)

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
データファイルの場所と注目すべき周波数はconfidential.pyに記載

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
3. confidentialにより、rootディレクトリとfittingに必要な周波数を指定する。
4. CSV_IOにより、CSVを読み込む。
5. fittingDivにより、fittingを行う。
6. CSV_IOにより、CSVを書き込む。


__USAGE__

* コマンドライン上にて`python main.py`で起動
	SN, powerを出力するcsvファイル名(ディレクトリパスと拡張子は抜き)の入力が求められる(例：ファイル名をhogehoge.csvとしたければ、`hogehoge`と入力する)
	フィッティング対象のデータの日付の入力が求められる`<最初の日付> <最後の日付>`。フォーマットはyymmdd形式(例：2015年11月1日の日付からにしたいときは`151101`と打ちこむ)
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
* csvの容量が大きくなるとプロセスの進行が遅れる
> 読み込みに時間がかかる
> 読み込みがfor文ごとにあるのがいけない
>> for文終了後に一気に書き込みできるようにする
>>> keyboard interruptされたときにwriteメソッド機能するようにしないと、プロセス中断すると計算結果がメモリとともに消えてしまう
* 日付だけでなく時間を引数にする
'''


import confidential as co
## __CSV NAME__________________________
'''
コンソールからファイル名を指定
新規にファイルを作成するときは古いファイルと新しいファイルの名前を同一にする
新しいファイルの入力を省けば自動的に古い名前と同一にしてくれる
'''
# oldinpS=input('Input old SN file base name>>> ')
# oldinpP=input('Input old power file base name>>> ')

# print('新規にファイルを作成したいときは何も入力せずENTER')
# newinpS=input('Input new SN file base name>>> ')
# if not newinpS:newinpS=oldinpS
# print('新規にファイルを作成したいときは何も入力せずENTER')
# newinpP=input('Input new power file base name>>> ')
# if not newinpP:newinpP=oldinpP

# inplist=[oldinpS,oldinpP,newinpS,newinpP]
# csvlist=[oldcsvS,oldcsvP,newcsvS,newcsvP]=map(lambda inp: co.out()+'\\CSV\\'+inp+'.csv' ,inplist)    #入力したファイルベースネームをフルパスと拡張しつけて返す
## ____________________________
'''開発環境内であらかじめファイル名を指定'''
(oldcsvS,newcsvS)=(co.out()+'\\CSV\\TEST\\SNfitting.csv',co.out()+'\\CSV\\TEST\\SNfitting.csv')
print('Read from %s\nWrite to %s'% (oldcsvS,newcsvS))
(oldcsvP,newcsvP)=(co.out()+'\\CSV\\TEST\\Pfitting.csv',co.out()+'\\CSV\\TEST\\Pfitting.csv')
## ____________________________
print('SN value :\nRead from %s\nWrite to %s'% (oldcsvS,newcsvS))    #読み込み元ファイル名(フルパス)、書き込み先ファイル名(フルパス)表示
print('Power value :\nRead from %s\nWrite to %s'% (oldcsvP,newcsvP))    #読み込み元ファイル名(フルパス)、書き込み先ファイル名(フルパス)表示





##__MAKE CSV__________________________
'''
oldcsvSを読み込んでnewcsvSに入れる
SNResultは空なのでoldcsvSがnewcsvSにコピーされるだけ
freqFreqで見出し行を作る
'''
SNResult,powerResult={},{}
freqFreq=co.freqWave()+co.freqCarrier()
outPath=co.out()    #ルートパス

import CSV_IO as c
c.editCSV(oldcsvS,newcsvS,SNResult,freqFreq)
c.editCSV(oldcsvP,newcsvP,powerResult,freqFreq)







# # >>>>>master
# ## __DATE LIST__________________________
# from datelist import datelist  #最初と最後の日付(yymmdd形式)を引数に、その間の日付をリストとして返す
# ## ____________________________
# '''コンソールから入力'''
# dateFirst=input('Input First Date>>> ')
# dateLast=input('Input Last Date>>> ')
# if not dateLast:    #dateLastの入力がなければdateFirstと同じにする
# 	dateLast=dateFirst
# ## ____________________________
# '''開発環境内でリストの最初と最後を指定'''
# # dateFirst='151201'
# # dateLast='151201'
# dateList=datelist(dateFirst,dateLast)  #最初から最後の日付のリストを返す
# ## ____________________________
# # '''リストで指定'''
# # dateList=['151201']
# ## ____________________________
# print('\nNow extracting from these dates\n%s\n'% dateList)
# filepath=g.globname(co.root(),dateList)    #dateList内の日付に測定されたファイル名のリスト(20151111_??????.txtが288×たくさん個)



# >>>>timearg
print('''
____________________________
<使い方>
グラフ化したいファイルベースネーム(拡張子抜きのファイル名)を入力
ワイルドカードも使えます！
"*"0文字以上の文字列
"?"1文字か0文字の文字列
"[]"の中に書いた文字列一文字ずつ(たとえば[135]は"1か3か5", [2-8]は"2,3,4,5,6,7,8のどれか")
使える正規表現一覧: http://docs.python.jp/3/library/re.html
(例)20151201_000344	<<<2015/12/01 00:03:44のデータ
(例)*151201_000344	<<<2015/12/01 00:03:44のデータ
(例)*151201_000344*	<<<2015/12/01 00:03:44のデータ
(例)*151201_001*	<<<2015/12/01 0時10分～19分のデータ
(例)*151201_00*		<<<2015/12/01 00時台のデータ
(例)*151201_0*		<<<2015/12/01 0～9時台のデータ
(例)*151201*		<<<2015/12/01のデータ
(例)201601??_21*	<<<2016年1月??日のデータのうち、21時台のデータ
(例)*1201_19??56	<<<？年12月1日のデータのうち、19時台で56秒で終わっているデータ
(例)201601??_2[13]*	<<<2016年01月のデータのうち、21時台か23時台のデータ
''')
filename=input('ファイル名を入力して下さい>>> ')
print('____________________________')
import globname as g
filepath=g.globregname(co.root(),filename)    #dateList内の日付に測定されたファイル名のリスト(20151111_??????.txtが288×たくさん個)
# print('グラフ化するファイルのフルパス: ',filepath)
print('''
____________________________
以上のファイルをグラフ化します
中断するときは`ctrl+c`!!!
____________________________
''')




try:
	# __FITTING__________________________
	for fitfile in filepath[0:] :
		import fitting as f
		import numpy as np
		data=np.loadtxt(fitfile)   #load text data as array
		if not len(data):continue    #dataが空なら次のループ
		fitRtn=f.fitting(fitfile)
		SNResult.update(fitRtn[0])    #fittingを行い、結果をSNResultに貯める
		powerResult.update(fitRtn[1])    #fittingを行い、結果をSNResultに貯める
		print('Write to SN\n', fitRtn[0])
		print('Write to Power\n', fitRtn[1])

except KeyboardInterrupt:
	print('Why do you interrupt me!?')


finally:
	## __WRITEING__________________________
	print('Write to SN\n', SNResult)
	print('Write to Power\n', powerResult)
	c.editCSV(newcsvS,newcsvS,SNResult,freqFreq)    #newcsvSにフィッティング結果を書き込む
	c.editCSV(newcsvP,newcsvP,powerResult,freqFreq)    #newcsvSにフィッティング結果を書き込む
	# SNResult,powerResult={},{}    #SNResultのリセット
