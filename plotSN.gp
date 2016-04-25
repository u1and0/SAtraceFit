## -----------------------------------------------------------------------
## plotSN.gp ver2.0
# __UPDATE2.0__
# awkコマンドを用いてcsvの見出し行を取得する
# __INTRODUCTION__
# SN比の時間推移を記録したSN.csvをプロットするgnuplotファイル
# __ACTION__
# x軸を時間軸にする
# set datafile separator ","でデータ区切りをコンマにする(csvファイルなので。)
# awkコマンドを用いてcsvの見出し行を取得する
# __USAGE__
# JUST BUILD
## -----------------------------------------------------------------------
cd 'C:/home/python/SAtraceFit'
file='160425.csv'
# file='SN160330_1.csv'

set grid
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
# set xrange ["2016-1-1 00:00:00":"2016-1-10 23:59:59"]
set format x "%m/%d\n%H:%M"
set datafile separator ","

## __SINGLE PLOT__________________________
# i=2
# p[][:100]  file u 1:i w l title system(sprintf('awk -F, "NR==1{print $%d}" %s',i,file))

## __MULTIPLOT__________________________
lastrow=system(sprintf('awk -F, "NR==1{print NF}" %s',file))
p for[i=2:lastrow] file u 1:i w lp ps 0.5 pt 7 title system(sprintf('awk -F, "NR==1{print $%d}" %s',i,file))
