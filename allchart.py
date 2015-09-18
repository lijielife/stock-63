#!/usr/bin/env python2.7
# -*- coding: utf-8 -*- 
# 東証のコード2700件分のチャートを取得する 
# 読み込むコードファイルは、codelist.txt（\n区切り）

import urllib
import urllib2
import os.path
import sys
import argparse
import time
from HTMLParser import HTMLParser
from datetime import datetime as dt


def download(code, outpath):
    # 期間6か月
    url="http://chart.yahoo.co.jp/?code=%s&tm=6m&type=c&log=off&size=m&over=m65,m130,s&add=v&comp="
    # 期間1年
    #url="http://chart.yahoo.co.jp/?code=%s&tm=1y&type=c&log=off&size=m&over=m65,m130,s&add=v&comp="
    img = urllib.urlopen(url % (code))
    localfile = open("%s/%s.%s.png" % (outpath, code, dt.now().strftime('%Y%m%d')),'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()

class codeParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self,tagname,attribute):
	detail = "http://stocks.finance.yahoo.co.jp/stocks/detail/?code="
        if tagname.lower() == "a":
            for i in attribute:
		if i[0].lower() == "href" and detail in i[1]:  
		    code_url=i[1].replace(detail,"",1)
                    # 取得したコード集めたファイルの作成
		    print code_url
                    f = open("codelist.txt","a")
                    #f.write("%s\t"%code_url)
                    f.write("%s\n"%code_url)
                    f.close()
		    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--outpath", required=False
	#, default="/tmp"
	, default="/vagrant/img"
        ,help="output path")
    parser.add_argument("-u","--url", required=False
	,default=0, type=int
        ,help=
	"urlno Stop high=0,Stop depreciation=1,Price rise=2,Fall in prices=3,Golden=4,Dead=5")
    args = parser.parse_args()

    # 銘柄コード収集URL
    serch_url = [
        # STOP高銘柄 Stop high
        #"http://info.finance.yahoo.co.jp/ranking/?kd=27&mk=1&tm=d&vl=a",
        # STOP安銘柄 Stop depreciation
        #"http://info.finance.yahoo.co.jp/ranking/?kd=28&mk=1&tm=d&vl=a",
        # 値上がり上位 Price rise
        #"http://info.finance.yahoo.co.jp/ranking/?kd=1&mk=1&tm=d&vl=a",
        # 値下がり上位 Fall in prices
        #"http://info.finance.yahoo.co.jp/ranking/?kd=2&mk=1&tm=d&vl=a",
	# Golden cross
	#"http://info.finance.yahoo.co.jp/ranking/?kd=37&mk=1&tm=d&vl=a",
        # Dead cross
	#"http://info.finance.yahoo.co.jp/ranking/?kd=38&mk=1&tm=d&vl=a",
	# All 
	"http://info.finance.yahoo.co.jp/ranking/?kd=46&mk=2&tm=d&vl=a&p=%d"
    ]
    
    # 生成したファイルの読み込み
    f = open("codelist.txt","r")
    row = f.read()
    f.close()
    #row_url = row.split('\n')
    #len_url = len(row_url)
    number_url = []
    number_url = row.split('\n')
    len_url = len(number_url)
    

    #for i in range(0,(len_url-1)):
    #    print("row=[%d] code=[%s]" % (i, row_url[i]))
    #    print("len=%d" % (len_url))
    #quit()

    #number_url = []

    #for i in range(0,(len_url-1)):
    #    number_url.append(row_url[i])

    for j in range(0,(len_url-1)):
        url = number_url[j]
        download(url, args.outpath)

    print('チャートのダウンロードが終了しました。')

    # ファイルの削除
    #os.remove("collection_url.txt")

