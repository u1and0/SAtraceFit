## ____________________________
## substr.gp ver1.0
##gnuplotでファイル名やらディレクトリパスを取得する文字列変換式郡
##[gnuplotの便利な文字列関数](http://www.ss.scphys.kyoto-u.ac.jp/person/yonezawa/contents/program/gnuplot/string_function.html)で定義された関数を使って、gnuplot上でファイル名やディレクトリパスの取得を行う。
## <<改造予定>>
## help打ち込んで関数の説明標準出力に出せないかなぁ
## ____________________________







## __substr_str_before(str, target)__________________________
## strの中でtargetよりも前の部分文字列を返す
## ____________________________
substr_str_before(str, target)=substr(str, 1, strstrt(str,target)-1)

# print sprintf("ドライブ名は   %s",substr_str_before(ARG0,":"))
##__実行結果__________________________
##	ドライブ名は   C
## ____________________________







## __substr_str_after(str, target)__________________________
## strの中でtargetよりも後の部分文字列を返す
## ____________________________
substr_str_after(str, target)=substr(str, strstrt(str,target)+strlen(target), strlen(str))

# print sprintf("ドライブ名を除いたパスは   %s",substr_str_after(ARG0,"\\"))
##__実行結果__________________________
##	ドライブ名を除いた部分は   home\gnuplot\WhereamI.gp
## ____________________________







## __strsubst_sub(str, index, target, subst)__________________________
## 再帰表現を利用して、strのindexより後の文字列のtargetをsubstに全て置換する
## ____________________________
strsubst_sub(str, index, target, subst)=\
	strstrt(str[index:],target)==0 ? str :\
	strsubst_sub( str[:index-1] . substr_str_before(str[index:],target) . \
	subst . substr_str_after(str[index:],target),\
	index+strstrt(str[index:],target)+strlen(subst)-strlen(target),target, subst)

# print sprintf("バックスラッシュをスラッシュに変えたパスは   %s",strsubst_sub(ARG0,1,"\\","/"))
## __実行結果__________________________
##	バックスラッシュをスラッシュに変えたパスは   C:/home/gnuplot/WhereamI.gp
## ____________________________







## __strstrlt(str,target)__________________________
## デフォルト関数`strstrt(str,target)`は最初の場所を返すのに対して
## 文字列strの中でtargetの最後に出てくる場所を返す
## ____________________________
#大きい方の値を返す関数を補助的に定義
max(x,y)= ( (x) > (y) ) ? (x) : (y)
# strのindexより後の文字列の中でtargetが最後に出てくる場所を返す
strstrlt_sub(str,index,target)=(strstrt(str[index:],target)==0 ? \
	max(index-strlen(target),0) : \
	strstrlt_sub(str, index-1+strstrt(str[index:],target)+strlen(target),target))
# strの中でtargetが最後に出てくる場所を返す
strstrlt(str,target)=strstrlt_sub(str,1,target)






## __dirname(path)__________________________
## 文字列pathからディレクトリ名を返す。
## ____________________________
dirname(path)=strstrt(path, "\\")!= 0 ? substr(path, 1, strstrlt(path,"\\")-1) : ""

# print sprintf("ディレクトリパスは   %s",dirname(ARG0))
## __実行結果__________________________
##	ディレクトリパスは   C:\home\gnuplot
##____________________________






##__remdirname(path)__________________________
##文字列pathからディレクトリ名を消したものを返す。
##____________________________
remdirname(path)=substr(path,strstrlt(path,"\\")+1,strlen(path))

# print sprintf("ファイル名は   %s",remdirname(ARG0))
## __実行結果__________________________
##	ファイル名は   WhereamI.gp
##____________________________



##__remext(path)__________________________
##文字列pathから拡張子を消したものを返す。
##____________________________
remext(filename)=strstrt(filename, ".")==0 ? filename : substr(filename,1,strstrlt(filename, ".")-1)

# print sprintf("ファイルベースネームは   %s",remext(remdirname(ARG0)))
## __実行結果__________________________
##	ファイルベースネームは   WhereamI
##____________________________
# print sprintf("拡張子は   %s",substr_str_after(ARG0,remext(remdirname(ARG0))))
## __実行結果__________________________
##	拡張子は   .gp
##____________________________
