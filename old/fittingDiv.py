'''fittingDiv.py ver0.1
1. データをテキスト形式で読み込みdataにリストとして読み込み
2. freqで指定した周波数の分だけfittingを行い
3. データとフィッティング曲線をプロットする
4. fittingする
5. 表示するかしないか判断
6. プロットして表示
'''

import numpy as np
from scipy import stats
from scipy import optimize
import matplotlib.pyplot as plt
# import glob





## __DATA__________________________
# data=np.loadtxt('C:/home/gnuplot/peaksearch/20151216_112356.txt')   #load text data as array
rawdata_drectory=('C:\\home\\gnuplot\\SAout\\151201\\rawdata\\trace')   #load text data as array
dataname=rawdata_drectory+'\\20151201_005844.txt'
# np.loadtxt(data)
data=np.loadtxt(dataname)   #load text data as array
print(dataname,'\n',data)

datax=data[:,0]   #各リストの0番目をdataxに代入
datay=data[:,2]



## __FORMULA__________________________
def freq2pnt(x):
	return (x*1000-22000)/4
def pnt2freq(x):
	return (x*4+22000)/1000
yy=stats.scoreatpercentile(datay, 25)	#fix at 1/4median
def func(x,aa,mu,si):	#fitting function
	return aa*np.exp(-(x-mu)**2/2/si**2)+yy

def fittingResult():
	plt.plot(pnt2freq(datax),fity,'-',lw=2,label=str(freqFit)+"kHz")   #fitting結果のプロット
	print("paramater"+str(freqFit)+" = ", paramater_optimal)   #fitting結果の表示






## __PLOT__________________________
plt.plot(pnt2freq(datax),datay,'-',lw=0.1,color='k')   #測定データのプロット




## __FITTING__________________________
freqWave=[22.2,23.4,24.0,24.25,24.8]   #帯域持った周波数
freqWave+=[23.0,24.1,24.5,25.0,25.1,25.2,25.5]   #キャリアのみの周波数



for freqFit in freqWave:   #freqWaveの周波数において、
	rrange=0.2
	rrangeMinus=freq2pnt(freqFit-rrange)
	rrangePlus=freq2pnt(freqFit+rrange)
	dataxRange=datax[rrangeMinus:rrangePlus]
	datayRange=datay[rrangeMinus:rrangePlus]

	parameter_initial=np.array([0.0,freq2pnt(freqFit),0.3])    #aa,mu,si
	paramater_optimal, covariance = optimize.curve_fit(func, dataxRange, datayRange, p0=parameter_initial)   #±200Hzをフィッティングする
	fity= func(datax,paramater_optimal[0],paramater_optimal[1],paramater_optimal[2])   #fitting結果を反映したfinnting関数

## __INDICATE CONDITION__________________________
	if (1<paramater_optimal[2]<100 and paramater_optimal[0]>0) or paramater_optimal[0]>5:   #幅が0~100の間に入るとき(正常なガウシアン) または S/N比5以上のとき fittng結果をプロットする
		fittingResult()










## __PLOT SSETTING__________________________
# plt.legend(bbox_to_anchor=(1.3,1.4))
plt.legend(loc='best',fancybox=True)
plt.xlabel('Frequency[kHz]')
plt.ylabel('Power[dBm]')
plt.grid(True)
plt.show()