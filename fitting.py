'''
## fitting.py

__INTRODUCTION__
タイムスタンプと周波数を引数にフィッティング結果を返すpy

__ACTION__
引数:filebasename:タイムスタンプのこと。例えば'2015年01月01日12時35分06秒'を表す'20150101_123506'
    freqWave:帯域を持つ周波数のリスト
    freqCarrier:帯域を持たない周波数のリスト
戻り値:タプル形式
    1. SNのディクショナリ in ディクショナリ形式のフィッティング結果{タイムスタンプ:{周波数1:出力1,周波数2:出力2,...}}
    2. Powerのディクショナリ in ディクショナリ形式のフィッティング結果{タイムスタンプ:{周波数1:出力1,周波数2:出力2,...}}


1. データをテキスト形式で読み込みdataにリストとして読み込み
2. freqで指定した周波数の分だけfittingを行い
3. データとフィッティング曲線をプロットする
4. waveに格納された周波数をfittingする
5. waveとしてみるか判断(OKだったらプロット)>>>indicatecondition
6. carrierに格納された周波数をfittingする
7. carrierとしてみるか判断(OKだったらプロット)
8. ノイズフロアをプロット
9. 測定データのプロット
10. pngを吐き出す(オプションでプロットして表示)
11. ディクショナリ in ディクショナリを返す

__TODO__
* plotshowing()
    * plotするかしないか
    * showするかsavepngするか
    * 条件分岐
    * dictionary使う？inputでmain.py空の命令に従う
* fittingされてreturnするdictをプロット
    * `plt.plot(dictionary.keys(), dictionary.keys(), dictionary.values()) `
'''

# BUILTIN PACKAGE
import numpy as np
from scipy import stats
from scipy import optimize
import matplotlib.pyplot as plt
import os
import datetime
# INSTALL PACKAGE
import simplejson
from tqdm import tqdm
from more_itertools import chunked
# USER PACKAGE
import listdic

# __PARAMETER DEFINITION__________________________
with open('parameter.json', 'r') as pa:
    param = simplejson.load(pa)


def freq2pnt(x): return int((x * 1000 - 22000) / 4)  # integer使わないと将来的にエラーが起きるというwarning出される


def pnt2freq(x): return (x * 4 + 22000) / 1000


def plotshowing(title, ext=None, dir='./'):
    '''
    ext(拡張子)を指定すると保存する拡張子を指定できる
    デフォルトは標準出力(pyplot)
    dir(ディレクトリ)を指定すると保存するディレクトリを指定できる
    デフォルトはワーキングディレクトリ
    '''
    plt.title(datetime.datetime.strptime(title, '%Y%m%d_%H%M%S'))
    # plt.legend(loc='best',fancybox=True,fontsize='small')
    plt.legend(bbox_to_anchor=(0.5, -0.25), loc='center',
               borderaxespad=0, fontsize='small', ncol=3)
    plt.subplots_adjust(bottom=0.25)
    plt.xlabel('Frequency[kHz]')
    plt.ylabel('Power[dBm]')
    plt.grid(True)
    plt.ylim(ymin=-120, ymax=0)
    switch = 'plt.show()' if not ext else 'plt.savefig(dir+title+"."+ext)'
    eval(switch)


def loaddata(dataname):
    '''
    ファイル名を引数にデータをロードし、返す
    また、データのプロットも行う(plotshowはしない)
    '''
    data = np.loadtxt(dataname)  # load text data as array
    r = (datax, datay) = (data[:, 0], data[:, 2])
    return r


