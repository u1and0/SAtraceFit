
# coding: utf-8

# # 自作ガウシアン

# In[4]:

def gauss(x, a, mu, si):
    """
    a: 最大値
    mu: 位置
    si: 線幅
    noisef: 最低値
    """
    return a * np.exp(-(x - mu)**2 / 2 / si**2)


# In[5]:

f = lambda x, a, mu, si, nf: gauss(x, a, mu, si) + nf 


# In[6]:

nf=0.5
n=1001
x = np.linspace(0,100,n)
a, mu, si = 1, 50, 1


# In[7]:

g= f(x, a, mu, si, nf); g


# In[8]:

plt.plot(x, g)


# ## 自作ガウシアンじゃなくてscipy.stats.normを使うべきでは

# In[9]:

from  scipy.stats import norm


# In[10]:

z=norm.pdf(x, loc=50, scale=1)-0.5; z


# In[11]:

plt.plot(x,z)


# In[37]:

a, mu, si=1, 50, 1
df=pd.DataFrame({'norm': a*norm.pdf(x, loc=mu, scale=si)+nf,
                 			'gauss': gauss(x, a, mu, si, nf)})
df.plot(style=['-', '--'])


# ## norm vs my_gauss
# normでも自作gaussでも中でnp使っているんで実行速度あんま変わらないだろうとテスト

# In[38]:

get_ipython().magic('timeit gauss(x, a, mu, si)')


# In[21]:

get_ipython().magic('timeit norm.pdf(x, loc=50, scale=1)-0.5')


# 自作ガウスのほうが早い…！

# ## ガウシアンに沿ってノイズを作る
# 
# ということで自作のガウシアンを使っていきます。

# In[13]:

g = f(x, a, mu, si, 0.5)
gnoise = g + 0.1 * g * np.random.randn(n)


# ノイズを発生させる

# In[14]:

plt.plot(x, gnoise, '-')
plt.plot(x, g,'b-' )


# ## カーブフィッティングをかけて、ノイズをフィッティングする
# 
# gからgnoiseを導き出したのだけれども、ここで急にgを未知の関数とみなしてしまう。
# 今あなたはgnoiseだけを知っていて、gのような関数を得たいとき、どうするか。
# 
# こういう時はカーブフィットを取る。
# scipy.optimizeからcurve_fitをインポートしてくる。

# In[15]:

from scipy.optimize import curve_fit
from scipy.optimize import leastsq
from scipy.optimize import least_squares


# 次にフィッティングパラメータを定める。

# In[160]:

(a_, mu_, si_), _ = leastsq(gauss, x, gnoise, p0=(a, mu, si))
yfit = gauss(x, a_, mu_, si_)  # フィッティングにより導き出されたa,mu,siを代入
print('元パラメータ:%s\nフィッティングで求めたパラメータ: %s' % ((a, mu , si), (a_, mu_, si_)))


# In[22]:

(a_, mu_, si_), _ = curve_fit(gauss, x, gnoise, p0=(a, mu, si))
yfit = f(x, a_, mu_, si_, nf)  # フィッティングにより導き出されたa,mu,siを代入
print('元パラメータ:%s\nフィッティングで求めたパラメータ: %s' % ((a, mu , si), (a_, mu_, si_)))


# In[23]:

_


# curve_fitの戻り値アンダーバーは共分散？
# 
#     pcov : 2d array
#     The estimated covariance of popt. The diagonals provide the variance
#     of the parameter estimate. To compute one standard deviation errors
#     on the parameters use ``perr = np.sqrt(np.diag(pcov))``.

# In[24]:

plt.plot(x, gnoise, 'r-')
plt.plot(x, yfit, 'b-') 


# さっきと同じグラフに見えるが、描いているのはgではなくyfitであることに注意
# 
# 同じグラフに見えるということはフィッティングできたということ。

# # scipy.stats.normを使った場合

# ## ガウシアンに沿ってノイズを作る

# In[19]:

from  scipy.stats import norm


# In[53]:

n=1001
xx = np.linspace(0,100,n)
aa, mu, si = 5, 50, 1


# In[57]:

def gauss2(x, a, mu, si):
    return a*norm.pdf(x, loc=mu, scale=si)-noisef


# In[58]:

g = gauss2(xx, aa, mu, si)
gnoise = g + 0.1 * np.random.randn(n)


# In[59]:

plt.plot(xx, gnoise, '.-')
plt.plot(xx, g,'r-' )


# ## カーブフィッティングをかけて、ノイズをフィッティングする
# 
# gからgnoiseを導き出したのだけれども、ここで急にgを未知の関数とみなしてしまう。
# 今あなたはgnoiseだけを知っていて、gのような関数を得たいとき、どうするか。

# In[66]:

from scipy.optimize import curve_fit
(aa_, mu_, si_), _ = curve_fit(gauss2, xx, gnoise, (aa, mu, si))
yfit = gauss2(xx,aa_, mu_, si_)


# In[67]:

plt.plot(xx, gnoise, '.-')
plt.plot(xx, yfit, 'r-')  # 描いているのはgではなく、yfitであることに注意


# ちゃんとフィッティングできた。

# # 自作ガウスをノイズのあるデータフレームにcarve_fitをapply

# ## ランダムデータフレームの作成

# In[6]:

r=np.random


# いっぱい使うから乱数生成をrに縮めちゃう

# In[7]:

g = gauss(x, a=r.rand(), mu=10*1, si=10*r.rand(), noisef=nf*r.rand())
plt.plot(x, g)


# ランダムな値を使って発生させたガウシアン

# In[8]:

get_ipython().run_cell_magic('timeit', '', 'df = pd.DataFrame([], index=range(1000))\nfor i in np.arange(min(x), max(x), 10):\n    g = gauss(x, a=r.rand(), mu=i, si=10*r.rand(), noisef=nf)\n    df[i] = pd.DataFrame(g)')


