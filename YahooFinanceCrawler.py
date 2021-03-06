# -*- coding: utf-8 -*-
# Yahooファイナンスから過去の値を取得しCSVで表示

from HTMLParser import HTMLParser
import urllib2
import os.path

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.__table_flag = 0 # table開始フラグ
        self.__table_cnt = 0  # 何番目のtableか
        self.__th_cnt = 0     # ヘッダの列数
        self.__td_flag = 0
        self.__td_cnt = 0
        self.___csv = ""

    def getCsv(self):
        return self.___csv

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "table":
            self.__table_cnt += 1
            # 今回の汎用性の無い仕様で2番目のテーブルのみ対象にする
            if self.__table_cnt == 2:
               self.__table_flag = 1
        # 対象table内でtdタグ開始
        if self.__table_flag == 1 and tag.lower() == "td":
            self.__td_flag = 1
        # ヘッダの列数をカウント
        if self.__table_flag == 1 and tag.lower() == "th":
            self.__th_cnt += 1

    def handle_endtag(self, tag):
        # tableの終わり検出
        if tag.lower() == "table":
            self.__table_flag = 0
        # tdの終わり検出
        if tag.lower() == "td":
            self.__td_flag = 0
        # 行の終わりを検出して改行
        if tag.lower() == "tr" and self.__table_flag == 1:
            print "\n",
            self.___csv += "\n"
            self.__td_cnt = 0

    def handle_data(self, data):
        # table内でtdタグ内のデータだけ出力
        if self.__table_flag == 1 and self.__td_flag == 1:
            print data.encode('utf-8').replace(",", ""),  
            self.___csv += data.encode('utf-8').replace(",", "")
            self.__td_cnt += 1
            # 行の終わりならカンマを出力しない
            if self.__td_cnt < self.__th_cnt:
                print ",",
                self.___csv += ","


# ファイルを読み込みHTMLをパースしてCSVで出力
def output_csv(path, csvfile):
    try:
        ifp = open(path,"r")        
        parser = MyHTMLParser()
        parser.feed(unicode(ifp.read(),'utf-8'))
        ofp = open(csvfile, "w")
        ofp.write(parser.getCsv())
    except Exception, ex:
        print ex
    finally:
        parser.close()
        ifp.close()
        ofp.close()


# YahooファイナンスからHTMLを取得してファイルに出力
def get_html(code, page, htmlfile):
    ret = True
    #if os.path.isfile(htmlfile) == False:
    try:
        fp = open(htmlfile,"w")
        htmldata = urllib2.urlopen(
            "http://info.finance.yahoo.co.jp/history/?code=%s&sy=2015&sm=1&sd=1&ey=2015&em=9&ed=17&tm=d&p=%d" % (code, page))
        fp.write(htmldata.read())
    except Exception, ex:
        ret = False
        print ex
    finally:
        htmldata.close()
        fp.close()
    #else:
        #ret = False
    return ret


if __name__ == "__main__":
    import stock_insert
    import time
    code = "3319.t"
    page = 1
    htmlfile = "./tmp.html"
    csvfile = "./tmp.csv" #"./%d.csv" % (code)

    stock_insert.init_db()
    fp = open("./codelist2.txt","r")
    for line in fp:
        code = line.replace("\n","")
	if code == "":
	    continue
        for page in range(1, 10):
            print "[" + code + "]"
	    if get_html(code, page, htmlfile) == False:
		print "!!!---[" + code + "]---> get_html() error!!!"
		continue
	    else:
                output_csv(htmlfile, csvfile)
		if stock_insert.insert_data(csvfile, code) == False:
		    print "!!!---[" + code + "]---> insert_data() error!!!"
                #stock_insert.verify_test()
                os.remove(htmlfile)
                os.remove(csvfile)
	    time.sleep(1)

