
# 自作ガウシアン


```python
def gauss(x, a, mu, si, nf):
    """
    a: 最大値
    mu: 位置
    si: 線幅
    noisef: 最低値
    """
    return a * np.exp(-(x - mu)**2 / 2 / si**2) + nf
```


```python
nf=0.5
n=1001
x = np.linspace(0,100,n)
a, mu, si = 1, 50, 1
```


```python
g= gauss(x, a, mu, si, nf); g
```




    array([ 0.5,  0.5,  0.5, ...,  0.5,  0.5,  0.5])




```python
plt.plot(x, g)
```




    [<matplotlib.lines.Line2D at 0x1a177d2bc88>]




![png](fit_lab_files/fit_lab_4_1.png)


## 自作ガウシアンじゃなくてscipy.stats.normを使うべきでは


```python
from  scipy.stats import norm
```


```python
z=norm.pdf(x, loc=50, scale=1)-0.5; z
```




    array([-0.5, -0.5, -0.5, ..., -0.5, -0.5, -0.5])




```python
plt.plot(x,z)
```




    [<matplotlib.lines.Line2D at 0x1e4a95df9e8>]




![png](fit_lab_files/fit_lab_8_1.png)



```python
a, mu, si=1, 50, 1
df=pd.DataFrame({'norm': a*norm.pdf(x, loc=mu, scale=si)+nf,
                 			'gauss': gauss(x, a, mu, si, nf)})
df.plot(style=['-', '--'])
```




    <matplotlib.axes._subplots.AxesSubplot at 0x148c87f5710>




![png](fit_lab_files/fit_lab_9_1.png)


## norm vs my_gauss
normでも自作gaussでも中でnp使っているんで実行速度あんま変わらないだろうとテスト


```python
%timeit gauss(x, a, mu, si)
```

    The slowest run took 5.79 times longer than the fastest. This could mean that an intermediate result is being cached.
    10000 loops, best of 3: 59.8 µs per loop
    


```python
%timeit norm.pdf(x, loc=50, scale=1)-0.5
```

    The slowest run took 5.26 times longer than the fastest. This could mean that an intermediate result is being cached.
    1000 loops, best of 3: 218 µs per loop
    

自作ガウスのほうが早い…！

## ガウシアンに沿ってノイズを作る

ということで自作のガウシアンを使っていきます。


```python
g = gauss(x, a, mu, si, 0.5)
gnoise = g + 0.1 * g * np.random.randn(n)
```


```python
plt.plot(x, gnoise, '-')
plt.plot(x, g,'b-' )
```




    [<matplotlib.lines.Line2D at 0x1a177c5bcf8>]




![png](fit_lab_files/fit_lab_16_1.png)


ノイズを発生させる

## カーブフィッティングをかけて、ノイズをフィッティングする

gからgnoiseを導き出したのだけれども、ここで急にgを未知の関数とみなしてしまう。
今あなたはgnoiseだけを知っていて、gのような関数を得たいとき、どうするか。

こういう時はカーブフィットを取る。
scipy.optimizeからcurve_fitをインポートしてくる。


```python
from scipy.optimize import curve_fit
from scipy.optimize import leastsq
from scipy.optimize import least_squares
from scipy.stats import scoreatpercentile
```

次にフィッティングパラメータを定める。


```python
(a_, mu_, si_, nf_), _ = curve_fit(gauss, x, gnoise, p0=(a, mu, si, nf))
yfit = gauss(x, a_, mu_, si_, nf)  # フィッティングにより導き出されたa,mu,siを代入
print('元パラメータ:%s\nフィッティングで求めたパラメータ: %s' % ((a, mu , si), (a_, mu_, si_)))
```

    元パラメータ:(1, 50, 1)
    フィッティングで求めたパラメータ: (0.98288835192385138, 49.983822066353746, 0.99222230410189216)
    


```python
_
```




    array([[  2.69528582e-04,   1.34053555e-10,  -1.71228319e-04,
             -2.27783859e-06],
           [  1.34053555e-10,   3.40470185e-04,  -1.30160080e-10,
             -1.16627832e-14],
           [ -1.71228319e-04,  -1.30160080e-10,   3.46610735e-04,
             -4.44756457e-06],
           [ -2.27783859e-06,  -1.16627832e-14,  -4.44756457e-06,
              3.22135030e-06]])



curve_fitの戻り値アンダーバーは共分散？

    pcov : 2d array
    The estimated covariance of popt. The diagonals provide the variance
    of the parameter estimate. To compute one standard deviation errors
    on the parameters use ``perr = np.sqrt(np.diag(pcov))``.


```python
plt.plot(x, gnoise, 'r-')
plt.plot(x, yfit, 'b-') 
```




    [<matplotlib.lines.Line2D at 0x1a1796a6828>]




![png](fit_lab_files/fit_lab_24_1.png)


さっきと同じグラフに見えるが、描いているのはgではなくyfitであることに注意

同じグラフに見えるということはフィッティングできたということ。

# scipy.stats.normを使った場合

## ガウシアンに沿ってノイズを作る


```python
from  scipy.stats import norm
```


```python
n=1001
xx = np.linspace(0,100,n)
aa, mu, si = 5, 50, 1
```


```python
def gauss2(x, a, mu, si):
    return a*norm.pdf(x, loc=mu, scale=si)-noisef
```


```python
g = gauss2(xx, aa, mu, si)
gnoise = g + 0.1 * np.random.randn(n)
```


```python
plt.plot(xx, gnoise, '.-')
plt.plot(xx, g,'r-' )
```




    [<matplotlib.lines.Line2D at 0x1ca7b0647f0>]




![png](fit_lab_files/fit_lab_32_1.png)


## カーブフィッティングをかけて、ノイズをフィッティングする

gからgnoiseを導き出したのだけれども、ここで急にgを未知の関数とみなしてしまう。
今あなたはgnoiseだけを知っていて、gのような関数を得たいとき、どうするか。


```python
from scipy.optimize import curve_fit
(aa_, mu_, si_), _ = curve_fit(gauss2, xx, gnoise, (aa, mu, si))
yfit = gauss2(xx,aa_, mu_, si_)
```


