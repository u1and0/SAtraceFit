## -----------------------------------------------------------------------
## plotSN.gp ver1.0
## <INTRODUCTION>
## SN±È¤Î•régÍÆÒÆ¤òÓ›åh¤·¤¿SN.csv¤ò¥×¥í¥Ã¥È¤¹¤ëgp
## <ACTION>
## --action--
## <USAGE>
## JUST BUILD
## <UPDATE>
## ver1.0
## -----------------------------------------------------------------------
cd 'C:/home/python/SAtraceGraph'

set grid
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
# set xrange ["2015-12-18 00:00:00":"2015-12-18 23:59:59"]
set format x "%m/%d\n%H:%M"
set datafile separator ","

# p 'SN160330_1.csv' u 1:2 w lp pt 7
p for [i =2:6] 'SN160330_1.csv' u 1:i w l