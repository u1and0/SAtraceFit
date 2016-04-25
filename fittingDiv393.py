'''
## fittingDiv.py ver0.3.9.3

__UPDATE0.3.9.3__
failebasenameではなくglobで拾われるフルパスに変更


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


def fitting(dataname,freqWave,freqCarrier):
	## __DATA__________________________
	data=np.loadtxt(dataname)   #load text data as array
	if not data:
		break

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
		'''
		引数textに入った文字列をfileに書き込んで、標準出力にも書き込む
		'''
		sys.stdout=open(file, "a")   #fileに上書き(a)で書き込む
		print(text)
		sys.stdout.close()
		sys.stdout = sys.__stdout__   #標準出力に書き込む
		print(text)

	def gaussfit(datax,datay,freqFit):
		fitrange=0.2
		dataxRange=datax[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]   #±200Hzをフィッティングする
		datayRange=datay[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]

		parameter_initial=[0,freq2pnt(freqFit),0.3]    #fitting初期値aa,mu,si
		paramater_optimal, covariance = optimize.curve_fit(gauss, dataxRange, datayRange, p0=parameter_initial, maxfev = 100000000)
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

	## __PLOT__________________________
	##測定データのプロット
	plt.plot(pnt2freq(datax),datay,'-',lw=0.1,color='k')


	## __FITTING LOG__________________________
	indicateCondition='(0<waveWidth<100) and abs(freqFit-fittingFreqFit)<0.1'    #幅が0~100の間に入るとき(正常なガウシアン)　かつ　フィッティングされた周波数とフィッティングするはずの周波数のずれが0.1kHz以内
	import datetime
	d = datetime.datetime.today()
	logfile='./log/Log%s.log' % d.strftime("%Y%m%d")
	logout(logfile,'\n# %s\n# Filename: %s \n# Dataname: %s \n# Indicate condition: %s' % (d.strftime("%Y-%m-%d %H:%M:%S"),__file__,dataname,indicateCondition))   #ログファイルに時刻を打ち込む




	fittingDict={}
	for freqFit in freqWave:   #freqWaveの周波数を片っ端からfit
		signaldiv=datay[freq2pnt(freqFit)]-yy
		if signaldiv>5:    #SN比が5以上ならfittingする
			print(freqFit,'kHz S/N might be about',signaldiv,'\nFit now...')
			## __FIT__________________________
			ttt=[fity,SNratio,fittingFreqFit,waveWidth]=list(gaussfit(datax,datay,freqFit))


			## __INDICATE CONDITION__________________________
			if eval(indicateCondition) :   #indicateConditionにマッチしたウェーブだけをプロットする
				plt.plot(pnt2freq(datax),fity,'-',lw=2,label=str(freqFit)+"kHz")   #fitting結果のプロット

				## __FITTING LOG__________________________
				print('\tOK! Plot as fit data...')
				## __OUTPUT__________________________
				fittingDict[str(freqFit)+'kHz']=SNratio  #周波数をキー、SN比を値にしてfittngDictへ入れる
			else : print('\tNG! Wave is too broad, narrow or out of range...')
			print('\tS/N=',SNratio,'waveWidth=',waveWidth)
			logout(logfile,"Wave fitting %s : %s" % (str(freqFit), ttt[1:4]))   # fitting結果を書き込む
		else : print(freqFit,'kHz S/N might be about',signaldiv,'pass to fit...')






	for freqFit in freqCarrier:   #freqCarrierの周波数を片っ端からfit
		signaldiv=datay[freq2pnt(freqFit)]-yy
		if signaldiv>10:    #SN10以上で信号ありとする
			print(freqFit,'kHz S/N might be about',signaldiv,'\nFit now...')
			## __FIT__________________________
			# グラフ表示するだけ。csvには吐き出さない
			ttt=[fity,SNratio,fittingFreqFit,waveWidth]=list(gaussfit(datax,datay,freqFit))
			plt.plot(pnt2freq(datax),fity,'-',lw=2,label=str(freqFit)+"kHz")   #fitting結果のプロット

			## __OUTPUT__________________________
			fittingDict[str(freqFit)+'kHz']=signaldiv  #周波数をキー、SN比を値にしてfittngDictへ入れる
			print('\tS/N=',signaldiv)
			logout(logfile,"Carrier  nofitting %s : %s" % (str(freqFit), [signaldiv,freqFit,'NoWidth']))   # S/Nを書き込む
		else : print(freqFit,'kHz S/N=',signaldiv,'pass to fit...')





				# fittingDict[str(freqFit)+'kHz']=SNratio  #周波数をキー、SN比を値にしてfittngDictへ入れる


	outData={}
	import globname as g
	import os
	outData[d.strptime(os.path.basename(dataname)[:-4],'%Y%m%d_%H%M%S')]=fittingDict  #ファイル名(=タイムスタンプ)をキーに、fittngDictを値にoutDataへ入れる
	print('\nFitting Result\n',outData)





##__PLOT SSETTING__________________________
	# plt.title(d.strptime(filebasename,'%Y%m%d_%H%M%S'))
	# plt.legend(loc='best',fancybox=True,fontsize='small')
	# plt.xlabel('Frequency[kHz]')
	# plt.ylabel('Power[dBm]')
	# plt.grid(True)
	# plt.ylim(ymax=30)
	# plt.show()



	return outData










'''
TEST
rawdata_directory=('C:\\home\\gnuplot\\SAout\\151201\\rawdata\\trace')
filebasename='20151201_000344'
freqWave=[22.2,23.4,24.0,24.25,24.8]   #帯域持った周波数
freqWave+=[23.0,24.1,24.5,25.0,25.1,25.2,25.5]   #キャリアのみの周波数
fitting(rawdata_directory,filebasename,freqWave)
'''
