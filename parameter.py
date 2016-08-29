'''
## confidential.py ver2.3

__UPDATE2.3__
関数country追加

__UPDATE2.2__
returnを短く書いた
リネーム
	root>>>out
	rootroot>>>root

__UPDATE2.1__
SAtraceGraph用のルートディレクトリ: root()
SAtraceFit用のルートディレクトリ: rootroot()
住み分けをした
root()には穴埋め用ダミーデータがある
rootroot()にはない

__UPDATE2.0__
帯域持った波とキャリアのみの波を分けた

__INTRODUCTION__
データの入ったrootディレクトリと注目する周波数を指定するpy

__ACTION__
関数入れているだけ

__USAGE__
root():データの入ったrootディレクトリ
引数:なし
戻り値:rootPath(文字列)
 
freq() : 注目する周波数を指定する
引数 : なし
戻り値 : freqWave(リスト)

__PLAN__
none
'''

# def out():return '\\\\sampanet.gr.jp\\DFS\\ShareUsers\\UserTokki\\Personal\\Maeno\\VLFsasebo\\'

# def freqWave():	return [22.2,23.4,24.0,24.5,24.8,25.2]   #帯域持った周波数

# def freqCarrier():return [23.0,24.1,25.0,25.1,25.5]   #キャリアのみの周波数

# def freqM():return [(23.8,24.0)]   #キャリアのみの周波数

def country(x):
	'''
	国名と電波形式のディクショナリを指定する
	引数の周波数に対して国名と電波形式の文字列を返す
	'''
	country={22.2:' JPN',23.4:' GER' ,24.0:' USA-ME' ,24.5:' UNK' ,24.8:' USA-WA' ,25.2:' USA-ND' ,23.0:' RUS' ,24.1:' CHN' ,25.0:' RUS' ,25.1:' RUS' ,25.5:' RUS',(23.8,24.0):'UNK'}
	rtn=country[x]
	return rtn

# def root():return '\\\\sampanet.gr.jp\\DFS\\ShareUsers\\UserTokki\\Common\\VLFtrace\\Common\\VLFtrace\\data4\\trace\\'

def param():
	return {
	'in':'\\\\sampanet.gr.jp\\DFS\\ShareUsers\\UserTokki\\Common\\VLFtrace\\Common\\VLFtrace\\data4\\trace\\',
	'out':'\\\\sampanet.gr.jp\\DFS\\ShareUsers\\UserTokki\\Personal\\Maeno\\VLFsasebo\\',
	'freqWave':[22.2,23.4,24.0,24.5,24.8,25.2],   #帯域持った周波数
	'freqCarrier':[23.0,24.1,25.0,25.1,25.5],   #キャリアのみの周波数
	'freqM':[(23.8,24.0)]   #キャリアのみの周波数
	}
