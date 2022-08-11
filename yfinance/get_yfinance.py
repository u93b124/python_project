#
# [yfinance ライブラリ] を用い、ヤフーファイナンスデータより各種株価データを取得し、ＣＳＶを出力する
#
# （準備） コマンドラインより pip install yfinance を実行し、yfinanceをインストール
# （実行方法）コマンドラインより、python3 [当ソースファイル名] を実行する
#
# （input.csv）入力となる企業コード
# （output.csv）作成されるcsvファイル
# （err.csv）処理中にエラーが発生した企業についてはここに出力する


# ライブラリの読み込み
import yfinance as yf
import os,csv
import time
import traceback

csv_buf     = [] # CSV出力用の2次元配列
csv_err_buf = [] #エラーファイル用の2次元配列
i = 0        # 処理件数表示用カウンタ

# 証券コードcsvファイルを読み込み、ループしながら1行ごとに処理を行う
with open('input/input.csv', encoding='shift_jis') as f:
  reader = csv.reader(f)
  header = next(reader) # ヘッダを読み飛ばす

  # エラーファイルのオープン
  err_f = open('output/err.csv', mode="w", newline="",encoding="utf_8_sig")
  
  for row in reader:
    # 処理件数の表示用
    i = i + 1
    print('------------------------------------------------------------')
    print('- ' + str(i) + ' 件目')
    print('------------------------------------------------------------')

    s_code = row[0] # input.csvから取得した証券コード（出力時の補足情報として使用）
    c_name = row[1] # input.csvから取得した企業名（出力時の補足情報として使用）

    try:
      # 全体情報を取得する  
      ticker_info = yf.Ticker(s_code+'.T')

      # PL情報を取得する
      pl_info = ticker_info.financials

      # PLのキー情報を取得する
      str_keys = pl_info.keys() 

      # 4年分取得されてしまうため、直近のPL情報を取得する
      pl_info_now = pl_info[str_keys[0]]

      # 売上高（totalRevenue）
      total_revenue = pl_info_now['Total Revenue']

      # 粗利益（Gross Profit）　6178など粗利益が存在しない企業もある
      if pl_info_now['Gross Profit'] == None:
        gross_profit = '-'
      else:  
        gross_profit = pl_info_now['Gross Profit'] 
      
      # 営業利益（Operating Income）
      if pl_info_now.get('Operating Income') == None:
        operation_income = '-'
      else:
        operation_income = pl_info_now['Operating Income']

      # 当期利益（Net Income）
      net_income = pl_info_now['Net Income']

      # BS情報を取得する
      bs_info = ticker_info.balance_sheet

      # BSのキー情報を取得する
      str_keys = bs_info.keys() 

      # 4年分取得されてしまうため、直近のBS情報を取得する
      bs_info_now = bs_info[str_keys[0]]
   
      # 総資産（Total Assets）
      total_assets = bs_info_now['Total Assets']

      # 総負債（Total Liab）
      total_liabilities = bs_info_now['Total Liab']

      # 純資産（Total Stockholder Equity）
      total_equity = bs_info_now['Total Stockholder Equity']

      # 自己資本比率（株主資本÷総資産）を計算する (100%に換算)
      equity_ratio = round(((total_equity / total_assets) * 100) , 1)

      # ROE（当期利益÷株主資本）を計算する (100%に換算)
      if ( net_income > 0 )  and ( total_equity > 0 ):
        roe = round(((net_income / total_equity) * 100 ), 1) 
      else:
        roe = 0

      # ROA（当期利益÷総資産）を計算する (100%に換算)
      if ( net_income > 0 ) or ( total_assets > 0 ):
        roa = round(((net_income / total_assets) * 100 ), 1) 
      else:
        roa = 0

      # 会社概要を取得する
      company_info = ticker_info.info

      # 株価終値
      close_val = company_info['currentPrice']

      # 時価総額（marketCap） 単位（億円）
      market_cap = round(company_info['marketCap'] / 100000000)

      # 発行済株式数（sharesOutstanding）
      shares_outstanding = company_info['sharesOutstanding']

      # EPS（当期純利益 ÷ 発行済株式数）
      eps = round( (net_income / shares_outstanding), 2 )
      
      # 配当金（lastDividendValue）
      if company_info['lastDividendValue'] == None:
        dividend = 0
      else: 
        dividend = company_info['lastDividendValue']

      # 配当利回り（株価÷配当金）を計算する   (100%に換算)
      dividend_yield = round((dividend /close_val) * 100, 2) 

      # PER（株価 ÷ EPS)
      per = round((close_val / eps), 2)

      # 益回りを計算する
      profit_margin = round((100 / per), 1)

      # PBR（時価総額÷純資産）を計算する
      pbr = round( (company_info['marketCap'] / total_equity ), 2)

      # PBRの逆数を計算する
      if pbr > 0:
        pbr_reciprocal = round((100 / pbr), 2)
      else:
        pbr_reciprocal = 0
      
      # スコア1（ROE x 益回り x 自己資本）
      score1 = round((roe * profit_margin * equity_ratio))

      # スコア2（ROE + 益回り + 自己資本）
      score2 = round((roe + profit_margin + equity_ratio), 1)

      # スコア3（ROE x PBR逆数 x 自己資本）
      score3 = round((roe * pbr_reciprocal * equity_ratio))

      # スコア4（ROE + PBR逆数 + 自己資本）
      score4 = round((roe + pbr_reciprocal + equity_ratio), 1)


      # デバッグ用
      print("証券コード = " + str(s_code))
      print("企業名 = " + str(c_name))
      print('株価 = ' + str(close_val))
      print('時価総額 = ' + str(market_cap))
      print('EPS = ' + str(eps))
      print('PER = ' + str(per))
      print('益回り = ' + str(profit_margin) )
      print('ROE = ' +  str(roe))
      print('自己資本比率 = ' +  str(equity_ratio))
      print('score1(ROE x 益回り x 自己資本) = ' +  str(score1))
      print('score1(ROE + 益回り + 自己資本) = ' +  str(score2))

      # CSV 出力用レコード
      rec = [s_code,c_name,close_val,market_cap,shares_outstanding,total_revenue,gross_profit,operation_income,net_income,
      total_assets,total_liabilities,total_equity,eps,dividend,dividend_yield,per,profit_margin,
      pbr,pbr_reciprocal,roe,roa,equity_ratio,score1,score2,score3,score4]
      # レコードを1行、2次元配列へ追加
      csv_buf.append(rec)

    except Exception as e:
      print('-----------------------------------------------')
      print('investpy取得エラー ' + s_code + ' ' + c_name)
      print(traceback.format_exc())
      print('-----------------------------------------------')
      # エラーファイルへ書き込み
      err_writer = csv.writer(err_f)
      err_writer.writerow(['investpy取得エラー',s_code,c_name,e]) 
      err_writer.writerow([traceback.format_exc()])

    # サーバからブロックされないよう1企業の取得毎に 1.5秒間 waitする
    time.sleep(1.5)
   
#print(csv_buf)

# CSVファイルを上書きモード(w)でオープン
f = open('output/output.csv', mode="w", newline="",encoding="utf_8_sig")
writer = csv.writer(f)

# CSVヘッダの出力
writer.writerow(['コード', '企業名', '株価','時価総額（億）','発行済株式数','売上高（百万）','粗利益','営業利益','当期利益',
 '総資産','総負債','純資産','EPS', '配当金','配当利回り','PER', '益回り', 'PBR','PBR逆数','ROE','ROA',
'自己資本比率', 'ROEx益回りx自己資本', 'ROE+益回り+自己資本','ROExPBR逆数x自己資本','ROE+PBR逆数+自己資本'])   

# 2次元配列を取り出し、CSVファイルへ1行ずつ書き込み
for data in csv_buf:
    writer.writerow(data)
f.close()

# エラーファイルクローズ
err_f.close()