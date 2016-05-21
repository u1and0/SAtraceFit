# SAtraceFit Developer Manual
開発者用マニュアル
各モジュールの説明等、開発メモ




## main.py ver7.0

__UPDATE7.0__
ファイル名を呼び出して1ファイルだけmatplotlibに表示する用

### 使い方
1. cmdなどのターミナルを開く
2. このファイルのあるディレクトリまでcdする
3. ターミナルに`python main.py`と入力
> 値が入力されるcsvファイルのフルパスが表示される
4. 以下のように表示されるので、 **拡張子無しのファイル名** (=日時)を例に倣って入力する
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

















-------------------
## CSV_IO.py ver1.0
__INTRODUCTION__
関数readCSV,writeCSV, editCSVで構成される。
組み込み関数csv, os.path, datetime.datetimeを使用して、fittinngの結果を読み込み、書き込み、編集を行う。
各関数の説明は各関数のdocを参照。










### readCSV.py ver1.1
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








### writeCSV.py ver1.3
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






### editCSV ver1.0
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



























-------------------
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


























-------------------
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




















-------------------
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






---------------------
## fitting.py ver3.5

__UPDATE3.5__

* listdic モジュール追加
	* listdic()リストの一部を抜き出す:
	* search_maxy_returnx():2つのリスト(それぞれの要素同士は対応しているはず)をディクショナリ形式にする
* carrier fitの周辺ぼやかして探す
	* search_maxy_returnx()


around():リストの一部を抜き出す
はdataxをあらかじめpnt2freq()していないからうまく動かない
多くの箇所を直さなければならなくなるので後回し



## fitting.py ver3.1.2

__UPDATE3.1.2__
around関数作ってcarrierにも適用

__UPDATE3.1.1__
fitting conditionのwavewithminの条件を甘くした
=======


__UPDATE3.4__

1. co.Mfit()の低い方の周辺20Hzの周波数の最大値を探す。そのシグナル値をpower0とする
2. co.Mfit()の高い方の周辺20Hzの周波数のにおいて、power0のシグナル値と最も近いシグナル値を探す。そのシグナル値をpower1とする
3. 「power0のSNが10以上」 かつ 「power1がpower0の±20%以内ならばプロット」
> `if power0-noisef>10 and power0-noisef*0.8<power1-noisef<power0-noisef*1.2:`

* carriierの表示にはnoisefを引く必要があった


__UPDATE3.3__

1. co.Mfit()の低い方の周辺20Hzの周波数の最大値を探す。そのシグナル値をpower0とする
2. co.Mfit()の高い方の周辺20Hzの周波数のにおいて、power0のシグナル値と最も近いシグナル値を探す。そのシグナル値をpower1とする
3. power0のSNが10以上なら、フィッティングを行う
4. 「フィッティングの状態が良い」または「power1のSN比がpower0のSN比の±5%未満」ならばpower0とpower1をプロットする
> 「フィッティングの状態が良い」とは、指定した周波数付近に鋭くも潰れてもいないちょうど良い波が、SN比0以上で出ている。if文は次のようになる
> `if fitcondition(avefit,SNratio,fittingFreqFit,waveWidth,condSN=0,condmu=0.2) or (power0-noisef>10 and power0-noisef*0.95<power1-noisef<power0-noisef*1.05):
`

>>>>>>> origin/Mfit

__UPDATE3.1__
Mfit 
power1とpower0が最も近くなるようにpower1の周波数を決める
`xpower1=min(datadict1.items(), key=lambda x:abs(x[1]-power0))[0]
`


1. fittingしてwaveが出たならば2以降へ進む
低い方の周波数±20Hz付近をサーチして、最も大きい値をプロット。このときの値を"A"とする。
2. 低い方の周波数±20Hz付近をサーチして、"A"に最も近い大きさの点をプロットする
3. プロットされた周波数とシグナル及びSNをCSVファイルに吐きだす



