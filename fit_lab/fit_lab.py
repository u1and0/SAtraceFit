
# coding: utf-8

# # 自作ガウシアン

# In[9]:

def gauss(x, a, mu, si):
    """
    a: 最大値
    mu: 位置
    si: 線幅
    noisef: 最低値
    """
    return aa * np.exp(-(x - mu)**2 / 2 / si**2) + noisef


# In[13]:

noisef=0.5
n=1001
x = np.linspace(0,100,n)
a, mu, si = 1, 50, 1


# In[21]:

g= gauss(x, a, mu, si); g


# In[22]:

plt.plot(x, g)


# ## 自作ガウシアンじゃなくてscipy.stats.normを使うべきでは

# In[15]:

from  scipy.stats import norm


# In[23]:

z=norm.pdf(x, loc=50, scale=1)-0.5; z


# In[25]:

plt.plot(x,z)


# In[39]:

a, mu, si=1, 50, 1
df=pd.DataFrame({'norm': a*norm.pdf(x, loc=mu, scale=si)+noisef,
                 			'gauss': gauss(xx, a, mu, si)})
df.plot(style=['-', '--'])


# ## norm vs my_gauss
# normでも自作gaussでも中でnp使っているんで実行速度あんま変わらないだろうとテスト

# In[26]:

get_ipython().magic('timeit gauss(x, a, mu, si)')


# In[27]:

get_ipython().magic('timeit norm.pdf(x, loc=50, scale=1)-0.5')


# 自作ガウスのほうが早い…！

# ## ガウシアンに沿ってノイズを作る
# 
# ということで自作のガウシアンを使っていきます。

# In[50]:

g = gauss(x, a, mu, si)
gnoise = g + 0.1 * np.random.randn(n)


# ノイズを発生させる

# In[55]:

plt.plot(x, gnoise, '-')
plt.plot(x, g,'b-' )


# ## カーブフィッティングをかけて、ノイズをフィッティングする
# 
# gからgnoiseを導き出したのだけれども、ここで急にgを未知の関数とみなしてしまう。
# 今あなたはgnoiseだけを知っていて、gのような関数を得たいとき、どうするか。
# 
# こういう時はカーブフィットを取る。
# scipy.optimizeからcurve_fitをインポートしてくる。

# In[59]:

from scipy.optimize import curve_fit


# 次にフィッティングパラメータを定める。

# In[60]:

(a_, mu_, si_), _ = curve_fit(gauss, x, gnoise, (aa, mu, si))
yfit = gauss(x, a_, mu_, si_)


# In[58]:

plt.plot(xx, gnoise, '-')
plt.plot(xx, yfit, 'b-') 


# さっきと同じグラフに見えるが、描いているのはgではなくyfitであることに注意
# 
# 同じグラフに見えるということはフィッティングできたということ。
# 
# ノイズgnoiseをカーブフィットの引数に、aa_ ,

# In[41]:

curve_fit(gauss, xx, g, )


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

# ランダムデータフレームの作成

# In[107]:

r=np.random.rand
df=pd.DataFrame([gauss(xx, r(), 10*_, 10*r()) + 0.1 * np.random.randn(n) for _ in range(10)]).T
df.plot()


# In[108]:

df


# In[114]:

f=lambda x: curve_fit(gauss, xx, x, (aa, mu, si), maxfev = 100000000)


# In[115]:

fit_param, convariance = df.apply(f)


# In[ ]:

fit_


# In[ ]:



