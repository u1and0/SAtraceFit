# SAtraceFit Developer Manual
開発者用マニュアル
各モジュールの説明等、開発メモ

## main.py v7.0.0

__USAGE__
コマンドライン上で`python main.py`で実行

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






## datelist.datelist()

**廃止**
datelist.date_range_input()にアップグレード


__UPDATE1.0__
first commit

__INTRODUCTION__
main.pyから2つの値が渡される
2つの間の日付のリストを返す

__ACTION__
yymmdd形式の6桁をdatetime関数で日付にする
ddate1,2に代入する
ddate1がddate2になるまで(while)
ddate1を1日ずつ足して、リストに追加する(append)

__USAGE__
引数 : 最初の日付yymmdd形式、最後の日付yymmdd形式
戻り値 : 最初の日付から最後の日付を入れたリストyymmdd形式


__PLAN__
none



## datelist.date_range_input()

* ファイル名のglobに用いる日付を基にした文字列をyieldするgenerator
* 引数:なし(ユーザーに入力施す)
* 戻り値:
	* datestr:文字列(%Y%m%d形式)












## confidential.py ver1.0

__INTRODUCTION__
データの入ったrootディレクトリと注目する周波数を指定するpy

__ACTION__
関数入れているだけ

__USAGE__
root():データの入ったrootディレクトリ
引数:なし
戻り値:rootPath(文字列)

freq() : 注目する周波数を指定する
引数 : なし
戻り値 : freqWave(リスト)

__UPDATE1.0__
first commit

__PLAN__
none













## CSV_IO.py ver1.0
__INTRODUCTION__
関数readCSV,writeCSV, editCSVで構成される。
組み込み関数csv, os.path, datetime.datetimeを使用して、fittinngの結果を読み込み、書き込み、編集を行う。
各関数の説明は各関数のdocを参照。










## readCSV.py ver1.1
__UPDATE1.1__
クラス'csv.DictReader()'を使ってディクショナリ形式でcsvを取り出す。
キーは見出し(csvの1行目)
行を読むたびリスト'dictList'へ追加する
dictListを返す
__INTRODUCTION__
csvファイルの中身をディクショナリに入れるpy
引数：ファイル名
戻り値：ディクショナリ'mydict
__ACTION__
filenameにいれた名前のファイルを開く
リスト'reader'に格納する
リスト'reader'に対して0要素目をキーに、1要素目以降(リスト形式)を値にしたディクショナリ'mydict'を作成する








## writeCSV.py ver1.3
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
__改造予定__
datetimeでソートしたい






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

```
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
|.| | | | |
|.| | | | |
|v(0,m-1)|v(1,m-1)|v(2,m-1)|...v(n,m-1)|
|v(0,m)|v(1,m)|v(2,m)|...v(n,m)|

		^
		|    <<ココはpython組み込み関数でできる
		v

```
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

```
# データ整理用 ディクショナリ in ディクショナリ形式
{
	{v00:{k1:v10,k2:v20,...,k(n-1):v(n-1,0),k(n):v(n,0)},
	{v01:{k1:v11,k2:v21},...,k(n-1):v(n-1,1),k(n):v(n,1)},
	...,
	{v0m:{k1:v(1,m),k2:v(2,m),...,k(n-1):v(n-1,m),k(n):v(n,m)}
}
```



__USAGE__
CSV_IO.pyから呼び出される。
各関数のdoc参照
Testはコメントアウト外してbuildするのみ



























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









## fittingDiv.py ver0.3.8

__UPDATE0.3.8__
datayとyyを比較することでS/N比が大体どれくらいか見積もることでfittingにかけるべきか否かわかる
>fittingかけなくてすめば時間短縮
>何故かfittingされちゃう1.0e+8みたいなデータもなくなる

__INTRODUCTION__
タイムスタンプを引数にフィッティング結果を返すpy

__ACTION__
引数:

+ rawdata_directory
>生データ置き場
>rootディレクトリ+日付(yymmdd形式)
>>SAtraceGraphで作成されたディレクトリ
+ filebasename
> 拡張子を除いたファイル名
> SAtraceによってタイムスタンプとされている
> 例えば'2015年01月01日12時35分06秒'を表す'20150101_123506'
+ freqWave
> フィッティングする周波数

戻り値:フィッティング結果(ディクショナリ in ディクショナリ形式{タイムスタンプ:{周波数1:出力1,周波数2:出力2,...}})

1. データをテキスト形式で読み込みdataにリストとして読み込む
1. 下からの四分位境界値(小さい順に並べて全体の1/4番目にある値)をノイズフロアと定義する
2. freqWaveで指定した周波数の分だけfittingを行う
3. データとフィッティング曲線をプロットする
> 内部処理なので表示はしない
4. ガウス曲線に従ってfittingする





```math
\frac{\pi}{2}
```


5. 表示するかしないか判断
6. プロットして表示(オプション)
7. ログを吐き出す
8. ディクショナリ in ディクショナリを返す

__PLAN__
None






## plotSN.gp ver2.0
__UPDATE2.0__
awkコマンドを用いてcsvの見出し行を取得する
__INTRODUCTION__
SN比の時間推移を記録したSN.csvをプロットするgnuplotファイル
__ACTION__
x軸を時間軸にする
set datafile separator ","でデータ区切りをコンマにする(csvファイルなので。)
awkコマンドを用いてcsvの見出し行を取得する
__USAGE__
JUST BUILD










## globname.py ver1.0

__UPDATE1.0__
first commit

__USAGE__
mainから呼び出す
引数:
	rootpath: 
	dateFirst:最初の日付yymmdd形式
	dateLast:最後の日付yymmdd形式
戻り値:リストfilebesename
 ~~イテレータでもいいな~~

globのhelpによるとリストを返すらしい
>    glob(pathname, *, recursive=False)
>        Return a list of paths matching a pathname pattern.


__INTRODUCTION__
最初と最後の日付をもらって、その中のfilebasename(拡張子無しのファイル名)

__ACTION__
datetime関数で日付の形式に直して
globの

__PLAN__
none