__UPDATE3.0__
Mfit周波数の平均値でfitting
Mfit周波数低い方の±10Hzのmaxを見る
高い方の周波数との差が1dB未満で最も小さいところが高い方のSN
ない場合は24.0kHzでMfit周波数低い方のSNと重なっている可能性があるので、最も高い値にマーク

Mfit0, Mfit1の周波数±10Hzを捜索
1. Mfit0のなかで最大値をプロットする(power0と名づける)
2. Mfit1のなかでpower0に最も近い値をプロットする(power1と名づける)

__UPDATE2.1__
2周波数以上あるフィッティングは実際にそぐわないので、2宗派でキャリア見つける方式に変更

__UPDATE2.0__
Mfit：2周波数以上あるフィッティング
周波数はこのモジュールfitting.pyから直接confidentialに問い合わせる形式にした(元々はmainから問い合わせて引数として渡す)

Mfit関数
dualgauss関数追加


__UPDATE1.4__
プロットするとき、ラベルはマーカーだけに限定

__UPDATE1.3__
ラベルに国名を表示

__UPDATE1.2__
データプロットを最前面にした

__UPDATE1.1__

* loaddata プロットの太さを0.1>>>0.2変更
* 取り出すシグナル強度をダイヤモンドマーカーで表示
* ノイズフロアの表示
* pngで保存も可能にした

__UPDATE1.0__

* fittingDiv, SN_PowerSearchの統合
* waveとcarrier分けた

**課題**

* fittingの廃止
* powerを別ファイルに吐き出す

__UPDATE0.3.9.4__
差分が一定以上ある場合は、測定値(Carrierとみなす)
差分が一定以内におさまる場合は、fit(Waveとみなす)
差分:(fit-signaldiv)

__UPDATE0.3.9.3__
failebasenameではなくglobで拾われるフルパスに変更
indicateConditionにSNratio>5 を追加した(前処理で5以上と判断されても、fitしてみてS/N５以上とは限らないため)

__UPDATE0.3.9.2__
SN抽出対象をWaveとCarrierに分けた
	Wave:
		帯域持つのでfitする
		フィッティング結果のSNを出力
	Carrier:
		帯域持たず、fitすると異常に高い値が出ることがあるので、fitしない
		Carrierはその周波数のsignalとノイズフロアの差分をSNとして出力

__INTRODUCTION__
タイムスタンプと周波数を引数にフィッティング結果を返すpy

__ACTION__
引数:filebasename:タイムスタンプのこと。例えば'2015年01月01日12時35分06秒'を表す'20150101_123506'
	freqWave:帯域を持つ周波数のリスト
	freqCarrier:帯域を持たない周波数のリスト
戻り値:タプル形式
	1. SNのディクショナリ in ディクショナリ形式のフィッティング結果{タイムスタンプ:{周波数1:出力1,周波数2:出力2,...}}
	2. Powerのディクショナリ in ディクショナリ形式のフィッティング結果{タイムスタンプ:{周波数1:出力1,周波数2:出力2,...}}


1. データをテキスト形式で読み込みdataにリストとして読み込み
2. freqで指定した周波数の分だけfittingを行い
3. データとフィッティング曲線をプロットする
4. waveに格納された周波数をfittingする
5. waveとしてみるか判断(OKだったらプロット)>>>indicatecondition
6. carrierに格納された周波数をfittingする
7. carrierとしてみるか判断(OKだったらプロット)
8. ノイズフロアをプロット
9. 測定データのプロット
10. pngを吐き出す(オプションでプロットして表示)
11. ディクショナリ in ディクショナリを返す

__TODO__
* M-fitting:
	* fitting周波数が2つ
	* 2つの周波数の重ね合わせ
>list2dic()
dataxはロードする時点でpnt2freqかけておかないと
> around():リストの一部を抜き出す
> はdataxをあらかじめpnt2freq()していないからうまく動かない
> 多くの箇所を直さなければならなくなるので後回し





















---------------------
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






-------------------
## globname.py ver1.1

__UPDATE1.1__
拡張子無しファイル名入力`globfullname`関数追加

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