def fitting(dataname, plot_switch=True):
    (datax, datay) = loaddata(dataname)

    noisef = stats.scoreatpercentile(datay, 25)  # fix at 1/4median

    def gauss(x, *param):  # fitting function
        [aa, mu, si] = param
        return aa * np.exp(-(x - mu)**2 / 2 / si**2) + noisef

    def gaussfit(x, y, mu):
        parameter_initial = [0, freq2pnt(mu), 0.3]  # fitting初期値aa,mu,si
        paramater_optimal, covariance = optimize.curve_fit(
            gauss, x, y, p0=parameter_initial, maxfev=100000000)
        rtnvalue = (gauss(datax, *paramater_optimal),
                    paramater_optimal[0],
                    pnt2freq(paramater_optimal[1]),
                    abs(paramater_optimal[2]))
        '''rtnvalueの要素
        1. フィッティング結果(リスト)
        2. SN比
        3. フィッティング周波数
        4. 帯域幅'''
        return rtnvalue

    def SNextract(x, y):
        '''SNやシグナルのマーカーの表示
        ディクショナリに値を追加'''
        plt.plot(x, y, 'D', fillstyle='none', markeredgewidth=1.5, label=str(
            freqFit) + param['country'].get(str(freqFit), ' UNK'))  # fitting結果のプロット
        if type(freqFit) == tuple:
            k = 0  # ラベルの添え字
            for i in freqFit:
                SNDict[str(freqFit) + '_' + str(k) + 'kHz'] = y - \
                    noisef  # 周波数をキー、SN比を値にしてfittngDictへ入れる
                powerDict[str(freqFit) + '_' + str(k) + 'kHz'] = y  # 周波数をキー、SN比を値にしてfittngDictへ入れる
                k += 1
        else:
            SNDict[str(freqFit) + 'kHz'] = y - noisef  # 周波数をキー、SN比を値にしてfittngDictへ入れる
            powerDict[str(freqFit) + 'kHz'] = y  # 周波数をキー、SN比を値にしてfittngDictへ入れる

    def fitcondition(freqFit,
                     SNratio,
                     fittingFreqFit,
                     waveWidth,
                     condSN=5,
                     condwavewidthmin=1,
                     condwavewidthmax=100,
                     condmu=0.05):
        '''
        フィッティングされた周波数とフィッティングするはずの周波数のずれが50Hz以内
        幅が0~100の間に入るとき、正常なガウシアン
         '''
        return (SNratio > condSN
                and condwavewidthmin < waveWidth < condwavewidthmax
                and abs(freqFit - fittingFreqFit) < condmu)

    plt.figure(figsize=(6, 6))
    SNDict, powerDict = {}, {}
    # __WAVE FIT__________________________
    for freqFit in tqdm(param['freqWave']):  # freqWaveの周波数をfit
        fitrange = 0.2
        datax_range = listdic.around(datax, freqFit, fitrange, freq2pnt)  # ±200Hzをフィッティングする
        datay_range = listdic.around(datay, freqFit, fitrange, freq2pnt)  # ±200Hzをフィッティングする
        [fity, SNratio, fittingFreqFit, waveWidth] = list(
            gaussfit(datax_range, datay_range, freqFit))
        if fitcondition(freqFit, SNratio, fittingFreqFit, waveWidth):
            SNextract(fittingFreqFit, SNratio + noisef)

    # __CARRIER FIT__________________________
    for freqFit in param['freqCarrier']:  # freqCarrierの周波数のシグナルを取得
        datax_range = listdic.around(datax, freqFit, 0.01, freq2pnt)  # ±10Hzを抜き出し
        datay_range = listdic.around(datay, freqFit, 0.01, freq2pnt)  # ±10Hzを抜き出し
        datadict = dict(zip(pnt2freq(datax_range), datay_range))
        # 2つのリスト(それぞれの要素同士は対応しているはず)をディクショナリ形式にする
        xpower = listdic.search_maxy_returnx(datadict)  # 大きいほう
        power = datadict[xpower]

        # poww=datay[freq2pnt(freqFit)]
        if power - noisef > 10:  # SN比が10以上ならCarrierが出ているとみなす
            SNextract(xpower, power)  # 大きいほうの値をextract
        # if poww-noisef>10:    #SN比が10以上ならCarrierが出ているとみなす
        #   SNextract(freqFit,poww)

    # __M FIT__________________________
    for freqFit in chunked(param['freqM'], 2):  # freqMの周波数のシグナルを取得
                                                # chunkedでリストを2個ずつにまとめる
        zipx0 = pnt2freq(listdic.around(datax, freqFit[0], 0.02, freq2pnt))
        zipy0 = listdic.around(datay, freqFit[0], 0.02, freq2pnt)
        datadict0 = dict(zip(zipx0, zipy0))
        xpower0 = listdic.search_maxy_returnx(datadict0)
        power0 = datadict0[xpower0]

        zipx1 = pnt2freq(listdic.around(datax, freqFit[1], 0.02, freq2pnt))
        zipy1 = listdic.around(datay, freqFit[1], 0.02, freq2pnt)
        datadict1 = dict(zip(zipx1, zipy1))

        xpower1 = (min(datadict1.items(), key=lambda x: abs(x[1] - power0))[0])
        power1 = datadict1[xpower1]
        # datadict1をキーと値でタプルにして
        # 要素の1番目(ディクショナリの値)を比較して
        # min(power0との差が最も小さい)ところの
        # タプルの第0要素を返す

        avefit = np.mean(freqFit)
        fitrange = 0.2
        datax_range = listdic.around(datax, avefit, fitrange, freq2pnt)  # ±200Hzをフィッティングする
        datay_range = listdic.around(datay, avefit, fitrange, freq2pnt)  # ±200Hzをフィッティングする
        [fity, SNratio, fittingFreqFit, waveWidth] = list(
            gaussfit(datax_range, datay_range, avefit))
        if fitcondition(avefit,
                        SNratio,
                        fittingFreqFit,
                        waveWidth,
                        condwavewidthmin=1,
                        condSN=-5,
                        condmu=0.2) and power0 - noisef > 5 and power1 - noisef > 5:
            SNextract(xpower0, power0)
            SNextract(xpower1, power1)

    # __MAKE RETURN DATA__________________________
    SNData, powerData = {}, {}
    filebasename = os.path.basename(dataname)[:-4]
    # ファイル名(=タイムスタンプ)をキーに、SNDictを値にSNDataへ入れる
    SNData[datetime.datetime.strptime(filebasename, '%Y%m%d_%H%M%S')] = SNDict
    # ファイル名(=タイムスタンプ)をキーに、powerDictを値にpowerDataへ入れる
    powerData[datetime.datetime.strptime(filebasename, '%Y%m%d_%H%M%S')] = powerDict
    outData = [SNData, powerData]
    # print('SN: %s\npower: %s'% (SNData,powerData))

    if plot_switch:  # 引数がTrueならプロット
        plt.plot(pnt2freq(datax), [noisef for i in datax], '-', lw=1, color='k')  # ノイズフロアのプロット
        plt.plot(pnt2freq(datax), datay, '-', lw=0.2, color='k')  # 測定データのプロット
        # extは拡張子指定オプション(デフォルトはplt.show())、dirは保存するディレクトリ指定オプション
        plotshowing(filebasename, ext='png', dir=param['out_png'])
    plt.close()
    return outData
