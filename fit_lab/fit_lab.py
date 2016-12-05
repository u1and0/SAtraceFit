
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


# In[2]:

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

# In[9]:

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

# In[4]:

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


# In[5]:

df = pd.DataFrame([waves(i) for i in range(10)]); df


# # データフレームに一斉にフィッティングかける
# 一番やりたかったこと　ここから。

# ## 試しに波を一つ選んでfitting

# ### 特定範囲を抽出する関数を作成

# In[6]:

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


# In[7]:

ch = (300, 200)  # 中央値300でスパン200で取り出したい
df0 = choice(df.iloc[0], *ch)
df0.plot()


# ### 一つの波をfitting

# In[10]:

param = (a, mu, si, nf) = 5, 300, 3, scoreatpercentile(df0, 25)
param


# パラメータ再設定

# In[11]:

fitx, fity = df0.index, df0.values,
popt, _pcov = curve_fit(gauss, np.array(fitx), fity, p0=param)
print('a, mu, si, nf = ', popt)


# fittingの結果

# In[12]:

df.iloc[0].plot(color='gray', lw=0.5)
plt.plot(df0.index, gauss(df0.index, *popt))
plt.plot(popt[1], popt[0]+popt[3] , 'D', fillstyle='none', mew=2)


# プロットするときは`mu`が横軸、　`a+nf`が縦軸

# ## df縦方向にfitting
# axis=0方向にfitting
# 
# 意味的には特定周波数を別時間軸上で同時に実行。
# `df.apply(curve_fit, args=())`使いたい。

# In[13]:

df.T.plot()
plt.plot((100,100, 300, 300, 100), (4.5, 10.5, 10.5, 4.5, 4.5), 'r-')  # 枠線


# 赤枠の中だけ拡大。(その中だけがフィッティング対象)

# In[21]:

ch = (300, 200)
dfe = df.apply(choice,axis=1, args=ch)
dfe.T.plot(legend=False)


# 拡大した図

# ### fitting関数作成

# In[22]:

fit = lambda x: curve_fit(gauss, x.index, x.values, p0=param)  # fitting function
fita = dfe.apply(fit, axis=1)


# フィッティング関数はlambda式で定義して、
# applyでデータフレームの各行に適用。

# In[23]:

type(fita)


# In[24]:

fita


# fitaはpandas.Seriesだが、一つの要素にタプル形式でフィッティングのパラメータと分散が入っている。
# 
# そこで以下のようにして内法表記で分解して第0要素だけ取り出す。

# In[46]:

result = pd.DataFrame((i[0] for i in fita), columns=['a', 'mu', 'si', 'nf']); result


# フィッティング結果のデータフレーム

# In[54]:

result = np.array([i[0] for i in fita]); result


# フィッティング結果のnp.array

# ### fitting結果を描く

# In[27]:

df.T.plot()


# この上にfitting結果を重ねていく

# fitting結果resultにapplyする関数を決定する。
# 
# 横軸の値、縦軸の値を返す関数。

# In[58]:

defit = lambda row: (row[1], row[0]+row[3])


# In[38]:

result.columns


# プロットするときは`mu`が横軸、　`a+nf`が縦軸

# In[61]:

plt_pnt = np.apply_along_axis(defit, 1, result); plt_pnt


# In[96]:

plt_pnt_se = pd.Series(plt_pnt.T[1], index=plt_pnt.T[0]); plt_pnt_se


# In[84]:

df.T.plot(cmap='gray')
plt_pnt_se.plot(style='D', mew=2, fillstyle='none')


# # 特定周波数(axis=1方向)のfittingまとめ

# ## モジュール

# In[7]:

from scipy.optimize import curve_fit
from scipy.stats import scoreatpercentile
r = np.random


# ## 関数

# ### ガウス関数

# In[8]:

def gauss(x, a, mu, si, nf):
    """
    a: 最大値
    mu: 位置
    si: 線幅
    noisef: 最低値
    """
    return a * np.exp(-(x - mu)**2 / 2 / si**2) + nf


# ## パラメータ

# In[12]:

param = a, mu, si = 5, 300, 3


# ### フィット関数

# In[1]:

