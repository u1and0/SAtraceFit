'''
fittingDiv.py ver0.3.4

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

<UPDATE0.3.4>
関数化
ディクショナリ in ディクショナリ形式で出力

<PLAN>
# dataname=rawdata_directory+'\\'+'20151201_234856.txt'    #←バグ出るデータ
																#maxfev=800(default value)だとハンチング
																# 無視して先へ進みたいがどうすれば。。。
CSVreaderで読み込んだデータと混ぜ合わせる>>>csv_dict_test.py参照
'''

import numpy as np
from scipy import stats
from scipy import optimize
import matplotlib.pyplot as plt
import sys
import datetime
# import glob


def fitting(rawdata_directory,filebasename):
	dataname=rawdata_directory+'\\'+filebasename+'.txt'
	## __DATA__________________________
	# data=np.loadtxt('C:/home/gnuplot/peaksearch/20151216_112356.txt')   #load text data as array
	# dataname=rawdata_directory+'\\'+'20151201_234856.txt'    #←バグ出るデータ
																	#maxfev=800(default value)だとハンチング
																	# 無視して先へ進みたいがどうすれば。。。
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





	## __PLOT__________________________
	plt.plot(pnt2freq(datax),datay,'-',lw=0.1,color='k')   #測定データのプロット




	## __FITTING__________________________
	freqWave=[22.2,23.4,24.0,24.25,24.8]   #帯域持った周波数
	freqWave+=[23.0,24.1,24.5,25.0,25.1,25.2,25.5]   #キャリアのみの周波数



	## __FITTING LOG__________________________
	indicateCondition='(10<paramater_optimal[2]<100 and paramater_optimal[0]>0) or (0<paramater_optimal[2]<1 and paramater_optimal[0]>10)'
	d = datetime.datetime.today()

	sys.stdout=open("./FittingLog.txt", "a")   #fittingLogに書き込む準備
	print('\n#',d.strftime("%Y-%m-%d %H:%M:%S"))
	logmsg='# Filename: %s \n# Dataname: %s \n# Indicate condition: %s' % (__file__,dataname,indicateCondition)
	print(logmsg)
	sys.stdout.close()
	sys.stdout = sys.__stdout__   #標準出力に書き込む
	print(logmsg)


	fittingDict={}
	for freqFit in freqWave:   #freqWaveの周波数を片っ端からfit
	## __FITTING RANGE__________________________
		fitrange=0.2
		dataxRange=datax[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]
		datayRange=datay[freq2pnt(freqFit-fitrange):freq2pnt(freqFit+fitrange)]

		parameter_initial=np.array([0.0,freq2pnt(freqFit),0.3])    #aa,mu,si
		paramater_optimal, covariance = optimize.curve_fit(gauss, dataxRange, datayRange, p0=parameter_initial)   #±200Hzをフィッティングする
		fity= gauss(datax,paramater_optimal[0],paramater_optimal[1],paramater_optimal[2])   #fitting結果を反映したfinnting関数


	## __INDICATE CONDITION__________________________
		if eval(indicateCondition) :   #幅が0~100の間に入るとき(正常なガウシアン) または S/N比5以上のとき fittng結果をプロットする
			plt.plot(pnt2freq(datax),fity,'-',lw=2,label=str(freqFit)+"kHz")   #fitting結果のプロット

		## __FITTING LOG__________________________
			fittnglog="paramater%s = %s" % (str(freqFit), paramater_optimal)
			print(fittnglog)   #fitting結果の表示
			sys.stdout=open("./FittingLog.txt", "a")   #fittingLog.txtに書き込む準備
			print(fittnglog)
			# print("paramater"+str(freqFit)+" = ", paramater_optimal)
			sys.stdout.close()
			sys.stdout = sys.__stdout__
		## __OUTPUT__________________________
			fittingDict[str(freqFit)]=list(paramater_optimal)[0]  #周波数をキー、SN比を値にしてfittngDictへ入れる

	outData={}
	outData[d.strptime(filebasename,'%Y%m%d_%H%M%S')]=fittingDict  #ファイル名(=タイムスタンプ)をキーに、fittngDictを値にoutDataへ入れる
	print('\noutData=',outData)
	return outData





## __PLOT SSETTING__________________________
# plt.legend(loc='best',fancybox=True,fontsize='small')
# plt.xlabel('Frequency[kHz]')
# plt.ylabel('Power[dBm]')
# plt.grid(True)
# plt.ylim(ymax=30)
# plt.show()



'''TEST
rawdata_directory=('C:\\home\\gnuplot\\SAout\\151201\\rawdata\\trace')
filebasename='20151201_235900'
print(fitting(rawdata_directory,filebasename))
'''