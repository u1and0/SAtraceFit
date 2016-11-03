# IPython log file 
# 2016/11/04 6:32:51
# aa,mu,si=1,2,3
# xx=np.linspace(22,26,1001)
# gauss(xx,aa,mu,si)
# noisef=-0.5
# gauss(xx,aa,mu,si)
# g=gauss(xx,aa,mu,si)
# plt.plot(xx, g)
# aa,mu,si=1,23,50
# g=gauss(xx,aa,mu,si)
# plt.plot(xx, g)
# aa,mu,si=1,23,5
# plt.plot(xx, g)
# g=gauss(xx,aa,mu,si)
# plt.plot(xx, g)
# aa,mu,si=1,23,1
# plt.plot(xx, g)
# g=gauss(xx,aa,mu,si)
# p
# plt.plot(xx, g)
# aa,mu,si=1,23,0.1
# g=gauss(xx,aa,mu,si)
# plt.plot(xx, g)
# n=1001gnoise=g+0.2*np.random.randn(n)
# n=1001
# gnoise=g+0.2*np.random.randn(n)
# gnoise
# plt.plot(xx, g)
# plt.plot(xx,gnoise)
# plt.plot(xx, g)
# plt.plot(xx,gnoise, '.')
n=1001
xx=np.linspace(22,26,n)
aa,mu,si=1,23,0.1
g=gauss(xx,aa,mu,si)
gnoise=g+0.1*np.random.randn(n)
plt.plot(xx, g)
plt.plot(xx,gnoise, '.')
noisef=0.5
# n=1001
# xx=np.linspace(22,26,n)
# aa,mu,si=1,23,0.1
# g=gauss(xx,aa,mu,si)
# gnoise=g+0.1*np.random.randn(n)
# plt.plot(xx, g)
# plt.plot(xx,gnoise, '.')
##
plt.plot(xx, g)
plt.plot(xx,gnoise, '.')
plt.title('ガウシアン　ノイズ発生')
from scipy.optimize import curve_fit
# get_ipython().magic('pinfo curve_fit')
# get_ipython().magic('pinfo gnoise')
curve_fit(gauss, xx, g, (aa,mu,si))
(aa_, mu_, si_), _=curve_fit(gauss, xx, g, (aa,mu,si))
yfit=gauss(xx, aa_, mu_, si_)
plt.plot(xx, gnoise, '.')
plt.plot(xx, yfit, '-')
# fittingできた




# df=pd.DataFrame([g+np.random.rand()*np.random.randn(n for _ in range(10)]),index=xx)
# df=pd.DataFrame([g+np.random.rand()*np.random.randn(n for _ in range(10)]),index=[xx])
# df=pd.DataFrame([g+np.random.rand()*np.random.randn(n) for _ in range(10)]),index=xx)
# df=pd.DataFrame([g+np.random.rand()*np.random.randn(n) for _ in range(10)]),index=[xx])
# df=pd.DataFrame([g+np.random.rand()*np.random.randn(n) for _ in range(10)]))
df=pd.DataFrame([g+np.random.rand()*np.random.randn(n) for _ in range(10)])
df
df.plot('.')
# get_ipython().magic('pinfo df.plot')
# get_ipython().magic('pinfo plt.plot')
df.plot(style='.')
df[1].plot(style='.')
df
df.T.plot(style='.')