```python
plt.plot(xx, gnoise, '.-')
plt.plot(xx, yfit, 'r-')  # 描いているのはgではなく、yfitであることに注意
```




    [<matplotlib.lines.Line2D at 0x1ca7b1252e8>]




![png](fit_lab_files/fit_lab_35_1.png)


ちゃんとフィッティングできた。

# 自作ガウスをノイズのあるデータフレームにcarve_fitをapply

## ランダムデータフレームの作成


```python
r=np.random
```

いっぱい使うから乱数生成をrに縮めちゃう


```python
g = gauss(x, a=r.rand(), mu=10*1, si=10*r.rand(), nf=nf*r.rand())
plt.plot(x, g)
```




    [<matplotlib.lines.Line2D at 0x1a1782dae80>]




![png](fit_lab_files/fit_lab_41_1.png)


ランダムな値を使って発生させたガウシアン


```python
%%timeit
df = pd.DataFrame([], index=range(1000))
for i in np.arange(min(x), max(x), 10):
    g = gauss(x, a=r.rand(), mu=i, si=10*r.rand(), noisef=nf)
    df[i] = pd.DataFrame(g)
```

    100 loops, best of 3: 8.69 ms per loop
    

まず思いつくforループ


```python
%%timeit
garray = np.array([gauss(x, a=r.rand(), mu=i, si=10*r.rand(), noisef=nf)
                    for i in np.arange(min(x), max(x), 10)]).T
df = pd.DataFrame(garray)
```

    1000 loops, best of 3: 743 µs per loop
    

リスト内包表記を使うことでより高速


```python
%%timeit
xa = np.tile(x, (10,1))
aa = abs(r.randn(10))
mua = np.arange(min(x), max(x), 10)
sia = 10 * abs(r.randn(10))

df = pd.DataFrame(gauss(xa.T, aa, mua, sia, nf))
```

    1000 loops, best of 3: 604 µs per loop
    

np.arrayで変数作るともっともっと高速


```python
xa = np.tile(x, (10,1))
aa = abs(r.randn(10))
mua = np.arange(min(x), max(x), 10)
sia = 10 * abs(r.randn(10))

df = pd.DataFrame(gauss(xa.T, aa, mua, sia, nf))
```


```python
df.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1a1782ad518>




![png](fit_lab_files/fit_lab_50_1.png)


様々な形のガウシアン。

ノイズフロアは一定にした。

こいつらにノイズを載せる。

## ランダムデータフレームにノイズのせてサンプルデータ作成


```python
noisedf =df + df * 0.05 * r.randn(*df.shape)
noisedf.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1a1783d5198>




![png](fit_lab_files/fit_lab_53_1.png)


5%のノイズをのせた。
`np.randn(*df.shape)`でデータフレームと同じ行列を持ったランダムデータフレームを生成させている。
スターを`df.shape`の前につけてタプルを展開して`randn`に渡す。


