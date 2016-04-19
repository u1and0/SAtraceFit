'''fitting_151216.py ver0.1
データをテキスト形式で読み込みdataにリストとして読み込み
freqで指定した周波数の分だけfittingを行い
データとフィッティング曲線をプロットする
'''

import numpy as np
from scipy import stats
from scipy import optimize
import matplotlib.pyplot as plt







## __DATA__________________________
data=np.loadtxt('C:/home/gnuplot/SAout/151201/rawdata/trace/20151201_002344.txt')   #load text data as array
# data=np.loadtxt('C:/home/gnuplot/peaksearch/20151216_112356.txt')   #load text data as array
# data=np.loadtxt('./rawdata/banana.dat')   #load text data as array

datax=data[:,0]   #各リストの0番目をdataxに代入
datay=data[:,2]



## __FORMULA__________________________
def freq2pnt(x):
	return (x*1000-22000)/4
def pnt2freq(x):
	return (x*4+22000)/1000
def func(x,aa,mu,si):	#fitting function
	return aa*np.exp(-(x-mu)**2/2/si**2)+yy
yy=stats.scoreatpercentile(datay, 25)	#fix at 1/4median



## __FITTING__________________________
freqWave=[22.2,23.4,24.0,24.25,24.8]
freqCarrier=[23.0,24.1,24.5,25.0,25.1,25.2,25.5]
freqList=freqWave+freqCarrier
for freq in freqList:
	parameter_initial=np.array([0.0,freq2pnt(freq),0.3])    #aa,mu,si



	paramater_optimal, covariance = optimize.curve_fit(func, datax, datay, p0=parameter_initial)
	print("paramater"+str(freq)+" = ", paramater_optimal)
	fity= func(datax,paramater_optimal[0],paramater_optimal[1],paramater_optimal[2])




## __PLOT__________________________
	plt.plot(pnt2freq(datax),datay,'o',ms=1)
	# if(1<paramater_optimal[2]<100):
	plt.plot(pnt2freq(datax),fity,'-',lw=2,label=str(freq)+"kHz")
# plt.legend(bbox_to_anchor=(1.3,1.4))
plt.legend(loc='best',fancybox=True)
plt.xlabel('Frequency[kHz]')
plt.ylabel('Power[dBm]')
plt.grid(True)
plt.show()