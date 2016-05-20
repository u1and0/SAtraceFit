'''
## listdic.py ver1.0

__UPDATE1.0__
First commit

__USAGE__
使用したいモジュール内に
`from listdic import *`
`import listdic as ld`
などと記述して指定した引数を用いて使用する

__INTRODUCTION__
リストとディクショナリの操作

__ACTION__
--action--

__TODO__
aroundはfittingモジュールのdataxを最初からpnt2freqかけておかないと
互換性の問題が大規模すぎるので今は後回し
'''



def around(li,c,r):    #listx,yはdatax,yだから0,1,2,3...と-89,-90,-87,...
	'''リストの一部を抜き出す'''
	return li[c-r:c+r]



def twoList2dic(keyList,valList):
	'''2つのリスト(それぞれの要素同士は対応しているはず)をディクショナリ形式にする'''
	return dict(zip(keyList, valList))
		# ゴリゴリ書くとこんな感じ
		# for i in datax[freq2pnt(freqFit[1]-0.02):freq2pnt(freqFit[1]+0.02)]:    #iはdataxの限られたポイント数
		# 	datadict1[pnt2freq(datax[i])]=datay[i]


'''
TEST
a=['a','b','c','d']
b=[9,8,7,6]

print(around(a,1,1))

print(twoList2dic(a,b))
# >>{'b': 8, 'c': 7, 'a': 9, 'd': 6}
print(twoList2dic(around(a,1,1),around(b,1,1)))
# >>{'b': 8, 'a': 9}
'''

def search_maxy_returnx(dic):
	'''ディクショナリの値の最大値を探し、そのときのキーを返す'''
	return max(dic.items(), key=lambda x:x[1])[0]