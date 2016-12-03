
# coding: utf-8

# # 自作ガウシアン

# In[1]:

def gauss(x, a, mu, si, nf):
    """
    a: 最大値
    mu: 位置
    si: 線幅
    noisef: 最低値
    """
    return a * np.exp(-(x - mu)**2 / 2 / si**2) + nf


# In[55]:

nf=0.5
n=1001
x = np.linspace(0,100,n)
a, mu, si = 1, 50, 1


# In[3]:

g= gauss(x, a, mu, si, nf); g


# In[4]:

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

# In[5]:

g = gauss(x, a, mu, si, 0.5)
gnoise = g + 0.1 * g * np.random.randn(n)


# In[6]:

plt.plot(x, gnoise, '-')
plt.plot(x, g,'b-' )


# ノイズを発生させる

# ## カーブフィッティングをかけて、ノイズをフィッティングする
# 
# gからgnoiseを導き出したのだけれども、ここで急にgを未知の関数とみなしてしまう。
# 今あなたはgnoiseだけを知っていて、gのような関数を得たいとき、どうするか。
# 
# こういう時はカーブフィットを取る。
# scipy.optimizeからcurve_fitをインポートしてくる。

# In[59]:

from scipy.optimize import curve_fit
from scipy.optimize import leastsq
from scipy.optimize import least_squares
from scipy.stats import scoreatpercentile


# 次にフィッティングパラメータを定める。

# In[56]:

(a_, mu_, si_, nf_), _ = curve_fit(gauss, x, gnoise, p0=(a, mu, si, nf))
yfit = gauss(x, a_, mu_, si_, nf)  # フィッティングにより導き出されたa,mu,siを代入
print('元パラメータ:%s\nフィッティングで求めたパラメータ: %s' % ((a, mu , si), (a_, mu_, si_)))


# In[28]:

_


# curve_fitの戻り値アンダーバーは共分散？
# 
#     pcov : 2d array
#     The estimated covariance of popt. The diagonals provide the variance
#     of the parameter estimate. To compute one standard deviation errors
#     on the parameters use ``perr = np.sqrt(np.diag(pcov))``.

# In[57]:

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

# In[12]:

r=np.random


# いっぱい使うから乱数生成をrに縮めちゃう

# In[13]:

g = gauss(x, a=r.rand(), mu=10*1, si=10*r.rand(), nf=nf*r.rand())
plt.plot(x, g)


# ランダムな値を使って発生させたガウシアン

# In[8]:

get_ipython().run_cell_magic('timeit', '', 'df = pd.DataFrame([], index=range(1000))\nfor i in np.arange(min(x), max(x), 10):\n    g = gauss(x, a=r.rand(), mu=i, si=10*r.rand(), noisef=nf)\n    df[i] = pd.DataFrame(g)')


# まず思いつくforループ

# In[12]:

get_ipython().run_cell_magic('timeit', '', 'garray = np.array([gauss(x, a=r.rand(), mu=i, si=10*r.rand(), noisef=nf)\n                    for i in np.arange(min(x), max(x), 10)]).T\ndf = pd.DataFrame(garray)')


# リスト内包表記を使うことでより高速

# In[14]:

get_ipython().run_cell_magic('timeit', '', 'xa = np.tile(x, (10,1))\naa = abs(r.randn(10))\nmua = np.arange(min(x), max(x), 10)\nsia = 10 * abs(r.randn(10))\n\ndf = pd.DataFrame(gauss(xa.T, aa, mua, sia, nf))')


# np.arrayで変数作るともっともっと高速

# In[20]:

xa = np.tile(x, (10,1))
aa = abs(r.randn(10))
mua = np.arange(min(x), max(x), 10)
sia = 10 * abs(r.randn(10))

df = pd.DataFrame(gauss(xa.T, aa, mua, sia, nf))


# In[21]:

df.plot()


# 様々な形のガウシアン。
# 
# ノイズフロアは一定にした。
# 
# こいつらにノイズを載せる。

# ## ランダムデータフレームにノイズのせてサンプルデータ作成

# In[22]:

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

# In[23]:

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


# In[24]:

df = pd.DataFrame([waves(i) for i in range(10)]); df


# # データフレームに一斉にフィッティングかける
# 一番やりたかったこと　ここから。

# ## 試しに波を一つ選んでfitting

# ### 特定範囲を抽出する関数を作成

# In[26]:

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


# In[37]:

ch = (300, 200)  # 中央値300でスパン200で取り出したい
df0 = choice(df.iloc[0], *ch)
df0.plot()


# ### 一つの波をfitting

# In[62]:

param = (a, mu, si, nf) = 5, 300, 3, scoreatpercentile(df0, 25)
param


# パラメータ再設定

# In[66]:

fitx, fity = df0.index, df0.values,
popt, _pcov = curve_fit(gauss, np.array(fitx), fity, p0=param)
print('a, mu, si, nf = ', popt)


# fittingの結果

# In[83]:

df.iloc[0].plot(color='gray', lw=0.5)
plt.plot(df0.index, gauss(df0.index, *popt))
plt.plot(popt[1], popt[0]+popt[3] , 'D', fillstyle='none', mew=2)


# プロットするときは`mu`が横軸、　`a+nf`が縦軸

# ## df縦方向にfitting
# axis=0方向にfitting
# 
# 意味的には特定周波数を別時間軸上で同時に実行。
# `df.apply(curve_fit, args=())`使いたい。

# In[205]:

ax=df.T.plot()
plt.plot((100,100, 300, 300, 100), (4.5, 10.5, 10.5, 4.5, 4.5), 'r-')  # 枠線


# 赤枠の中だけ拡大。(その中だけがフィッティング対象)

# In[106]:

dfe = df.apply(choice,axis=1, args=ch)
dfe.T.plot(legend=False)


# 拡大した図

# ### fitting関数作成

# In[149]:

fit = lambda x: curve_fit(gauss, x.index, x.values, p0=param)  # fitting function
fita = dfe.apply(fit, axis=1)


# フィッティング関数はlambda式で定義して、
# applyでデータフレームの各行に適用。

# In[150]:

type(fita)


# In[207]:

fita


# fitaはpandas.Seriesだが、一つの要素にタプル形式でフィッティングのパラメータと分散が入っている。
# 
# そこで以下のようにして内法表記で分解して第0要素だけ取り出す。

# In[208]:

result = pd.DataFrame((i[0] for i in fita), columns=['a', 'mu', 'si', 'nf']); result


# フィッティング結果のデータフレーム

# ### fitting結果を描く

# In[216]:

df.T.plot()


# In[220]:

defit = lambda a, mu, si ,nf: gauss(np.array(df.columns), a, mu, si ,nf)


# In[221]:

result.apply(defit, axis=1)


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