```python
sumdf = noisedf.sum(axis=1)
sumdf.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x1de4c436320>




![png](fit_lab_files/fit_lab_55_1.png)



```python
sumdf
```




    0       5.432676
    1       5.605698
    2       5.298539
    3       5.522210
    4       5.598536
    5       5.628876
    6       5.590488
    7       5.520159
    8       5.357040
    9       5.524325
    10      5.352305
    11      5.252700
    12      5.442083
    13      5.357631
    14      5.633205
    15      5.394023
    16      5.485547
    17      5.300434
    18      5.472389
    19      5.403377
    20      4.983068
    21      5.330210
    22      5.274541
    23      5.166913
    24      5.551668
    25      5.476331
    26      5.108893
    27      4.984221
    28      5.214877
    29      5.402299
              ...   
    971     5.363341
    972     5.478791
    973     5.665920
    974     5.777761
    975     5.737976
    976     5.659097
    977     5.625246
    978     5.545209
    979     5.726983
    980     5.747878
    981     5.479815
    982     5.714544
    983     5.406541
    984     5.325538
    985     5.532115
    986     5.222370
    987     5.502674
    988     5.481744
    989     5.548988
    990     5.690841
    991     5.502521
    992     5.599736
    993     5.366537
    994     5.508551
    995     5.497639
    996     5.128502
    997     5.403535
    998     5.350118
    999     5.540160
    1000    5.401792
    dtype: float64



indexはそのままにカラムをすべて足す。この中でindexいくつの位置にガウシアンが立つかを調べる。

## 複数のランダムウェーブを生成


```python
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
```




    <matplotlib.axes._subplots.AxesSubplot at 0x28e0a0c9160>




![png](fit_lab_files/fit_lab_59_1.png)



```python
%timeit waves()
```

    100 loops, best of 3: 2.33 ms per loop
    


```python
df = pd.DataFrame([waves(i) for i in range(10)]); df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
      <th>7</th>
      <th>8</th>
      <th>9</th>
      <th>...</th>
      <th>991</th>
      <th>992</th>
      <th>993</th>
      <th>994</th>
      <th>995</th>
      <th>996</th>
      <th>997</th>
      <th>998</th>
      <th>999</th>
      <th>1000</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>6.945187</td>
      <td>7.108197</td>
      <td>6.845565</td>
      <td>6.948541</td>
      <td>6.845199</td>
      <td>7.055347</td>
      <td>6.977616</td>
      <td>7.056927</td>
      <td>7.079365</td>
      <td>7.138362</td>
      <td>...</td>
      <td>5.352165</td>
      <td>5.237588</td>
      <td>5.368697</td>
      <td>5.147199</td>
      <td>5.197124</td>
      <td>5.213663</td>
      <td>5.317618</td>
      <td>5.263670</td>
      <td>5.266836</td>
      <td>5.319199</td>
    </tr>
    <tr>
      <th>1</th>
      <td>7.133442</td>
      <td>7.059512</td>
      <td>7.190294</td>
      <td>7.232617</td>
      <td>7.261932</td>
      <td>7.016845</td>
      <td>7.189088</td>
      <td>7.295845</td>
      <td>7.185489</td>
      <td>7.022073</td>
      <td>...</td>
      <td>5.166897</td>
      <td>5.017208</td>
      <td>5.075220</td>
      <td>5.214620</td>
      <td>5.136346</td>
      <td>5.049252</td>
      <td>5.014033</td>
      <td>5.049660</td>
      <td>5.022505</td>
      <td>5.217068</td>
    </tr>
    <tr>
      <th>2</th>
      <td>5.348248</td>
      <td>5.553449</td>
      <td>5.548598</td>
      <td>5.538164</td>
      <td>5.430301</td>
      <td>5.412686</td>
      <td>5.579073</td>
      <td>5.552572</td>
      <td>5.647116</td>
      <td>5.415833</td>
      <td>...</td>
      <td>5.104680</td>
      <td>5.207193</td>
      <td>5.014641</td>
      <td>5.061536</td>
      <td>5.125885</td>
      <td>5.072221</td>
      <td>5.181555</td>
      <td>4.908350</td>
      <td>5.057412</td>
      <td>5.102178</td>
    </tr>
    <tr>
      <th>3</th>
      <td>7.274488</td>
      <td>7.426611</td>
      <td>7.076638</td>
      <td>7.595002</td>
      <td>7.723684</td>
      <td>7.506426</td>
      <td>7.210183</td>
      <td>7.406186</td>
      <td>7.584276</td>
      <td>7.486866</td>
      <td>...</td>
      <td>5.332370</td>
      <td>5.272767</td>
      <td>5.421780</td>
      <td>5.499642</td>
      <td>5.210076</td>
      <td>5.363444</td>
      <td>5.385211</td>
      <td>5.220253</td>
      <td>5.466960</td>
      <td>5.286162</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5.086649</td>
      <td>5.070892</td>
      <td>5.054293</td>
      <td>5.011917</td>
      <td>5.164769</td>
      <td>5.146161</td>
      <td>4.921866</td>
      <td>5.057269</td>
      <td>5.123093</td>
      <td>5.084757</td>
      <td>...</td>
      <td>5.065826</td>
      <td>5.150936</td>
      <td>5.078083</td>
      <td>5.028696</td>
      <td>5.064742</td>
      <td>5.037380</td>
      <td>5.331177</td>
      <td>5.131369</td>
      <td>5.206482</td>
      <td>5.235898</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5.380750</td>
      <td>5.546886</td>
      <td>5.502097</td>
      <td>5.557626</td>
      <td>5.416009</td>
      <td>5.364240</td>
      <td>5.585252</td>
      <td>5.475956</td>
      <td>5.528495</td>
      <td>5.392496</td>
      <td>...</td>
      <td>5.354433</td>
      <td>5.439949</td>
      <td>5.550969</td>
      <td>5.281462</td>
      <td>5.491426</td>
      <td>5.382127</td>
      <td>5.453180</td>
      <td>5.208387</td>
      <td>5.277590</td>
      <td>5.423068</td>
    </tr>
    <tr>
      <th>6</th>
      <td>5.629440</td>
      <td>5.443759</td>
      <td>5.531657</td>
      <td>5.720805</td>
      <td>5.500641</td>
      <td>5.665483</td>
      <td>5.582582</td>
      <td>5.677595</td>
      <td>5.435612</td>
      <td>5.648220</td>
      <td>...</td>
      <td>5.288703</td>
      <td>5.109035</td>
      <td>5.229636</td>
      <td>5.267676</td>
      <td>5.134689</td>
      <td>5.277698</td>
      <td>5.236259</td>
      <td>5.066652</td>
      <td>5.206823</td>
      <td>5.181833</td>
    </tr>
    <tr>
      <th>7</th>
      <td>6.827328</td>
      <td>6.582126</td>
      <td>6.744212</td>
      <td>6.905696</td>
      <td>6.514176</td>
      <td>6.890059</td>
      <td>6.824137</td>
      <td>6.794166</td>
      <td>6.634765</td>
      <td>6.680948</td>
      <td>...</td>
      <td>5.532310</td>
      <td>5.495926</td>
      <td>5.500994</td>
      <td>5.431254</td>
      <td>5.448915</td>
      <td>5.520323</td>
      <td>5.463009</td>
      <td>5.670345</td>
      <td>5.523788</td>
      <td>5.370447</td>
    </tr>
    <tr>
      <th>8</th>
      <td>6.417707</td>
      <td>6.429011</td>
      <td>6.475284</td>
      <td>6.290368</td>
      <td>6.670582</td>
      <td>6.636257</td>
      <td>6.427363</td>
      <td>6.455692</td>
      <td>6.620168</td>
      <td>6.508548</td>
      <td>...</td>
      <td>4.998059</td>
      <td>4.907901</td>
      <td>4.900991</td>
      <td>4.984814</td>
      <td>5.011483</td>
      <td>4.939173</td>
      <td>5.053548</td>
      <td>4.868739</td>
      <td>4.874232</td>
      <td>4.905128</td>
    </tr>
    <tr>
      <th>9</th>
      <td>5.285603</td>
      <td>5.404935</td>
      <td>5.279550</td>
      <td>5.060339</td>
      <td>5.276347</td>
      <td>5.236848</td>
      <td>5.305694</td>
      <td>5.347108</td>
      <td>5.337980</td>
      <td>5.361805</td>
      <td>...</td>
      <td>5.626433</td>
      <td>5.572625</td>
      <td>5.647371</td>
      <td>5.480810</td>
      <td>5.495603</td>
      <td>5.535284</td>
      <td>5.492852</td>
      <td>5.550408</td>
      <td>5.592165</td>
      <td>5.344825</td>
    </tr>
  </tbody>
</table>
<p>10 rows × 1001 columns</p>
</div>



# データフレームに一斉にフィッティングかける
一番やりたかったこと　ここから。

## 試しに波を一つ選んでfitting

### 特定範囲を抽出する関数を作成


```python
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
```


