'''
## fitting.py ver1.3

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
4. fittingする
5. 表示するかしないか判断
# 6. プロットして表示
7. ログを吐き出す
8. ディクショナリ in ディクショナリを返す

__PLAN__
'''

import numpy as np
from scipy import stats
from scipy import optimize
import matplotlib.pyplot as plt
import sys
import datetime
d = datetime.datetime.today()
import confidential as co



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
	plt.legend(bbox_to_anchor=(0.5, -0.25), loc='center', borderaxespad=0,fontsize='small',ncol=4)
	plt.subplots_adjust(bottom=0.25)
	plt.xlabel('Frequency[kHz]')
	plt.ylabel('Power[dBm]')
	plt.grid(True)
	plt.ylim(ymin=-120,ymax=0)
	switch='plt.show()' if ext==None else 'plt.savefig(dir+title+"."+ext)'
	eval(switch)
	plt.close()

def loaddata(dataname):
	'''ファイル名を引数にデータをロードし、返す
	また、データのプロットも行う(plotshowはしない)'''
	data=np.loadtxt(dataname)   #load text data as array
	r=(datax,datay)=(data[:,0],data[:,2])
	return r





def fitting(dataname,freqWave,freqCarrier):
	(datax,datay)=loaddata(dataname)

	yy=stats.scoreatpercentile(datay, 25)	#fix at 1/4median
	def gauss(x,aa,mu,si):	#fitting function
		return aa*np.exp(-(x-mu)**2/2/si**2)+yy


	def gaussfit(x,y,mu):
		parameter_initial=[0,freq2pnt(mu),0.3]    #fitting初期値aa,mu,si
		paramater_optimal, covariance = optimize.curve_fit(gauss, x, y, p0=parameter_initial, maxfev = 100000000)
		rtnvalue=(gauss(datax,paramater_optimal[0],paramater_optimal[1],paramater_optimal[2]),
			paramater_optimal[0],
			pnt2freq(paramater_optimal[1]),
			abs(paramater_optimal[2]))
		'''rtnvalueの要素
		1. フィッティング結果(リスト)
		2. SN比
		3. フィッティング周波数
		4. 帯域幅'''
		return rtnvalue



	def SNextract(x):
		'''SNやシグナルのマーカーの表示'''
		plt.plot(x,SNratio+yy,'D',fillstyle='none',markeredgewidth=1.5,label=str(freqFit)+co.country(freqFit))   #fitting結果のプロット
		SNDict[str(freqFit)+'kHz']=SNratio  #周波数をキー、SN比を値にしてfittngDictへ入れる
		powerDict[str(freqFit)+'kHz']=SNratio+yy  #周波数をキー、SN比を値にしてfittngDictへ入れる








	plt.figure(figsize=(6,6))
	indicateCondition='SNratio>5 and (1<waveWidth<100) and abs(freqFit-fittingFreqFit)<0.05'    #幅が0~100の間に入るとき(正常なガウシアン)　かつ　フィッティングされた周波数とフィッティングするはずの周波数のずれが50Hz以内
	SNDict,powerDict={},{}
	for freqFit in freqWave:   #freqWaveの周波数をfit
		## __FIT__________________________
		fitrange=0.2
		dataxRange=datax[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]   #±200Hzをフィッティングする
		datayRange=datay[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]
		fitresult=[fity,SNratio,fittingFreqFit,waveWidth]=list(gaussfit(dataxRange,datayRange,freqFit))
		if eval(indicateCondition) :   #indicateConditionにマッチしたウェーブだけをプロットする
			plt.plot(pnt2freq(datax),fity,'-',lw=1,label=str(freqFit)+co.country(freqFit))   #fitting結果のプロット
			SNextract(fittingFreqFit)
	for freqFit in freqCarrier:   #freqCarrierの周波数のシグナルを取得
		SNratio=datay[freq2pnt(freqFit)]-yy
		if SNratio>10:    #SN比が10以上ならCarrierが出ているとみなす
			SNextract(freqFit)


	SNData,powerData={},{}
	import os
	filebasename=os.path.basename(dataname)[:-4]
	SNData[d.strptime(filebasename,'%Y%m%d_%H%M%S')]=SNDict  #ファイル名(=タイムスタンプ)をキーに、SNDictを値にSNDataへ入れる
	powerData[d.strptime(filebasename,'%Y%m%d_%H%M%S')]=powerDict  #ファイル名(=タイムスタンプ)をキーに、powerDictを値にpowerDataへ入れる
	outData=[SNData,powerData]
	# print('SN: %s\npower: %s'% (SNData,powerData))



	plt.plot(pnt2freq(datax),[yy for i in datax],'-',lw=1,label=None,color='k')    #ノイズフロアを黒色で表示
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