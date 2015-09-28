# -*- coding: utf-8 -*-
# Yahooファイナンスから過去の値を取得しCSVで表示

from HTMLParser import HTMLParser
import urllib2
import os.path

class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self._table_flag = 0 # table開始フラグ
        self._table_cnt = 0  # 何番目のtableか
        self._th_cnt = 0     # ヘッダの列数
        self._td_flag = 0
        self._td_cnt = 0
        self._csv = ""

    def getCsv(self):
        return self._csv

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "table":
            self._table_cnt += 1
            # 今回の汎用性の無い仕様で2番目のテーブルのみ対象にする
            if self._table_cnt == 2:
               self._table_flag = 1
        # 対象table内でtdタグ開始
        if self._table_flag == 1 and tag.lower() == "td":
            self._td_flag = 1
        # ヘッダの列数をカウント
        if self._table_flag == 1 and tag.lower() == "th":
            self._th_cnt += 1

    def handle_endtag(self, tag):
        # tableの終わり検出
        if tag.lower() == "table":
            self._table_flag = 0
        # tdの終わり検出
        if tag.lower() == "td":
            self._td_flag = 0
        # 行の終わりを検出して改行
        if tag.lower() == "tr" and self._table_flag == 1:
            #print "\n",
            self._csv += "\n"
            self._td_cnt = 0

    def handle_data(self, data):
        # table内でtdタグ内のデータだけ出力
        if self._table_flag == 1 and self._td_flag == 1:
            #print data.encode('utf-8').replace(",", ""),  
            self._csv += data.encode('utf-8').replace(",", "")
            self._td_cnt += 1
            # 行の終わりならカンマを出力しない
            if self._td_cnt < self._th_cnt:
                #print ",",
                self._csv += ","


# ファイルを読み込みHTMLをパースしてCSVで出力
def output_csv(path, csvfile):
    ret = True
    try:
        ifp = open(path,"r")        
        parser = MyHTMLParser()
        parser.feed(unicode(ifp.read(),'utf-8'))
        ofp = open(csvfile, "w")
        ofp.write(parser.getCsv())
        parser.close()
        ifp.close()
        ofp.close()
    except Exception, ex:
        ret = False
        print ex
    finally:
        #parser.close()
        #ifp.close()
        #ofp.close()
        pass
    return ret

# YahooファイナンスからHTMLを取得してファイルに出力
def get_html(code, page, htmlfile):
    ret = True
    #if os.path.isfile(htmlfile) == False: # ファイルがあったら上書き
    try:
        fp = open(htmlfile,"w")
        htmldata = urllib2.urlopen(
            "http://stocks.finance.yahoo.co.jp/stocks/history/?code=%s" % (code))
        fp.write(htmldata.read())
        htmldata.close()
        fp.close()
    except Exception, ex:
        ret = False
        print ex
    finally:
        #fp.close()
        #htmldata.close() # close()で例外引いたので
        pass
    #else:
        #ret = False
    return ret


# Today's update
if __name__ == "__main__":
    import stock_insert
    import time
    code = "3319.t"
    page = 1
    htmlfile = "./tmp.html"
    csvfile = "./tmp.csv" 

    stock_insert.init_db()
    fp = open("./codelist.txt","r")
    for line in fp:
        code = line.replace("\n","")
        if code == "":
            continue
        print "[" + code + "]"
        if get_html(code, page, htmlfile) == False:
            print "!!!---[" + code + "]---> get_html() error!!!"
            continue
        if output_csv(htmlfile, csvfile) == False:
            print "!!!---[" + code + "]---> output_csv() error!!!"
            continue
        
        # 最新の値(1行目)だけをDBに登録
        if stock_insert.insert_data_1row(csvfile, code) == False:
            print "!!!---[" + code + "]---> insert_data() error!!!"

        #stock_insert.verify_test()
        #os.remove(htmlfile)
        #os.remove(csvfile)
        #time.sleep(1)
    os.remove(htmlfile)
    os.remove(csvfile)

