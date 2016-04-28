'''
fittingDiv.py ver0.3.7

<INTRODUCTION>
タイムスタンプを引数にフィッティング結果を返すpy

<ACTION>
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

<UPDATE0.3.7>
fitting parameter の調整
Log書き込み関数"logout"作成
<PLAN>
'''

import numpy as np
from scipy import stats
from scipy import optimize
import matplotlib.pyplot as plt
import sys


def fitting(rawdata_directory,filebasename,freqWave,*plotFlag):
	dataname=rawdata_directory+'\\'+filebasename+'.txt'
	## __DATA__________________________
	data=np.loadtxt(dataname)   #load text data as array

	datax=data[:,0]   #各リストの0番目をdataxに代入
	datay=data[:,2]

	## __FORMULA__________________________
	def freq2pnt(x):
		return (x*1000-22000)/4
	def pnt2freq(x):
		return (x*4+22000)/1000
	yy=stats.scoreatpercentile(datay, 25)	#fix at 1/4median
	def gauss(x,aa,mu,si):	#fitting function
		return aa*np.exp(-(x-mu)**2/2/si**2)+yy

	def logout(file,text):
		sys.stdout=open(file, "a")   #fileに上書き(a)で書き込む
		print(text)
		sys.stdout.close()
		sys.stdout = sys.__stdout__   #標準出力に書き込む
		print(text)


	## __PLOT__________________________
	plt.plot(pnt2freq(datax),datay,'-',lw=0.1,color='k')   #測定データのプロット


	## __FITTING LOG__________________________
	indicateCondition='(10<waveWidth<100 and SNratio>5) or (0<waveWidth<1 and SNratio>10)'    #幅が0~100の間に入るとき(正常なガウシアン) または S/N比5以上のとき fittng結果をプロットする
	# indicateCondition='(10<waveWidth<100 and SNratio>0) or (0<waveWidth<1 and SNratio>10)'
	import datetime
	d = datetime.datetime.today()
	logout('./FittingLog.txt','\n# %s\n# Filename: %s \n# Dataname: %s \n# Indicate condition: %s' % (d.strftime("%Y-%m-%d %H:%M:%S"),__file__,dataname,indicateCondition))

	fittingDict={}
	for freqFit in freqWave:   #freqWaveの周波数を片っ端からfit
	## __FITTING RANGE__________________________
		fitrange=0.2
		dataxRange=datax[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]
		datayRange=datay[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]

		parameter_initial=[0,freq2pnt(freqFit),0.3]    #aa,mu,si
		# parameter_initial=np.array([100,freq2pnt(freqFit),100])    #aa,mu,si
		paramater_optimal, covariance = optimize.curve_fit(gauss, dataxRange, datayRange, p0=parameter_initial, maxfev = 100000000)   #±200Hzをフィッティングする
		fity= gauss(datax,float(paramater_optimal[0]),float(paramater_optimal[1]),float(paramater_optimal[2]))   #fitting結果を反映したfinnting関数
		# fity= gauss(datax,paramater_optimal[0],paramater_optimal[1],paramater_optimal[2])   #fitting結果を反映したfinnting関数
		SNratio=paramater_optimal[0]
		waveWidth=abs(paramater_optimal[2])

	## __INDICATE CONDITION__________________________
		if eval(indicateCondition) :   #indicateConditionにマッチしたウェーブだけをプロットする
			plt.plot(pnt2freq(datax),fity,'-',lw=2,label=str(freqFit)+"kHz")   #fitting結果のプロット

		## __FITTING LOG__________________________
			logout('./FittingLog.txt',"paramater%s = %s" % (str(freqFit), paramater_optimal))
		## __OUTPUT__________________________
			fittingDict[str(freqFit)+'kHz']=list(paramater_optimal)[0]  #周波数をキー、SN比を値にしてfittngDictへ入れる

	outData={}
	outData[d.strptime(filebasename,'%Y%m%d_%H%M%S')]=fittingDict  #ファイル名(=タイムスタンプ)をキーに、fittngDictを値にoutDataへ入れる
	print('\nFitting Result\n',outData)







# TEST
# rawdata_directory=('C:\\home\\gnuplot\\SAout\\151201\\rawdata\\trace')
# filebasename='20151201_000344'
# freqWave=[22.2,23.4,24.0,24.25,24.8]   #帯域持った周波数
# freqWave+=[23.0,24.1,24.5,25.0,25.1,25.2,25.5]   #キャリアのみの周波数
# fitting(rawdata_directory,filebasename,freqWave)

##__PLOT SSETTING__________________________
	if plotFlag:
		plt.legend(loc='best',fancybox=True,fontsize='small')
		plt.xlabel('Frequency[kHz]')
		plt.ylabel('Power[dBm]')
		plt.grid(True)
		plt.ylim(ymax=30)
		plt.show()





	return outData