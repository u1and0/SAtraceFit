'''
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



<<<<<<< HEAD
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


'''

import numpy as np
from scipy import stats
from scipy import optimize
import matplotlib.pyplot as plt
import sys
import datetime
d = datetime.datetime.today()
import confidential as co
import listdic as ld



def freq2pnt(x):return (x*1000-22000)/4

def pnt2freq(x):return (x*4+22000)/1000

logfile='./log/Log%s.log' % d.strftime("%Y%m%d")
def logprint(text,file=logfile):
	'''引数textに入った文字列をfileと標準出力両方に書き込む
	printの代わりに使える'''
	sys.stdout=open(file, "a")   #fileに上書き(a)で書き込む
	print(text)
	sys.stdout.close()
	sys.stdout = sys.__stdout__   #標準出力に書き込む
	print(text)


def plotshowing(title,ext=None,dir='./'):
	'''
	ext(拡張子)を指定すると保存する拡張子を指定できる
	デフォルトは標準出力(pyplot)
	dir(ディレクトリ)を指定すると保存するディレクトリを指定できる
	デフォルトはワーキングディレクトリ
	'''
	plt.title(d.strptime(title,'%Y%m%d_%H%M%S'))
	# plt.legend(loc='best',fancybox=True,fontsize='small')
	plt.legend(bbox_to_anchor=(0.5, -0.25), loc='center', borderaxespad=0,fontsize='small',ncol=3)
	plt.subplots_adjust(bottom=0.25)
	plt.xlabel('Frequency[kHz]')
	plt.ylabel('Power[dBm]')
	plt.grid(True)
	plt.ylim(ymin=-120,ymax=0)
	switch='plt.show()' if ext==None else 'plt.savefig(dir+title+"."+ext)'
	eval(switch)
	plt.close()

def loaddata(dataname):
	'''
	ファイル名を引数にデータをロードし、返す
	また、データのプロットも行う(plotshowはしない)
	'''
	data=np.loadtxt(dataname)   #load text data as array
	r=(datax,datay)=(data[:,0],data[:,2])
	return r




