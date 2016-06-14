'''
## yesno.py ver1.0

__UPDATE1.0__
First commit

__USAGE__
別のpythonファイルから読み出すか、testする
testはコメントアウトはずしてbuildするだけ

__INTRODUCTION__
コマンドライン上のユーザー入力(y/n)またはキーボードインタラプション(ctrl+c)を判断する

__ACTION__
判断した結果を返す

__TODO__
None
'''


import sys

def yesno(message):
	result = ''
	sys.stdout.write(message)
	sys.stdout.flush()
	try:
		while True:
			char = sys.stdin.read(1)
			if char == 'y' or char == 'Y':
				result = 'y'
				break
			elif char == 'n' or char == 'N':
				result = 'n'
				break
	except KeyboardInterrupt:
		result = '^C'
	# print(result)
	return result

'''TEST
result = yesno('よろしいですか? (y/n) ')
if result == 'y':
	print('[Y]が押された')
elif result == 'n':
	print('[N]が押された')
elif result == '^C':
	print('[Ctrl]+[C]が押された')
'''