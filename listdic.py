'''
## listdic.py ver1.0

__UPDATE1.0__
First commit

__USAGE__
`from listdic import *`
を記述して正しい引数を用いて使用する

__INTRODUCTION__
リストとディクショナリの操作

__ACTION__
--action--

__TODO__
None
'''



def around(li,c,r):    #listx,yはdatax,yだから0,1,2,3...と-89,-90,-87,...
	'''リストの一部を抜き出す'''
	return li[c-r:c+r]



def twoList2dic(keyList,valList):
	'''2つのリスト(それぞれの要素同士は対応しているはず)をディクショナリ形式にする'''
	return dict(zip(keyList, valList))



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



# def freqlist_diclist(lx):
# 	for i in 