def fitting(dataname):
	(datax,datay)=loaddata(dataname)

	noisef=stats.scoreatpercentile(datay, 25)	#fix at 1/4median
	def gauss(x,*param):	#fitting function
		[aa,mu,si]=param
		return aa*np.exp(-(x-mu)**2/2/si**2)+noisef

	def gaussfit(x,y,mu):
		parameter_initial=[0,freq2pnt(mu),0.3]    #fitting初期値aa,mu,si
		paramater_optimal, covariance = optimize.curve_fit(gauss, x, y, p0=parameter_initial, maxfev = 100000000)
		rtnvalue=(gauss(datax,*paramater_optimal),
			paramater_optimal[0],
			pnt2freq(paramater_optimal[1]),
			abs(paramater_optimal[2]))
		'''rtnvalueの要素
		1. フィッティング結果(リスト)
		2. SN比
		3. フィッティング周波数
		4. 帯域幅'''
		return rtnvalue



	def SNextract(x,y):
		'''SNやシグナルのマーカーの表示
		ディクショナリに値を追加'''
		plt.plot(x,y,'D',fillstyle='none',markeredgewidth=1.5,label=str(freqFit)+co.country(freqFit))   #fitting結果のプロット
		if type(freqFit)!=float:
			k=0    #ラベルの添え字
			for i in freqFit:
				SNDict[str(freqFit)+'_'+str(k)+'kHz']=y-noisef  #周波数をキー、SN比を値にしてfittngDictへ入れる
				powerDict[str(freqFit)+'_'+str(k)+'kHz']=y  #周波数をキー、SN比を値にしてfittngDictへ入れる
				k+=1
		else:
			SNDict[str(freqFit)+'kHz']=y-noisef  #周波数をキー、SN比を値にしてfittngDictへ入れる
			powerDict[str(freqFit)+'kHz']=y  #周波数をキー、SN比を値にしてfittngDictへ入れる



	def fitcondition(freqFit,SNratio,fittingFreqFit,waveWidth,condSN=5,condwavewidthmin=1,condwavewidthmax=100, condmu=0.05 ):
		return (SNratio>condSN 
			and condwavewidthmin<waveWidth<condwavewidthmax 
			and abs(freqFit-fittingFreqFit)<condmu) #幅が0~100の間に入るとき(正常なガウシアン)
			   #フィッティングされた周波数とフィッティングするはずの周波数のずれが50Hz以内



	plt.figure(figsize=(6,6))
	SNDict,powerDict={},{}
	for freqFit in co.freqWave():   #freqWaveの周波数をfit
		fitrange=0.2
		dataxRange=datax[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]   #±200Hzをフィッティングする
		datayRange=datay[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]
		fitresult=[fity,SNratio,fittingFreqFit,waveWidth]=list(gaussfit(dataxRange,datayRange,freqFit))
		# if (SNratio>5 
		# 		and 1<waveWidth<100    #幅が0~100の間に入るとき(正常なガウシアン)
		# 		and abs(freqFit-fittingFreqFit)<0.05) :   #フィッティングされた周波数とフィッティングするはずの周波数のずれが50Hz以内
		if fitcondition(freqFit,SNratio,fittingFreqFit,waveWidth):
			# plt.plot(pnt2freq(datax),fity,'-',lw=1)   #fitting結果のプロット
			SNextract(fittingFreqFit,SNratio+noisef)
	for freqFit in co.freqCarrier():   #freqCarrierの周波数のシグナルを取得
		datadict=ld.twoList2dic(pnt2freq(datax[freq2pnt(freqFit-0.01):freq2pnt(freqFit+0.01)]),datay[freq2pnt(freqFit-0.01):freq2pnt(freqFit+0.01)])
		print('datad',datadict)
		xpower=ld.search_maxy_returnx(datadict)
		power=datadict[xpower]

		# poww=datay[freq2pnt(freqFit)]
		if power-noisef>10:    #SN比が10以上ならCarrierが出ているとみなす
			SNextract(xpower,power)
			print('Plot!', xpower,power)
		# if poww-noisef>10:    #SN比が10以上ならCarrierが出ているとみなす
		# 	SNextract(freqFit,poww)








	for freqFit in co.freqM():   #freqMの周波数のシグナルを取得
		datadict0=ld.twoList2dic(pnt2freq(datax[freq2pnt(freqFit[0]-0.02):freq2pnt(freqFit[0]+0.02)]),datay[freq2pnt(freqFit[0]-0.02):freq2pnt(freqFit[0]+0.02)])
		xpower0=ld.search_maxy_returnx(datadict0)
		power0=datadict0[xpower0]




		datadict1=ld.twoList2dic(pnt2freq(datax[freq2pnt(freqFit[1]-0.02):freq2pnt(freqFit[1]+0.02)]),datay[freq2pnt(freqFit[1]-0.02):freq2pnt(freqFit[1]+0.02)])


		'''
		print('\n'*6,dataname,'\n','Show datadict1!!',datadict1.items())
		print('\n'*4,'Which one is NEAR!?!?!?\n',min(datadict1.items(), key=lambda x:abs(x[1]-power0))[0])
		'''


		xpower1=(min(datadict1.items(), key=lambda x:abs(x[1]-power0))[0])    #datadict1をキーと値でタプルにして、要素の1番目(ディクショナリの値)を比較して、min(power0との差が最も小さい)ところのタプルの第0要素を返す
		power1=datadict1[xpower1]



		print('!!!!!!!!!!!!!!!!!!!!!!!!!!')
		print('Plot!!!\n',xpower0,power0)
		print('Plot!!!\n',xpower1,power1)


		avefit=np.mean(freqFit)
		fitrange=0.2
		dataxRange=datax[freq2pnt(avefit-fitrange):freq2pnt(avefit+fitrange)]   #±200Hzをフィッティングする
		datayRange=datay[freq2pnt(avefit-fitrange):freq2pnt(avefit+fitrange)]
		fitresult=[fity,SNratio,fittingFreqFit,waveWidth]=list(gaussfit(dataxRange,datayRange,avefit))
		# plt.plot(pnt2freq(datax),fity,'-',lw=1)   #fitting結果のプロット
		if fitcondition(avefit,SNratio,fittingFreqFit,waveWidth,condwavewidthmin=1,condSN=-5,condmu=0.2) and power0-noisef>5 and power1-noisef>5:


			SNextract(xpower0,power0)
			SNextract(xpower1,power1)

























	SNData,powerData={},{}
	import os
	filebasename=os.path.basename(dataname)[:-4]
	SNData[d.strptime(filebasename,'%Y%m%d_%H%M%S')]=SNDict  #ファイル名(=タイムスタンプ)をキーに、SNDictを値にSNDataへ入れる
	powerData[d.strptime(filebasename,'%Y%m%d_%H%M%S')]=powerDict  #ファイル名(=タイムスタンプ)をキーに、powerDictを値にpowerDataへ入れる
	outData=[SNData,powerData]
	# print('SN: %s\npower: %s'% (SNData,powerData))



	plt.plot(pnt2freq(datax),[noisef for i in datax],'-',lw=1,color='k')    #ノイズフロアのプロット
	plt.plot(pnt2freq(datax),datay,'-',lw=0.2,color='k')    #測定データのプロット

	plotshowing(filebasename,ext='png',dir=co.out()+'PNG/')    #extは拡張子指定オプション(デフォルトはplt.show())、dirは保存するディレクトリ指定オプション


	return outData











# '''
# TEST
# '''
# import confidential as co
# a=co.rootroot()+'20160112_132741.txt'
# b=co.freqWave
# c=co.freqCarrier
# fitting(a,b,c)