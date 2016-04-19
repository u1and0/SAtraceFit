## ___CHARACTER OPERATION__________________________
load "SAtraceGraph/substr.gp"   #自作の文字列操作パッケージ

## ___PATH NAME__________________________
outdrct=dirname(ARG0)."/rawdata"   #このファイルのディレクトリパス+rawdata
outdrctBS=strsubst_sub(outdrct,1,"/","\\")   #バックスラッシュとスラッシュ置き換え


## __FORMULA__________________________
gauss(x)=aa*exp(-(x-mu)**2/2/si**2)+yy

############ここらへんをいじくりまわす
aa=0.2
mu=-0.7
si=0.5
yy=0.6
#############


## __MAKE DATA__________________________
set samples 50
set table outdrct."/mikan.dat"   #作成するファイル名
plot gauss(x)
unset table


## __INDICATE__________________________
command=sprintf('dir %s /b | awk "{print}"',outdrctBS)   # ファイル名一覧を出力するdir /bしてパイプでawkに渡す
list=system(command)   #awk実行
plot for[data in list] outdrct."/".data w l  title data   #ディレクトリ内の全プロットを重ねあわせ表示