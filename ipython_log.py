# IPython log file
# 2016/11/04 16:02:27

noisef = -0.5
def gauss(x, *param):  # fitting function
    aa, mu, si = param
    return aa * np.exp(-(x - mu)**2 / 2 / si**2) + noisef
n = 1001
xx = np.linspace(22, 26, n)
aa, mu, si = 1, 23, 0.1
g = gauss(xx, aa, mu, si)
gnoise = g + 0.1 * np.random.randn(n)
plt.plot(xx, g)
plt.plot(xx, gnoise, '.')
noisef = 0.5
# n=1001
# xx=np.linspace(22,26,n)
# aa,mu,si=1,23,0.1
# g=gauss(xx,aa,mu,si)
# gnoise=g+0.1*np.random.randn(n)
# plt.plot(xx, g)
# plt.plot(xx,gnoise, '.')
##
plt.plot(xx, g)
plt.plot(xx, gnoise, '.')
plt.title('ガウシアン　ノイズ発生')
from scipy.optimize import curve_fit
# get_ipython().magic('pinfo curve_fit')
# get_ipython().magic('pinfo gnoise')
curve_fit(gauss, xx, g, (aa, mu, si))
(aa_, mu_, si_), _ = curve_fit(gauss, xx, g, (aa, mu, si))
yfit = gauss(xx, aa_, mu_, si_)
plt.plot(xx, gnoise, '.')
plt.plot(xx, yfit, '-')
# fittingできた


# df=pd.DataFrame([g+np.random.rand()*np.random.randn(n for _ in range(10)]),index=xx)
# df=pd.DataFrame([g+np.random.rand()*np.random.randn(n for _ in range(10)]),index=[xx])
# df=pd.DataFrame([g+np.random.rand()*np.random.randn(n) for _ in range(10)]),index=xx)
# df=pd.DataFrame([g+np.random.rand()*np.random.randn(n) for _ in range(10)]),index=[xx])
# df=pd.DataFrame([g+np.random.rand()*np.random.randn(n) for _ in range(10)]))
df = pd.DataFrame([g + np.random.rand() * np.random.randn(n) for _ in range(10)])
df
df.plot('.')
# get_ipython().magic('pinfo df.plot')
# get_ipython().magic('pinfo plt.plot')
df.plot(style='.')
df[1].plot(style='.')
df
df.T.plot(style='.')
get_ipython().magic('log_start')
get_ipython().magic('logstart')
get_ipython().magic('logstop')
