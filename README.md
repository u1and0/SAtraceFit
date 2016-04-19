# SAtraceFit
SAtraceによって収集された5分間隔のファイルを集計するPythonコードの説明を行う。




# データ定義

## データ形式
1000行4列のtxtファイル
`ファイル名=タイムスタンプ(測定時刻yyyymmdd_HHMMSS.txt)`
日付が最初の8桁、アンダースコアを挟んで、時間を6桁で表している。

1列目 : 行数
2列目 : maxホールド
3列目 : 平均値
4列目 : minimumホールド

スタート周波数が行数をxとしたとき、(x*4+22000)/1000で周波数となる。
ここでは2列目


## データの場所
ファイル名confidential.pyに変数rootPathとして格納した。













# 各モジュールの説明


## main.py ver2.3

## main.py ver2.3

### UPDATE2.3
外部に出したくない情報は別ファイルに格納(confidential.py)

### INTRODUCTION
各モジュールを動かすメインファイル

### ACTION
引数:
dateFirst, dateLast : コーンソールから入力、テストの際はコード内で書き換える
oldcsv, newcsv : コード内で書き換える

戻り値:なし(CSVファイルに書き込む)

1. datelistにより、フィッティングを行う最初の日付から最後の日付までのリストを抽出する。
コンソールに出力
2. (oldcsv,newcsv)で、読み込み元CSV, 書き込み先CSVファイルを指定する。
rawdataPathで、データの位置を指定する(日付)
3. confidentialにより、rootディレクトリとfittingに必要な周波数を指定する。
4. CSV_IOにより、CSVを読み込む。
5. fittingDivにより、fittingを行う。
6. CSV_IOにより、CSVを書き込む。


### USAGE
コマンドライン上にて
python main.py <最初の日付> <最後の日付>
フォーマットはyymmdd形式(例えば2015年11月1日=151101と打ちこむ)
CSV_IO.editCSV内でread, writeメソッドを1つの関数に収めた
	fitting>read>translate>update>translate>writeの流れは1セット

### PLAN
プログラムを途中で止めるとこれまでの計算結果が記録されない
	>>>writeメソッドが走るのはfor文の最後だから
	read, writeメソッドが走るタイミングを調整する
二重起動すると強制終了される
	マルチプロセスかができない












## datelist.py

## datelist.py ver1.0

### INTRODUCTION
main.pyから2つの値が渡される
2つの間の日付のリストを返す

### ACTION
yymmdd形式の6桁をdatetime関数で日付にする
ddate1,2に代入する
ddate1がddate2になるまで(while)
ddate1を1日ずつ足して、リストに追加する(append)

### USAGE
引数 : 最初の日付yymmdd形式、最後の日付yymmdd形式
戻り値 : 最初の日付から最後の日付を入れたリストyymmdd形式

### UPDATE1.0
first commit

## PLAN
none