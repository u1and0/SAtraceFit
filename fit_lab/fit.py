"""特定周波数(axis=1方向)のfittingまとめ"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import scoreatpercentile
r = np.random


def gauss(x, a, mu, si, nf):
    """
    a: 最大値
    mu: 位置
    si: 線幅
    noisef: 最低値
    """
    return a * np.exp(-(x - mu)**2 / 2 / si**2) + nf


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
    x, y = series.index, series.values
    nf = scoreatpercentile(series, 25)
    cfshape = (4,)
    try:
        cf = curve_fit(gauss, x, y, p0=(a, mu, si, nf))
    except Exception as e:
        errcount += 1
        print('error', errcount, ':', e)  # エラー数, エラーメッセージの表示
        cf = np.full(cfshape, np.nan), np.nan  # エラー起きたらnan返す
    return cf


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


def waves(seed: int=np.random.randint(100), rows=10):
    """ランダムノイズを発生させたウェーブを作成する
    引数: seed: ランダムステートを初期化する整数。デフォルトでseedをランダムに発生させる
    戻り値: noisedf.sum(1): pd.Series型"""
    r = np.random
    r.seed(seed)  # ランダム初期化
    x = np.linspace(1, 10, 1001)
    xa = np.tile(x, (rows, 1))
    aa = abs(r.randn(rows))
    mua = np.linspace(min(x), max(x), rows)
    sia = abs(r.randn(rows))
    nf = 0.01 * r.randn(rows)

    df = pd.DataFrame(gauss(xa.T, aa, mua, sia, nf))
    noisedf = df + 0.05 * r.randn(*df.shape)
    return noisedf.sum(1)


def fit_df(df, center: float, span: float, param: tuple):
    """pandas.DataFrameに対してガウシアンフィッティング
    引数:
        center, span: 抜き出す中心周波数, 幅
        param: a, mu, siの初期値
            a: 最大値
            mu: 位置
            si: 線幅
    戻り値:
        result: フィッティング結果のarray(np.array型)
            要素数: 0, 1, 2, 3 = a, mu, si nf(ノイズフロア) """
    dfe = df.apply(choice, axis=1, args=(center, span))  # dfからcenter,spanで取り出す
    fita = dfe.apply(fit, axis=1, args=param)  # フィッティング # param = a, mu, si
    result = np.array([i[0] for i in fita])  # タプルの第一要素だけを取り出しarray化
    return result


def regauss(x, fitresult, axis=1):
    """フィッティング結果のarrayをガウシアンに適用して、
    ガウシアンの入ったarrayを返す"""
    return np.apply_along_axis(lambda row: gauss(x, *row), axis, fitresult)


# def defit(row):
#     """return fitting result as plot point"""
#     return row[1], row[0] + row[3]
def defit(array):
    plt_pnt = np.apply_along_axis(lambda x: (x[1], x[0] + x[3]), 1, array)  # ポイントのプロットに必要な部分抜き出し
    plt_pnt_se = pd.Series(plt_pnt.T[1], index=plt_pnt.T[0])  # fitting結果をseries化
    return plt_pnt_se


def fitplot(df, result):
    fig, ax = plt.subplots(len(df), sharex=True, figsize=(4, 18))
    df.T.plot(color='gray', lw=.5, legend=False, subplots=True, ax=ax)  # オリジナルをプロット
    pd.DataFrame(regauss(df.columns, result)).T.plot(
        legend=False, subplots=True, ax=ax)  # resultをregaussでガウシアンに戻す
    for nu in range(len(df)):
        pl = defit(result)
        x, y = pl.index[nu], pl.iloc[nu]
        ax[nu].plot(x, y, 'D', mew=2, fillstyle='none')


# __FITTING CONDITION__________________________


def fitcondition_a(array, a_high, a_low):
    """a_high以上、a_low未満はNaN"""
    a = array.T[0]
    a[a > a_high] = np.nan
    a[a < a_low] = np.nan
    return a


def fitcondition_mu(array, mu_real, mu_tol):
    """mu_realとmuの差がmu_tol超えたらNaN"""
    mu = array.T[1]
    mu[abs(mu - mu_real) > mu_tol] = np.nan
    return mu


def fitcondition_si(array, si_high, si_low):
    """si_realとsiの差がsi_high超えたらNaN"""
    si = array.T[2]
    si[si > si_high] = np.nan
    si[si < si_low] = np.nan
    return si


def fitcondition(array, **kwargs):
    """fitconditionすべて"""
    fitcondition_a(array, kwargs['a_high'], kwargs['a_low'])
    fitcondition_mu(array, kwargs['mu_real'], kwargs['mu_tol'])
    fitcondition_si(array, kwargs['si_high'], kwargs['si_low'])
    return array


# ____________________________


if __name__ == '__main__':
    df = pd.DataFrame([waves(i) for i in range(10)])
    df.index = pd.date_range('20160101', periods=len(df), freq='H')

    # TEST1
    # for mu in range(600, 800, 10):
    #     print('# TEST', mu, '\n', fit_df(df, center=mu, span=200, param=(df[mu].max(), mu, 1)))

    # TEST2
    mu = 560
    result = fit_df(df, center=mu, span=200, param=(df[mu].max(), mu, 1))
    fitcondition(result, a_high=df.values.max(), a_low=0,
                 mu_real=mu, mu_tol=mu * 0.1, si_high=80, si_low=-np.inf)
    print(result)

    fitplot(df, result)
    plt.show()