```python
ch = (300, 200)  # 中央値300でスパン200で取り出したい
df0 = choice(df.iloc[0], *ch)
df0.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x28e0a0945c0>




![png](fit_lab_files/fit_lab_66_1.png)


### 一つの波をfitting


```python
param = (a, mu, si, nf) = 5, 300, 3, scoreatpercentile(df0, 25)
param
```




    (5, 300, 3, 6.1943784193082427)



パラメータ再設定


```python
fitx, fity = df0.index, df0.values,
popt, _pcov = curve_fit(gauss, np.array(fitx), fity, p0=param)
print('a, mu, si, nf = ', popt)
```

    a, mu, si, nf =  [   1.64608234  299.80613945    8.94731799    6.44094237]
    

fittingの結果


```python
df.iloc[0].plot(color='gray', lw=0.5)
plt.plot(df0.index, gauss(df0.index, *popt))
plt.plot(popt[1], popt[0]+popt[3] , 'D', fillstyle='none', mew=2)
```




    [<matplotlib.lines.Line2D at 0x28e0a53a278>]




![png](fit_lab_files/fit_lab_72_1.png)


プロットするときは`mu`が横軸、　`a+nf`が縦軸

## df縦方向にfitting
axis=0方向にfitting

意味的には特定周波数を別時間軸上で同時に実行。
`df.apply(curve_fit, args=())`使いたい。


```python
df.T.plot()
plt.plot((100,100, 300, 300, 100), (4.5, 10.5, 10.5, 4.5, 4.5), 'r-')  # 枠線
```




    [<matplotlib.lines.Line2D at 0x28e0a54a7b8>]




![png](fit_lab_files/fit_lab_75_1.png)


赤枠の中だけ拡大。(その中だけがフィッティング対象)


```python
ch = (300, 200)
dfe = df.apply(choice,axis=1, args=ch)
dfe.T.plot(legend=False)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x28e0b874f28>




![png](fit_lab_files/fit_lab_77_1.png)


拡大した図

### fitting関数作成


```python
fit = lambda x: curve_fit(gauss, x.index, x.values, p0=param)  # fitting function
fita = dfe.apply(fit, axis=1)
```

フィッティング関数はlambda式で定義して、
applyでデータフレームの各行に適用。


```python
type(fita)
```




    pandas.core.series.Series




```python
fita
```




    0    ([1.64608233941, 299.806139455, 8.94731798894,...
    1    ([1.06720581454, 342.175948763, 77.8097497546,...
    2    ([-1.86034853457, 247.618524866, 71.1429284505...
    3    ([0.119213086912, 301.166378566, 1.38645305185...
    4    ([603.417204075, 231.312304775, 3682.28745173,...
    5    ([-8214.48961119, 324.777372988, 5187.93270244...
    6    ([-10834.1282713, 288.175702378, 7442.99563502...
    7    ([0.167421897449, 299.669427889, 11.8363393835...
    8    ([-10855.5095368, 267.685530085, 9114.65805152...
    9    ([-5964.08199733, 311.71632169, 6258.82944108,...
    dtype: object



fitaはpandas.Seriesだが、一つの要素にタプル形式でフィッティングのパラメータと分散が入っている。

そこで以下のようにして内法表記で分解して第0要素だけ取り出す。


```python
result = pd.DataFrame((i[0] for i in fita), columns=['a', 'mu', 'si', 'nf']); result
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>a</th>
      <th>mu</th>
      <th>si</th>
      <th>nf</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.646082</td>
      <td>299.806139</td>
      <td>8.947318</td>
      <td>6.440942</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.067206</td>
      <td>342.175949</td>
      <td>77.809750</td>
      <td>6.611884</td>
    </tr>
    <tr>
      <th>2</th>
      <td>-1.860349</td>
      <td>247.618525</td>
      <td>71.142928</td>
      <td>8.390693</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.119213</td>
      <td>301.166379</td>
      <td>1.386453</td>
      <td>7.093136</td>
    </tr>
    <tr>
      <th>4</th>
      <td>603.417204</td>
      <td>231.312305</td>
      <td>3682.287452</td>
      <td>-597.375350</td>
    </tr>
    <tr>
      <th>5</th>
      <td>-8214.489611</td>
      <td>324.777373</td>
      <td>5187.932702</td>
      <td>8219.951273</td>
    </tr>
    <tr>
      <th>6</th>
      <td>-10834.128271</td>
      <td>288.175702</td>
      <td>7442.995635</td>
      <td>10840.016757</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.167422</td>
      <td>299.669428</td>
      <td>11.836339</td>
      <td>5.240607</td>
    </tr>
    <tr>
      <th>8</th>
      <td>-10855.509537</td>
      <td>267.685530</td>
      <td>9114.658052</td>
      <td>10863.926883</td>
    </tr>
    <tr>
      <th>9</th>
      <td>-5964.081997</td>
      <td>311.716322</td>
      <td>6258.829441</td>
      <td>5969.772154</td>
    </tr>
  </tbody>
</table>
</div>



フィッティング結果のデータフレーム


```python
result = np.array([i[0] for i in fita]); result
```




    array([[  1.64608234e+00,   2.99806139e+02,   8.94731799e+00,
              6.44094237e+00],
           [  1.06720581e+00,   3.42175949e+02,   7.78097498e+01,
              6.61188409e+00],
           [ -1.86034853e+00,   2.47618525e+02,   7.11429285e+01,
              8.39069261e+00],
           [  1.19213087e-01,   3.01166379e+02,   1.38645305e+00,
              7.09313574e+00],
           [  6.03417204e+02,   2.31312305e+02,   3.68228745e+03,
             -5.97375350e+02],
           [ -8.21448961e+03,   3.24777373e+02,   5.18793270e+03,
              8.21995127e+03],
           [ -1.08341283e+04,   2.88175702e+02,   7.44299564e+03,
              1.08400168e+04],
           [  1.67421897e-01,   2.99669428e+02,   1.18363394e+01,
              5.24060726e+00],
           [ -1.08555095e+04,   2.67685530e+02,   9.11465805e+03,
              1.08639269e+04],
           [ -5.96408200e+03,   3.11716322e+02,   6.25882944e+03,
              5.96977215e+03]])



フィッティング結果のnp.array

### fitting結果を描く


```python
df.T.plot()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x28e0a5ad898>




![png](fit_lab_files/fit_lab_90_1.png)


この上にfitting結果を重ねていく

fitting結果resultにapplyする関数を決定する。

横軸の値、縦軸の値を返す関数。


```python
defit = lambda row: (row[1], row[0]+row[3])
```


```python
result.columns
```




    Index(['a', 'mu', 'si', 'nf'], dtype='object')



プロットするときは`mu`が横軸、　`a+nf`が縦軸


```python
plt_pnt = np.apply_along_axis(defit, 1, result); plt_pnt
```




    array([[ 299.80613945,    8.08702471],
           [ 342.17594876,    7.6790899 ],
           [ 247.61852487,    6.53034408],
           [ 301.16637857,    7.21234883],
           [ 231.31230478,    6.04185377],
           [ 324.77737299,    5.46166178],
           [ 288.17570238,    5.8884859 ],
           [ 299.66942789,    5.40802915],
           [ 267.68553009,    8.41734618],
           [ 311.71632169,    5.69015661]])




```python
plt_pnt_se = pd.Series(plt_pnt.T[1], index=plt_pnt.T[0]); plt_pnt_se
```




    299.806139    8.087025
    342.175949    7.679090
    247.618525    6.530344
    301.166379    7.212349
    231.312305    6.041854
    324.777373    5.461662
    288.175702    5.888486
    299.669428    5.408029
    267.685530    8.417346
    311.716322    5.690157
    dtype: float64




```python
df.T.plot(cmap='gray')
plt_pnt_se.plot(style='D', mew=2, fillstyle='none')
```




    <matplotlib.axes._subplots.AxesSubplot at 0x28e0d0400b8>




![png](fit_lab_files/fit_lab_98_1.png)


# 特定周波数(axis=1方向)のfittingまとめ

## モジュール


```python
from scipy.optimize import curve_fit
from scipy.stats import scoreatpercentile
r = np.random
```

## 関数

### ガウス関数


```python
def gauss(x, a, mu, si, nf):
    """
    a: 最大値
    mu: 位置
    si: 線幅
    noisef: 最低値
    """
    return a * np.exp(-(x - mu)**2 / 2 / si**2) + nf
```

## パラメータ


```python
param = a, mu, si = 5, 300, 3
```

### フィット関数


```python
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
```

### デフィット関数


```python
def defit(row):
    """return fitting result as plot point"""
    return row[1], row[0]+row[3]
```

### choice関数


```python
def choice(array, center, span):↔

```

## データ


```python
def waves(seed: int=np.random.randint(100), rows=10):↔

    df = pd.DataFrame(gauss(xa.T, aa, mua, sia, nf))
    noisedf = df +  0.05 * r.randn(*df.shape)
    return noisedf.sum(1)
```


```python
df = pd.DataFrame([waves(i) for i in range(10)]); df
df.index=pd.date_range('20160101', periods=len(df), freq='H')
```


```python
df.T.plot(legend=False)
# 枠線
w1, w2, h1, h2 = 150, 300, -.5, 4.5
plt.plot((w1,w1, w2, w2, w1), (h1, h2, h2, h1, h1), 'r--')
```




    [<matplotlib.lines.Line2D at 0xb7f7048>]




![png](fit_lab_files/fit_lab_116_1.png)


赤枠内をフィッティング

## フィッティング処理


```python
ch = (220, 200)  # 中央値220でスパン200で取り出したい
dfe = df.apply(choice,axis=1, args=ch)  # 抜き出し
fita = dfe.apply(fit, axis=1, args=param)  # フィッティング
    
# フィッティング結果の整理
result = np.array([i[0] for i in fita])  # タプルの第一要素だけを取り出しarray化
plt_pnt = np.apply_along_axis(defit, 1, result)  # ポイントのプロットに必要な部分抜き出し
plt_pnt_se = pd.Series(plt_pnt.T[1], index=plt_pnt.T[0])  # fitting結果をseries化
```

    error 1 : Optimal parameters not found: Number of calls to function has reached maxfev = 1000.
    


```python
result
```




    array([[ -2.66132842e-01,   2.88736148e+02,   9.15963390e+00,
              1.22932384e+00],
           [  6.29053800e-01,   3.11584775e+02,   1.57575658e+01,
              1.90521197e+00],
           [  2.25524792e+00,   2.82022999e+02,   1.16582536e+02,
             -5.87482031e-01],
           [             nan,              nan,              nan,
                         nan],
           [  1.84837107e+00,   2.57369098e+02,   1.19955217e+02,
             -7.69991058e-01],
           [ -1.12784752e+00,   3.09939505e+02,   2.05845982e+01,
              1.69080069e+00],
           [ -2.75390973e-01,   3.04536318e+02,   3.17605280e+01,
              1.35006383e+00],
           [  1.88870239e-01,   3.22392036e+02,   1.21034501e+01,
              1.45666266e-01],
           [  1.14160133e+00,   2.82278675e+02,   8.91448753e+01,
              2.47223875e+00],
           [ -3.80732172e-01,   3.01482594e+02,   1.72303744e+01,
              1.04019927e+00]])



フィッティング結果resultはarray.
タプルの第一要素だけを取り出しarray化したもの。

それぞれの要素は以下のものがdfのindexの個数分出てくる

`array[ [a, mu, si, nf],[a, mu, si, nf],[a, mu, si, nf],...]`

### データフレームへのフィットを関数化

resultさえあれば何とかなるので、resultをreturnする関数にする。


```python
def fit_df(df, center, span, param):
    dfe = df.apply(choice,axis=1, args=(center, span))  # dfからcenter,spanで取り出す
    fita = dfe.apply(fit, axis=1, args=param)  # フィッティング # param = a, mu, si
    result = np.array([i[0] for i in fita])  # タプルの第一要素だけを取り出しarray化
    return result
```


```python
mu = 220
result = fit_df(df, center=mu, span=200, param=(df[mu].max(), mu, 1))
result
```




    array([[  2.21691725e-01,   2.13580606e+02,   2.71176423e+01,
              1.12346093e+00],
           [  1.82872764e-01,   2.20590464e+02,   8.88599712e-01,
              1.98918253e+00],
           [  2.08159926e+00,   2.22439925e+02,   4.59234267e+00,
              1.08671082e+00],
           [ -5.75501049e-01,   2.19661573e+02,   2.67285120e-01,
              2.43258836e+00],
           [  1.84757841e+00,   2.57369440e+02,   1.19921676e+02,
             -7.69187238e-01],
           [  2.10001609e+00,   2.23559109e+02,   3.64246222e+01,
              5.40678934e-01],
           [  5.36912197e-01,   2.19109931e+02,  -1.06405484e-01,
              1.27381097e+00],
           [  2.84744125e-01,   2.20155924e+02,  -1.66996800e-01,
              1.56364664e-01],
           [  1.14160092e+00,   2.82278656e+02,   8.91448299e+01,
              2.47223917e+00],
           [  1.12007172e+00,   2.26628421e+02,   3.30471036e+01,
              5.07641118e-01]])



### 返ってきたresultで様々な表現


```python
plt_pnt = np.apply_along_axis(defit, 1, result)  # ポイントのプロットに必要な部分抜き出し
plt_pnt_se = pd.Series(plt_pnt.T[1], index=plt_pnt.T[0])  # fitting結果をseries化
plt_pnt_se
```




    213.580606    1.345153
    220.590464    2.172055
    222.439925    3.168310
    219.661573    1.857087
    257.369440    1.078391
    223.559109    2.640695
    219.109931    1.810723
    220.155924    0.441109
    282.278656    3.613840
    226.628421    1.627713
    dtype: float64



plt_pnt_seはポイントのプロットに必要な部分をdefit関数により抜き出したもの


```python
ch = (220, 200)  # 中央値220でスパン200で取り出したい
dfe = df.apply(choice,axis=1, args=ch)  # 抜き出し
param = (df.values.max(), 220, 1)
fita = dfe.apply(fit, axis=1, args=param)  # フィッティング
fita
```

    C:\tools\Anaconda3\lib\site-packages\scipy\optimize\minpack.py:715: OptimizeWarning: Covariance of the parameters could not be estimated
      category=OptimizeWarning)
    




    2016-01-01 00:00:00    ([0.221690672943, 213.580488158, 27.1208233524...
    2016-01-01 01:00:00    ([0.182837882718, 220.590773451, 0.88893858950...
    2016-01-01 02:00:00    ([2.08159841168, 222.439929952, 4.59234679185,...
    2016-01-01 03:00:00    ([-0.599273196879, 219.657527327, 0.2639297643...
    2016-01-01 04:00:00    ([1.84821490434, 257.369180184, 119.948620612,...
    2016-01-01 05:00:00    ([2.10001496382, 223.55910331, 36.4245546125, ...
    2016-01-01 06:00:00    ([-0.115082890904, 219.504196564, 0.0011172805...
    2016-01-01 07:00:00    ([0.425635251809, 220.140523187, -0.1085459189...
    2016-01-01 08:00:00    ([1.14160086337, 282.278652916, 89.1448232556,...
    2016-01-01 09:00:00    ([1.1200718093, 226.628402467, 33.0471191404, ...
    Freq: H, dtype: object



defit関数により戻したplt_pnt_seをseries化


```python
fita.apply(lambda x: x[0][0])
```




    2016-01-01 00:00:00    0.221691
    2016-01-01 01:00:00    0.182838
    2016-01-01 02:00:00    2.081598
    2016-01-01 03:00:00   -0.599273
    2016-01-01 04:00:00    1.848215
    2016-01-01 05:00:00    2.100015
    2016-01-01 06:00:00   -0.115083
    2016-01-01 07:00:00    0.425635
    2016-01-01 08:00:00    1.141601
    2016-01-01 09:00:00    1.120072
    Freq: H, dtype: float64




```python
fita.apply(lambda x: x[0][1]+ x[0][3])
```




    2016-01-01 00:00:00    214.703941
    2016-01-01 01:00:00    222.579956
    2016-01-01 02:00:00    223.526641
    2016-01-01 03:00:00    222.090116
    2016-01-01 04:00:00    256.599347
    2016-01-01 05:00:00    224.099784
    2016-01-01 06:00:00    220.779582
    2016-01-01 07:00:00    220.296888
    2016-01-01 08:00:00    284.750892
    2016-01-01 09:00:00    227.136043
    Freq: H, dtype: float64




```python
ase = fita.apply(lambda x: x[0][0])
muse = fita.apply(lambda x: x[0][1]+ x[0][3])
amudf = pd.DataFrame([ase, muse]).T
amudf
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2016-01-01 00:00:00</th>
      <td>0.221691</td>
      <td>214.703941</td>
    </tr>
    <tr>
      <th>2016-01-01 01:00:00</th>
      <td>0.182838</td>
      <td>222.579956</td>
    </tr>
    <tr>
      <th>2016-01-01 02:00:00</th>
      <td>2.081598</td>
      <td>223.526641</td>
    </tr>
    <tr>
      <th>2016-01-01 03:00:00</th>
      <td>-0.599273</td>
      <td>222.090116</td>
    </tr>
    <tr>
      <th>2016-01-01 04:00:00</th>
      <td>1.848215</td>
      <td>256.599347</td>
    </tr>
    <tr>
      <th>2016-01-01 05:00:00</th>
      <td>2.100015</td>
      <td>224.099784</td>
    </tr>
    <tr>
      <th>2016-01-01 06:00:00</th>
      <td>-0.115083</td>
      <td>220.779582</td>
    </tr>
    <tr>
      <th>2016-01-01 07:00:00</th>
      <td>0.425635</td>
      <td>220.296888</td>
    </tr>
    <tr>
      <th>2016-01-01 08:00:00</th>
      <td>1.141601</td>
      <td>284.750892</td>
    </tr>
    <tr>
      <th>2016-01-01 09:00:00</th>
      <td>1.120072</td>
      <td>227.136043</td>
    </tr>
  </tbody>
</table>
</div>




```python
fi = a_, mu_, si_, nf_ = result.T; mu_
```




    array([ 213.58060554,  220.59046389,  222.43992503,  219.66157289,
            257.36943998,  223.55910904,  219.10993057,  220.15592395,
            282.27865555,  226.62842067])



### フィッティング可視化


```python
with plt.style.context(('seaborn-darkgrid')):
    df.T.plot(cmap='gray', legend=False)
    plt_pnt_se.plot(style='D', mew=2, fillstyle='none')
```


![png](fit_lab_files/fit_lab_135_0.png)


簡単に、データフレームの上にポイントだけ打ってみた。


```python
regauss = np.apply_along_axis(lambda x: gauss(df.columns, *x), 1, result)
pd.DataFrame(regauss).T.plot(legend=False)
```




    <matplotlib.axes._subplots.AxesSubplot at 0xc696400>




![png](fit_lab_files/fit_lab_137_1.png)


resultをガウス関数に当てはめてウェーブを描く


```python
plt_pnt_se
```




    213.580606    1.345153
    220.590464    2.172055
    222.439925    3.168310
    219.661573    1.857087
    257.369440    1.078391
    223.559109    2.640695
    219.109931    1.810723
    220.155924    0.441109
    282.278656    3.613840
    226.628421    1.627713
    dtype: float64




```python
def regauss(x, fitresult, axis=1):
    """フィッティング結果のarrayをガウシアンに適用して、
    ガウシアンの入ったarrayを返す"""
    return np.apply_along_axis(lambda row: gauss(x, *row), axis, fitresult)
```


```python
fig, ax = plt.subplots(10, sharex=True, figsize=(4,18))
df.T.plot(color='gray', lw=.5, legend=False, subplots=True, ax=ax)
regaussdf = regauss(df.columns, result)
pd.DataFrame(regaussdf).T.plot(legend=False, subplots=True, ax=ax)
for nu in range(len(plt_pnt_se)):
    x,y=plt_pnt_se.index[nu], plt_pnt_se.iloc[nu]
    ax[nu].plot(x, y, 'D', mew=2, fillstyle='none')
```


![png](fit_lab_files/fit_lab_141_0.png)


データフレームのインデックスごとに描画


```python
df.T.plot(lw=.5, cmap='gray', legend=False)
for nu in range(len(df)):
    pd.Series(gauss(df.columns, *result[nu])).plot()
    x,y=plt_pnt_se.index[nu], plt_pnt_se.iloc[nu]
    print(x,y)
    plt.plot(x, y, 'D', mew=2, fillstyle='none')
```

    213.580605538 1.34515265913
    220.59046389 2.17205529893
    222.439925034 3.16831007531
    219.66157289 1.85708731459
    257.369439978 1.0783911683
    223.559109042 2.64069502599
    219.109930572 1.81072316438
    220.155923946 0.441108789599
    282.278655555 3.61384009745
    226.628420666 1.6277128406
    


![png](fit_lab_files/fit_lab_143_1.png)



```python
fig, ax = plt.subplots(10, sharex=True, figsize=(4,18))
for nu in range(len(df)):
    df.iloc[nu].plot(cmap='gray', legend=False, ax=ax[nu])
    pd.Series(gauss(df.columns, *result[nu])).plot(ax=ax[nu])
    x,y=plt_pnt_se.index[nu], plt_pnt_se.iloc[nu]
    ax[nu].plot(x, y, 'D', mew=2, fillstyle='none')
```


![png](fit_lab_files/fit_lab_144_0.png)


ほとんどフィッティングできていないのがお分かりだろうか

フィルターをかけることでこの中から不要なフィッティング結果を削除する。

## フィルタリング

具体的に

* 処理
    * フィッティング取れていないと思ったものは`np.nan`にする
* 判定
    * 逆さまになっている(a < 0)
    * 大きさが小さい(a < ?)
    * 大きさがとんでもない(a >> Series.max())
    * 位置がでたらめ(abs(mu-result[1]) > 1)
    * 幅が広すぎ(abs(si - result[2]) > 100)
    * 幅が狭すぎ(1 < abs(si - result[2]))
    
課題として、大きい/小さい、広い/狭い、位置が動きすぎの判定はどれだけのさじ加減か。
機械学習できたらな...

### aのfitcondition


```python
def fitcondition_a(array, a_high, a_low):
    """a_high以上、a_low未満はNaN"""
    a = array.T[0]
    a[a > a_high] = np.nan
    a[a < a_low] = np.nan
    return a
```


```python
fitcondition_a(result, a_high=df.values.max(), a_low=0)
```




    array([ 0.22169173,  0.18287276,  2.08159926,         nan,  1.84757841,
            2.10001609,  0.5369122 ,  0.28474413,  1.14160092,  1.12007172])



### muのfitcondition


```python
def fitcondition_mu(array, mu_real, mu_tol):
    """mu_realとmuの差がmu_tol超えたらNaN"""
    mu = array.T[1]
    mu[abs(mu-mu_real) > mu_tol] = np.nan
    return mu
```


```python
fitcondition_mu(result, mu, mu*0.1)  # muの値の10%超えたらNaN
```




    array([ 213.58060554,  220.59046389,  222.43992503,  219.66157289,
                     nan,  223.55910904,  219.10993057,  220.15592395,
                     nan,  226.62842067])



### siのfitcondition


```python
def fitcondition_si(array, si_high, si_low):
    """si_realとsiの差がsi_high超えたらNaN"""
    si = array.T[2]
    si[si > si_high] = np.nan
    si[si < si_low] = np.nan
    return si
```


```python
fitcondition_si(result, si_high=80, si_low=-np.inf)
```

    C:\tools\Anaconda3\lib\site-packages\ipykernel\__main__.py:5: RuntimeWarning: invalid value encountered in less
    




    array([ 27.11764231,   0.88859971,   4.59234267,   0.26728512,
                    nan,  36.42462223,  -0.10640548,  -0.1669968 ,
                    nan,  33.04710357])



### fitcondition総合


```python
def fitcondition(array, **kwargs):
    """fitconditionすべて"""
    fitcondition_a(array, kwargs['a_high'], kwargs['a_low'])
    fitcondition_mu(array, kwargs['mu_real'], kwargs['mu_tol'])
    fitcondition_si(array, kwargs['si_high'], kwargs['si_low'])
    return array
```


```python
result
```




    array([[  2.21691725e-01,   2.13580606e+02,   2.71176423e+01,
              1.12346093e+00],
           [  1.82872764e-01,   2.20590464e+02,   8.88599712e-01,
              1.98918253e+00],
           [  2.08159926e+00,   2.22439925e+02,   4.59234267e+00,
              1.08671082e+00],
           [             nan,   2.19661573e+02,   2.67285120e-01,
              2.43258836e+00],
           [  1.84757841e+00,              nan,              nan,
             -7.69187238e-01],
           [  2.10001609e+00,   2.23559109e+02,   3.64246222e+01,
              5.40678934e-01],
           [  5.36912197e-01,   2.19109931e+02,  -1.06405484e-01,
              1.27381097e+00],
           [  2.84744125e-01,   2.20155924e+02,  -1.66996800e-01,
              1.56364664e-01],
           [  1.14160092e+00,              nan,              nan,
              2.47223917e+00],
           [  1.12007172e+00,   2.26628421e+02,   3.30471036e+01,
              5.07641118e-01]])




```python
fitcondition(result, a_high=df.values.max(), a_low=0,
             mu_real=mu, mu_tol=mu*0.1, si_high=80, si_low=-np.inf)
result
```

    C:\tools\Anaconda3\lib\site-packages\ipykernel\__main__.py:4: RuntimeWarning: invalid value encountered in greater
    C:\tools\Anaconda3\lib\site-packages\ipykernel\__main__.py:5: RuntimeWarning: invalid value encountered in less
    




    array([[  2.21691725e-01,   2.13580606e+02,   2.71176423e+01,
              1.12346093e+00],
           [  1.82872764e-01,   2.20590464e+02,   8.88599712e-01,
              1.98918253e+00],
           [  2.08159926e+00,   2.22439925e+02,   4.59234267e+00,
              1.08671082e+00],
           [             nan,   2.19661573e+02,   2.67285120e-01,
              2.43258836e+00],
           [  1.84757841e+00,              nan,              nan,
             -7.69187238e-01],
           [  2.10001609e+00,   2.23559109e+02,   3.64246222e+01,
              5.40678934e-01],
           [  5.36912197e-01,   2.19109931e+02,  -1.06405484e-01,
              1.27381097e+00],
           [  2.84744125e-01,   2.20155924e+02,  -1.66996800e-01,
              1.56364664e-01],
           [  1.14160092e+00,              nan,              nan,
              2.47223917e+00],
           [  1.12007172e+00,   2.26628421e+02,   3.30471036e+01,
              5.07641118e-01]])



### フィルタリング可視化


```python
defit??
```


```python
def defit(array):
    plt_pnt = np.apply_along_axis(lambda row: row[1],
                                  row[0]+row[3], 1, array)  # ポイントのプロットに必要な部分抜き出し
    plt_pnt_se = pd.Series(plt_pnt.T[1], index=plt_pnt.T[0])  # fitting結果をseries化
    return plt_pnt_se
```


```python
def fitplot(df, result):
    fig, ax = plt.subplots(10, sharex=True, figsize=(4,18))
    df.T.plot(color='gray', lw=.5, legend=False, subplots=True, ax=ax)  # オリジナルをプロット
    regaussdf = regauss(df, result)  # resultをregaussでガウシアンに戻す
    pd.DataFrame(regaussdf).T.plot(legend=False, subplots=True, ax=ax)  # ラインをプロット
    for nu in range(len(plt_pnt_se)):
        pl = defit(result)
        x,y=pl.index[nu], pl.iloc[nu]
        ax[nu].plot(x, y, 'D', mew=2, fillstyle='none')
```


```python
fitplot(df, result)
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    <ipython-input-120-8f2bb0ad9b5c> in <module>()
    ----> 1 fitplot(df, result)
    

    <ipython-input-118-805ba982ce93> in fitplot(df, result)
          2     fig, ax = plt.subplots(10, sharex=True, figsize=(4,18))
          3     df.T.plot(color='gray', lw=.5, legend=False, subplots=True, ax=ax)  # オリジナルをプロット
    ----> 4     regaussdf = regauss(df, result)  # resultをregaussでガウシアンに戻す
          5     pd.DataFrame(regaussdf).T.plot(legend=False, subplots=True, ax=ax)  # ラインをプロット
          6     for nu in range(len(plt_pnt_se)):
    

    <ipython-input-111-5fd08f44281b> in regauss(x, fitresult, axis)
          2     """フィッティング結果のarrayをガウシアンに適用して、
          3     ガウシアンの入ったarrayを返す"""
    ----> 4     return np.apply_along_axis(lambda row: gauss(x, *row), axis, fitresult)
    

    C:\tools\Anaconda3\lib\site-packages\numpy\lib\shape_base.py in apply_along_axis(func1d, axis, arr, *args, **kwargs)
        115         outshape[axis] = len(res)
        116         outarr = zeros(outshape, asarray(res).dtype)
    --> 117         outarr[tuple(i.tolist())] = res
        118         k = 1
        119         while k < Ntot:
    

    ValueError: could not broadcast input array from shape (10,1001) into shape (10)



![png](fit_lab_files/fit_lab_165_1.png)


___


```python
import sys
sys.path.append('../')
```


```python
from fitclass import *
```


```python
# giving initial parameters
mu = Parameter(7)
sigma = Parameter(3)
height = Parameter(5)
```


```python
# define your function:
def f(x, h=height(), mu=mu(), si=sigma()): return h * np.exp(-((x-mu)/si)**2)
```


```python
# fit! (given that data is an array with the data to fit)
data = 10*np.exp(-np.linspace(0, 10, 100)**2) + np.random.rand(100)
fitp, _ = fit(f, [mu, sigma, height], data); fitp
```




    array([ -1.89549379,  12.09140583,  11.17214325])




```python
plt.plot(data)
plt.plot(f(data, *fitp))
```




    [<matplotlib.lines.Line2D at 0xc1785f8>]




![png](fit_lab_files/fit_lab_172_1.png)



```python

```