# まず思いつくforループ

# In[12]:

get_ipython().run_cell_magic('timeit', '', 'garray = np.array([gauss(x, a=r.rand(), mu=i, si=10*r.rand(), noisef=nf)\n                    for i in np.arange(min(x), max(x), 10)]).T\ndf = pd.DataFrame(garray)')


# リスト内包表記を使うことでより高速

# In[81]:

get_ipython().run_cell_magic('timeit', '', 'xa = np.tile(x, (10,1))\naa = abs(r.randn(10))\nmua = np.arange(min(x), max(x), 10)\nsia = 10 * abs(r.randn(10))\n\ndf = pd.DataFrame(gauss(xa.T, aa, mua, sia, nf))')


# np.arrayで変数作るともっともっと高速

# In[82]:

gdf.plot()


# ## 足し合わせた複数の波があるdf

# 様々な形のガウシアン。
# 
# ノイズフロアは一定にした。
# 
# こいつらにノイズを載せる。

# ## ランダムデータフレームにノイズのせてサンプルデータ作成

# In[89]:

noisedf =df + df * 0.05 * r.randn(*df.shape)
noisedf.plot()


# 5%のノイズをのせた。
# `np.randn(*df.shape)`でデータフレームと同じ行列を持ったランダムデータフレームを生成させている。
# スターを`df.shape`の前につけてタプルを展開して`randn`に渡す。

# In[90]:

sumdf = noisedf.sum(axis=1)
sumdf.plot()


# In[85]:

sumdf


# indexはそのままにカラムをすべて足す。この中でindexいくつの位置にガウシアンが立つかを調べる。

# ## 複数のランダムウェーブを生成

# In[133]:

def waves(seed: int=np.random.randint(100)):
    """ランダムノイズを発生させたウェーブを作成する
    引数: seed: ランダムステートを初期化する整数。デフォルトでseedをランダムに発生させる
    戻り値: noisedf.sum(1): pd.Series型"""
    r = np.random
    r.seed(seed)  # ランダム初期化
    xa = np.tile(x, (10,1))
    aa = abs(r.randn(10))
    mua = np.arange(min(x), max(x), 10)
    sia = 10 * abs(r.randn(10))

    df = pd.DataFrame(gauss(xa.T, aa, mua, sia, nf))
    noisedf = df + df * 0.05 * r.randn(*df.shape)
    return noisedf.sum(1)
waves().plot()


# In[147]:

get_ipython().magic('timeit waves()')


# In[148]:

df = pd.DataFrame([waves(i) for i in range(10)]); df


# # データフレームに一斉にフィッティングかける
# 一番やりたかったこと　ここから。

# In[242]:

param = (a, mu, si) = 5, 300, 3
param


# パラメータ再設定

# ## 試しに波を一つ選んでfitting

# In[254]:

def choice(array, center, span):
    """特定の範囲を抜き出す
    引数: 
        array: 抜き出し対象のarrayっぽいの(arraylike)
        center: 抜き出し中央(float)
        span: 抜き出しスパン(float)
    戻り値:
        rarray:
    """
    x1 = int(center - span / 2)
    x2 = int(center + span / 2)
    return array[x1:x2]


# In[256]:

ch = (300, 300)  # 中央値300でスパン300で取り出したい
fitx, fity = choice(sumdf.index, *ch), choice(sumdf, *ch)
plt.plot(fitx, fity)


# In[275]:

popt, _pcov = curve_fit(gauss, fitx, fity, p0=param)
print('a, mu, si = ', popt)


# fittingの結果

# In[274]:

gg = gauss(sumdf.index,*popt)


# In[273]:

sumdf.plot()
plt.plot(fitx, choice(gg, *ch), 'k-')


# fittingの結果を用いてガウシアン描いてみる。

# ## 連続的にfitting

# In[303]:

fitting_list = (300, 500, 600, 700)  # 目測どのあたりに波があるか
fitdf=pd.DataFrame(np.empty(1000))
for i in fitting_list:
    param = (a, mu, si) = 5, i, 3
    ch = (i, 300)
    fitx, fity = choice(sumdf.index, *ch), choice(sumdf, *ch)
    popt, _pcov = curve_fit(gauss, fitx, fity, p0=param, maxfev = 10000)
    gg = gauss(sumdf.index,*popt)
    fitdf[i] = pd.DataFrame(choice(gg, *ch), index=fitx)
del fitdf[0]


# In[323]:

fitdf['sumdf'] = sumdf
fitdf.plot(style = ['-', '-', '-', '-', '.'])


# In[152]:

fit=lambda df: curve_fit(gauss, x[:-1], df['0.0'], p0=(a, mu, si))


# In[231]:

sumdf.apply(fit)


# In[ ]:




# In[211]:

Bfit = noisedf.T
Bfit.index=pd.date_range('20161111', freq='H', periods=10)
Bfit


# 実際fittingかけたいデータフレームはindexが時間、カラムが

# ___

# In[2]:

import sys
sys.path.append('../')


# In[4]:

from fitclass import *


# In[5]:

# giving initial parameters
mu = Parameter(7)
sigma = Parameter(3)
height = Parameter(5)


# In[13]:

# define your function:
def f(x, h=height(), mu=mu(), si=sigma()): return h * np.exp(-((x-mu)/si)**2)


# In[16]:

# fit! (given that data is an array with the data to fit)
data = 10*np.exp(-np.linspace(0, 10, 100)**2) + np.random.rand(100)
fitp, _ = fit(f, [mu, sigma, height], data); fitp


# In[21]:

plt.plot(data)
plt.plot(f(data, *fitp))


# In[ ]:



