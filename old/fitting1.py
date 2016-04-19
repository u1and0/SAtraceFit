import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt

## __DATA__________________________
data=np.loadtxt('./rawdata/banana.dat')   #load text data as array

datax=data[:,0]   #各リストの0番目をdataxに代入
datay=data[:,1]


## __FITTING__________________________
parameter_initial=np.array([0.0,0.0,0.3,0.0])    #aa,mu,si,yy
def func(x,aa,mu,si,yy):
	return aa*np.exp(-(x-mu)**2/2/si**2)+yy


paramater_optimal, covariance = scipy.optimize.curve_fit(func, datax, datay, p0=parameter_initial)
print("paramater =", paramater_optimal)




fity= func(datax,paramater_optimal[0],paramater_optimal[1],paramater_optimal[2],paramater_optimal[3])

plt.plot(datax,datay,'o',ms=3)
plt.plot(datax,fity,'-',lw=1)
plt.show()