def fit(series, a, mu, si):
    """fitting function
    シリーズに対してガウシアンフィッティングを行う
    引数:
        a: 最大値
        mu: 位置
        si: 線幅
    戻り値:
        cf: フィッティング結果(エラーが起きたときはnp.nanのタプル)"""
    errcount = 0
    x, y =  series.index, series.values
    nf = scoreatpercentile(series, 25)
    cfshape = (4,)
    try:
        cf = curve_fit(gauss, x, y, p0=(a, mu, si, nf))
    except Exception as e:
        errcount += 1
        print('error', errcount, ':', e)  # エラー数, エラーメッセージの表示
        cf = np.full(cfshape, np.nan), np.nan  # エラー起きたらnan返す
    return cf


# ### デフィット関数

# In[2]:

def defit(row):
    """return fitting result as plot point"""
    return row[1], row[0]+row[3]


# ### choice関数

# In[3]:

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


# ## データ

# In[4]:

def waves(seed: int=np.random.randint(100), rows=10):
    """ランダムノイズを発生させたウェーブを作成する
    引数: seed: ランダムステートを初期化する整数。デフォルトでseedをランダムに発生させる
    戻り値: noisedf.sum(1): pd.Series型"""
    r = np.random
    r.seed(seed)  # ランダム初期化
    x = np.linspace(1, 10, 1001)
    xa = np.tile(x, (rows,1))
    aa = abs(r.randn(rows))
    mua = np.linspace(min(x), max(x), rows)
    sia = abs(r.randn(rows))
    nf = 0.01 * r.randn(rows)

    df = pd.DataFrame(gauss(xa.T, aa, mua, sia, nf))
    noisedf = df +  0.05 * r.randn(*df.shape)
    return noisedf.sum(1)


# In[9]:

df = pd.DataFrame([waves(i) for i in range(10)]); df
df.index=pd.date_range('20160101', periods=len(df), freq='H')


# In[10]:

df.T.plot(legend=False)
# 枠線
w1, w2, h1, h2 = 150, 300, -.5, 4.5
plt.plot((w1,w1, w2, w2, w1), (h1, h2, h2, h1, h1), 'r--')


# 赤枠内をフィッティング

# ## フィッティング処理

# In[207]:

ch = (220, 200)  # 中央値220でスパン200で取り出したい
dfe = df.apply(choice,axis=1, args=ch)  # 抜き出し
fita = dfe.apply(fit, axis=1, args=param)  # フィッティング
    
# フィッティング結果の整理
result = np.array([i[0] for i in fita])  # タプルの第一要素だけを取り出しarray化
plt_pnt = np.apply_along_axis(defit, 1, result)  # ポイントのプロットに必要な部分抜き出し
plt_pnt_se = pd.Series(plt_pnt.T[1], index=plt_pnt.T[0])  # fitting結果をseries化


# In[208]:

result


# フィッティング結果resultはarray.
# タプルの第一要素だけを取り出しarray化したもの。
# 
# それぞれの要素は以下のものがdfのindexの個数分出てくる
# 
# `array[ [a, mu, si, nf],[a, mu, si, nf],[a, mu, si, nf],...]`

# ### データフレームへのフィットを関数化
# 
# resultさえあれば何とかなるので、resultをreturnする関数にする。

# In[114]:

def fit_df(df, center, span, param):
    dfe = df.apply(choice,axis=1, args=(center, span))  # dfからcenter,spanで取り出す
    fita = dfe.apply(fit, axis=1, args=param)  # フィッティング # param = a, mu, si
    result = np.array([i[0] for i in fita])  # タプルの第一要素だけを取り出しarray化
    return result


# In[209]:

mu = 780
result = fit_df(df, center=mu, span=200, param=(df[mu].max(), mu, 1))
result


# ### 返ってきたresultで様々な表現

# In[15]:

plt_pnt_se


# plt_pnt_seはポイントのプロットに必要な部分をdefit関数により抜き出したもの

# In[16]:

fita


# defit関数により戻したplt_pnt_seをseries化

# In[17]:

fita.apply(lambda x: x[0][0])


# In[18]:

fita.apply(lambda x: x[0][1]+ x[0][3])


# In[19]:

ase = fita.apply(lambda x: x[0][0])
muse = fita.apply(lambda x: x[0][1]+ x[0][3])
amudf = pd.DataFrame([ase, muse]).T
amudf


# In[20]:

fi = a_, mu_, si_, nf_ = result.T; mu_


# ### フィッティング可視化

# In[81]:

with plt.style.context(('seaborn-darkgrid')):
    df.T.plot(cmap='gray', legend=False)
    plt_pnt_se.plot(style='D', mew=2, fillstyle='none')


