'''
## fittingDiv.py ver1.0

__UPDATE1.0__
gaussの調整
SNSearch

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
タイムスタンプを引数にフィッティング結果を返すpy

__ACTION__
引数:filebasename
	タイムスタンプのこと。例えば'2015年01月01日12時35分06秒'を表す'20150101_123506'
戻り値:ディクショナリ in ディクショナリ形式のフィッティング結果{タイムスタンプ:{周波数1:出力1,周波数2:出力2,...}}

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


def freq2pnt(x):
	return (x*1000-22000)/4

def pnt2freq(x):
	return (x*4+22000)/1000

logfile='./log/Log%s.log' % d.strftime("%Y%m%d")
def logprint(text,file=logfile):
	'''引数textに入った文字列をfileと標準出力両方に書き込む
	printの代わりに使える'''
	sys.stdout=open(file, "a")   #fileに上書き(a)で書き込む
	print(text)
	sys.stdout.close()
	sys.stdout = sys.__stdout__   #標準出力に書き込む
	print(text)


def plotshowing(title):
	plt.title(d.strptime(title,'%Y%m%d_%H%M%S'))
	plt.legend(loc='best',fancybox=True,fontsize='small')
	plt.xlabel('Frequency[kHz]')
	plt.ylabel('Power[dBm]')
	plt.grid(True)
	plt.ylim(ymax=30)
	plt.show()

def loaddata(dataname):
	'''ファイル名を引数にデータをロードし、返す
	また、データのプロットも行う(plotshowはしない)'''
	data=np.loadtxt(dataname)   #load text data as array
	r=(datax,datay)=(data[:,0],data[:,2])
	plt.plot(pnt2freq(datax),datay,'-',lw=0.1,color='k')    #測定データのプロット
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


	## __FITTING LOG__________________________
	indicateCondition='SNratio>5 and (0<waveWidth<100) and abs(freqFit-fittingFreqFit)<0.1'    #幅が0~100の間に入るとき(正常なガウシアン)　かつ　フィッティングされた周波数とフィッティングするはずの周波数のずれが0.1kHz以内
	logfile='./log/Log%s.log' % d.strftime("%Y%m%d")
	logprint('\n# %s\n# Filename: %s \n# Dataname: %s \n# Indicate condition: %s' % (d.strftime("%Y-%m-%d %H:%M:%S"),__file__,dataname,indicateCondition))   #ログファイルに時刻を打ち込む




	rtnDict={}
	for freqFit in freqWave+freqCarrier:   #freqWaveの周波数を片っ端からfit
		signaldiv=datay[freq2pnt(freqFit)]-yy
		if signaldiv>5:    #SN比が5以上ならfittingする
			print('%skHz S/N might be about'% freqFit,signaldiv,'\nFit now...' )
			## __FIT__________________________
			fitrange=0.2
			dataxRange=datax[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]   #±200Hzをフィッティングする
			datayRange=datay[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]
			fitresult=[fity,fitSN,fittingFreqFit,waveWidth]=list(gaussfit(dataxRange,datayRange,freqFit))
			SNratio=fitSN if abs(fitSN-signaldiv)<10 else signaldiv    #SNratioはフィッティングの値と測定値の差が10に収まればフィッティングのSN(fitSN)、そうでなければ測定値(signaldiv)を返す
			if eval(indicateCondition) :   #indicateConditionにマッチしたウェーブだけをプロットする
				print('\tOK! Plot as fit data...')
				plt.plot(pnt2freq(datax),fity,'-',lw=2,label=str(freqFit)+"kHz")   #fitting結果のプロット
				rtnDict[str(freqFit)+'kHz']=SNratio  #周波数をキー、SN比を値にしてfittngDictへ入れる
			else : print('\tNG! Wave is too broad, narrow or out of range...')
			print('\tS/N=',SNratio,'waveWidth=',waveWidth)
			logprint("Wave fitting %s : %s" % (str(freqFit), fitresult[1:4]))   # fitting結果を書き込む
		else : print('%skHz S/N might be about' % freqFit,signaldiv,'pass to fit...')


	outData={}
	import os
	filebasename=os.path.basename(dataname)[:-4]
	outData[d.strptime(filebasename,'%Y%m%d_%H%M%S')]=rtnDict  #ファイル名(=タイムスタンプ)をキーに、fittngDictを値にoutDataへ入れる
	print('\nFitting Result\n',outData)

	plotshowing(filebasename)

	return outData







def plotfit(x,y,mu):
	plt.plot(pnt2freq(x),list(gaussfit(x,y,mu))[0],'-',lw=2,label=str(mu)+"kHz")   #fitting結果のプロット



def SNSearch(dataname,freqWave,freqCarrier):
	(datax,datay)=loaddata(dataname)
	yy=stats.scoreatpercentile(datay, 25)	#fix at 1/4median


	## __FITTING LOG__________________________
	indicateCondition='SNratio>5'    #幅が0~100の間に入るとき(正常なガウシアン)　かつ　フィッティングされた周波数とフィッティングするはずの周波数のずれが0.1kHz以内
	logprint('\n# %s\n# Filename: %s.%s \n# Dataname: %s \n# Indicate condition: %s' % (d.strftime("%Y-%m-%d %H:%M:%S"),__file__,SNSearch,dataname,indicateCondition))   #ログファイルに時刻を打ち込む


	rtnDict={}
	for freqFit in freqWave+freqCarrier:   #freqWaveの周波数を片っ端からfit
		SNratio=datay[freq2pnt(freqFit)]-yy
		if eval(indicateCondition):    #SN比が5以上ならウェーブとみなす
			print('\tOK! Plot as fit data...')
			fitrange=0.2
			dataxRange=datax[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]   #±200Hzをフィッティングする
			datayRange=datay[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]

			# plotfit(dataxRange,datayRange,freqFit)
			rtnDict[str(freqFit)+'kHz']=SNratio  #周波数をキー、SN比を値にしてfittngDictへ入れる
		else : print('\tNG! Wave is too weak...')
		logprint("SNratio %skHz : %s" % (str(freqFit), SNratio))   # fitting結果を書き込む

	outData={}
	import os
	filebasename=os.path.basename(dataname)[:-4]
	outData[d.strptime(filebasename,'%Y%m%d_%H%M%S')]=rtnDict  #ファイル名(=タイムスタンプ)をキーに、fittngDictを値にoutDataへ入れる
	logprint('\nResult\n%s'% outData)
	# plotshowing(filebasename)
	return outData




def PowerSearch(dataname,freqWave,freqCarrier):
	(datax,datay)=loaddata(dataname)
	yy=stats.scoreatpercentile(datay, 25)	#fix at 1/4median


	## __FITTING LOG__________________________
	indicateCondition='SNratio>5'    #幅が0~100の間に入るとき(正常なガウシアン)　かつ　フィッティングされた周波数とフィッティングするはずの周波数のずれが0.1kHz以内
	logprint('\n# %s\n# Filename: %s.%s \n# Dataname: %s \n# Indicate condition: %s' % (d.strftime("%Y-%m-%d %H:%M:%S"),__file__,SNSearch,dataname,indicateCondition))   #ログファイルに時刻を打ち込む


	rtnDict={}
	for freqFit in freqWave+freqCarrier:   #freqWaveの周波数を片っ端からfit
		SNratio=datay[freq2pnt(freqFit)]-yy
		power=datay[freq2pnt(freqFit)]
		if eval(indicateCondition):    #SN比が5以上ならウェーブとみなす
			print('\tOK! Plot as fit data...')
			fitrange=0.2
			dataxRange=datax[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]   #±200Hzをフィッティングする
			datayRange=datay[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]

			# plotfit(dataxRange,datayRange,freqFit)
			rtnDict[str(freqFit)+'kHz']=power  #周波数をキー、SN比を値にしてfittngDictへ入れる
		else : print('\tNG! Wave is too weak...')
		logprint("power %skHz : %s" % (str(freqFit), power))   # fitting結果を書き込む

	outData={}
	import os
	filebasename=os.path.basename(dataname)[:-4]
	outData[d.strptime(filebasename,'%Y%m%d_%H%M%S')]=rtnDict  #ファイル名(=タイムスタンプ)をキーに、fittngDictを値にoutDataへ入れる
	logprint('\nResult\n%s'% outData)
	# plotshowing(filebasename)
	return outData



# '''
# TEST
# '''
# import confidential as co
# a=co.rootroot()+'20160112_132741.txt'
# b=co.freqWave
# c=co.freqCarrier
# fitting(a,b,c)