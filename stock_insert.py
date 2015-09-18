#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime

# データベースファイル名
# SQLiteのデータストアは単一のファイルである。
DBNAME = "stock.sqlite3"

# データベースの準備
def init_db():
    conn = sqlite3.connect(DBNAME)
    try:
        # テーブルを作成する
        conn.executescript(
            """create table stock(
            code varchar(8),
            day date,
            opening integer,
            hight integer,
            low integer,
            closing integer,
            volume integer,
            finally integer,
            remarks text);""")
        conn.executescript("""create index code_idx on stock(code);""")
        conn.executescript("""create index day_idx on stock(day);""")
        conn.executescript("""create unique index stock_idx on stock(day,code);""")

    except Exception, ex:
        # 作成に失敗したら、作成済みと想定してスルー
        #conn.commit()
        pass
    finally:
        conn.close()


# データをSqlite3に登録
def insert_data(csvfile, code):
    ret = True
    # csvfileを読み込み
    ifp = open(csvfile,"r")
    # ロックのタイムアウトは、10秒に設定。
    conn = sqlite3.connect(DBNAME, timeout=10000)
    # 1件づつ暗黙でコミットする。（Autocommit）
    conn.isolation_level = None
    try:
        cur = conn.cursor()
        try:
            column = []
            for line in ifp:
                column = line.split(',')
                if column[0] == "\n":
                    print "row is empty."
                    continue
                dt = datetime.strptime(column[0], "%Y年%m月%d日")
                cur.execute("""insert into stock(code, day, opening, hight, low, closing, 
                    volume, finally) values(?,?,?,?,?,?,?,?)"""
                    ,(code,dt,column[1],column[2],column[3], column[4],column[5]
                    ,column[6].replace("\n","")))    
        finally:
            cur.close()
    except Exception, ex:
	ret = False
        # タイムアウト時間までにロックを獲得できなかった場合は例外が発生する。
        print "insert error=%s" % (str(ex))
    finally:
        conn.close()
        ifp.close()
    return ret


# 書き込み結果の表示
def verify_test():
    conn = sqlite3.connect(DBNAME)
    try:
        cur = conn.cursor()
        try:
            cur.execute("select count(*) from stock")
            cnt = cur.fetchone()[0]
            print "count=%d" % cnt
            cur.execute("""select code, count(code) from stock
                group by code order by code""")
            for row in cur:
                print row
        finally:
            cur.close()
    except Exception, ex:
        print ex
    finally:
        conn.close()


# テスト用コード
if __name__ == "__main__":
    csvfile = "test.csv"
    code = "3319"
    init_db()
    ret = insert_data(csvfile,code)
    verify_test()