# 簡単に、データフレームの上にポイントだけ打ってみた。

# In[48]:

regauss = np.apply_along_axis(lambda x: gauss(df.columns, *x), 1, result)
pd.DataFrame(regauss).T.plot(legend=False)


# resultをガウス関数に当てはめてウェーブを描く

# In[33]:

plt_pnt_se


# In[215]:

def regauss(df, fitresult, axis=1):
    return np.apply_along_axis(lambda x: gauss(df.columns, *x), axis, fitresult)


# In[216]:

fig, ax = plt.subplots(10, sharex=True, figsize=(4,18))
df.T.plot(color='gray', lw=.5, legend=False, subplots=True, ax=ax)
regaussdf = regauss(df, result)
pd.DataFrame(regaussdf).T.plot(legend=False, subplots=True, ax=ax)
for nu in range(len(plt_pnt_se)):
    x,y=plt_pnt_se.index[nu], plt_pnt_se.iloc[nu]
    ax[nu].plot(x, y, 'D', mew=2, fillstyle='none')


# データフレームのインデックスごとに描画

# In[82]:

df.T.plot(lw=.5, cmap='gray', legend=False)
for nu in range(len(df)):
    pd.Series(gauss(df.columns, *result[nu])).plot()
    x,y=plt_pnt_se.index[nu], plt_pnt_se.iloc[nu]
    print(x,y)
    plt.plot(x, y, 'D', mew=2, fillstyle='none')


# In[43]:

fig, ax = plt.subplots(10, sharex=True, figsize=(4,18))
for nu in range(len(df)):
    df.iloc[nu].plot(cmap='gray', legend=False, ax=ax[nu])
    pd.Series(gauss(df.columns, *result[nu])).plot(ax=ax[nu])
    x,y=plt_pnt_se.index[nu], plt_pnt_se.iloc[nu]
    ax[nu].plot(x, y, 'D', mew=2, fillstyle='none')


# ほとんどフィッティングできていないのがお分かりだろうか
# 
# フィルターをかけることでこの中から不要なフィッティング結果を削除する。

# ## フィルタリング

# 具体的に
# 
# * 処理
#     * フィッティング取れていないと思ったものは`np.nan`にする
# * 判定
#     * 逆さまになっている(a < 0)
#     * 大きさが小さい(a < ?)
#     * 大きさがとんでもない(a >> Series.max())
#     * 位置がでたらめ(abs(mu-result[1]) > 1)
#     * 幅が広すぎ(abs(si - result[2]) > 100)
#     * 幅が狭すぎ(1 < abs(si - result[2]))
#     
# 課題として、大きい/小さい、広い/狭い、位置が動きすぎの判定はどれだけのさじ加減か。
# 機械学習できたらな...

# ### aのfitcondition

# In[205]:

def fitcondition_a(array, a_high, a_low):
    """a_high以上、a_low未満はNaN"""
    a = array.T[0]
    a[a > a_high] = np.nan
    a[a < a_low] = np.nan
    return a


# In[206]:

fitcondition_a(result, a_high=df.values.max(), a_low=0)


# ### muのfitcondition

# In[153]:

def fitcondition_mu(array, mu_real, mu_tol):
    """mu_realとmuの差がmu_tol超えたらNaN"""
    mu = array.T[1]
    mu[abs(mu-mu_real) > mu_tol] = np.nan
    return mu


# In[155]:

fitcondition_mu(result, mu, mu*0.1)  # muの値の10%超えたらNaN


# ### siのfitcondition

# In[176]:

def fitcondition_si(array, si_high, si_low):
    """si_realとsiの差がsi_high超えたらNaN"""
    si = array.T[2]
    si[si > si_high] = np.nan
    si[si < si_low] = np.nan
    return si


# In[177]:

fitcondition_si(result, si_high=80, si_low=-np.inf)


# ### fitcondition総合

# In[210]:

def fitcondition(array, **kwargs):
    """fitconditionすべて"""
    fitcondition_a(array, kwargs['a_high'], kwargs['a_low'])
    fitcondition_mu(array, kwargs['mu_real'], kwargs['mu_tol'])
    fitcondition_si(array, kwargs['si_high'], kwargs['si_low'])
    return array


# In[211]:

result


# In[214]:

fitcondition(result, a_high=df.values.max(), a_low=0,
             mu_real=mu, mu_tol=mu*0.1, si_high=80, si_low=-np.inf)
result


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



