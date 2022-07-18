# resuests モジュールをインポート
import requests
# Pandas モジュールをインポート
import pandas as pd
# タイムモジュールをインポート
import time
import datetime as dt
import sqlite3
import investpy

#東証のHPより東証上場銘柄一覧情報を取得し、Excelで保存
url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
r = requests.get(url)
with open('data_j.xls', 'wb') as output:
    output.write(r.content)

#Excelをデータフレームで開く
stocklist = pd.read_excel("./data_j.xls")

#日本の指数(225,トピ,マザーズ,ジャスダック,東証REIT,日経VI)
index_list_jp = ['JP225', 'TOPX', 'MTHR', 'NOTC', 'TREIT', 'JNIV']

#指定した日本の指数とデータフレームからコード部分をlist化して統合する
index_list_jp.extend(stocklist['コード'].tolist())

#米国指数(ダウ,sp500,ナス,ラッセル,ドル円,vix,WTI)
index_list_us = ['DJI', 'SPX', 'IXIC', 'RUT', 'USD/JPY', 'VIX', 'T'] 


### 株価/ポイント取得関数 ###
def get_brand(code, country):
    try:

        #print('code = ' + str(code))
        #print('country = ' + str(country))
    
        start = pd.to_datetime('2000/01/01').strftime("%d/%m/%Y") #取得開始日
        end = dt.date.today().strftime("%d/%m/%Y") #取得終了日

        #print('aa')
        if country=='jp': #日本関係のデータ
            #print('bb')
            data = investpy.search_quotes(text=str(code), countries=["japan"], n_results=1)
            print('data jp = ' + str(data))
        elif country=='us': #US関係のデータ(ダウ等)
            #print('cc')
            data = investpy.search_quotes(text=code, countries=["united states"], n_results=1)
            print('data us = ' + str(data))

        #ヒストリカルデータ取得
        historical_data = data.retrieve_historical_data(from_date=start, to_date=end)

        df = historical_data.reset_index()
        df = df.assign(code=code) #証券コードをデータフレームに統合

        print(str(code)+'取得完了') #デバッグ用の正常取得完了通知

    except:
        print(str(code)+'は存在しません') #万が一取得できなかった場合の把握通知
        return None

    return df


### データフレーム操作関数 ###
def brands_generator(index_list_jp, index_list_us):

    #空のデータフレーム作成
    cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Change Pct', 'code']
    df = pd.DataFrame(index=[], columns=cols)

    #まずJP関連を取得
    for code in index_list_jp:        

        brand = get_brand(code, 'jp') #引数にJP
        #情報が取得できていれば、情報を結合していく
        if brand is not None:
            df = pd.concat([df, brand]).reset_index(drop=True)

        #1.5秒間プログラムを停止する(Block対策)
        time.sleep(1.5)

    #同様にUS関連を取得
    for code in index_list_us:
        brand = get_brand(code, 'us') #引数にUS    
        if brand is not None:
            df = pd.concat([df, brand]).reset_index(drop=True)

        time.sleep(1.5)

    return df



#作成したJPとUSの証券コードを引数で関数へ渡してデータフレーム取得
df = brands_generator(index_list_jp, index_list_us)

#データベースを作成
db = sqlite3.connect('japan_stock_price.db', isolation_level=None)
#priceテーブルに収集したデータフレームを格納する
df.to_sql('price', db, if_exists='append', index=None, method='multi', chunksize=5000)




