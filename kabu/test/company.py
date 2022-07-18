#
# [invest.py ライブラリ] を用い、ブルームバーグデータより各種株価データを取得し、ＣＳＶを出力する
#
# （準備） コマンドラインより pip install investpy を実行し、investpyをインストール
# （実行方法）コマンドラインより、python3 [当ソースファイル名] を実行する
#
# （input.csv）入力となる企業コード
# （output.csv）作成されるcsvファイル
#
import investpy
import os,csv
import time

csv_buf = [] # CSV出力用の2次元配列

# 証券コードcsvファイルを読み込み、ループしながら1行ごとに処理を行う
with open('input.csv', encoding='shift_jis') as f:
  reader = csv.reader(f)
  header = next(reader) # ヘッダを読み飛ばす
  for row in reader:
    s_code = row[0] # input.csvから取得した証券コード（出力時の補足情報として使用）
    c_name = row[1] # input.csvから取得した企業名（出力時の補足情報として使用）

    # 各種株価データを取得する(3番目のパラメータ： json=true)
    data = investpy.get_stock_information(s_code,'japan',True)
    print(data)
    # 財務諸表(PL)の取得
    pl_data = investpy.stocks.get_stock_financial_summary(s_code, 'japan',
    summary_type='income_statement', period='annual')

    # 財務諸表(BS)の取得
    bs_data = investpy.stocks.get_stock_financial_summary(s_code, 'japan',
    summary_type='balance_sheet', period='annual')

    # サーバからブロックされないよう1企業の取得毎に 1.5秒間 waitする
    time.sleep(1.5)
   
    # 売上高（Total Revenue）
    total_revenue = round(pl_data.iloc[0]['Total Revenue'])

    # 粗利益（Gross Profit）
    gross_profit = round(pl_data.iloc[0]['Gross Profit'])

    # 営業利益（Operating Income）
    operation_income = round(pl_data.iloc[0]['Operating Income'])

    # 当期利益（Net Income）
    net_income = round(pl_data.iloc[0]['Net Income'])

    # 総資産（Total Assets）
    total_assets = round(bs_data.iloc[0]['Total Assets'])

    # 総負債（Total Liabilities）
    total_liabilities = round(bs_data.iloc[0]['Total Liabilities'])

    # 純資産（Total Equity）
    total_equity = round(bs_data.iloc[0]['Total Equity'])

    # 自己資本比率（株主資本÷総資産）を計算する (100%に換算)
    equity_ratio = round(((total_equity / total_assets) * 100) , 1)

    # ROE（当期利益÷株主資本）を計算する (100%に換算)
    roe = round(((net_income / total_equity) * 100 ), 1) 

    # ROA（当期利益÷総資産）を計算する (100%に換算)
    roa = round(((net_income / total_assets) * 100 ), 1) 

    # 株価終値
    close_val = round(data['Prev. Close'])

    # 時価総額（Market Cap） 単位（億円）
    market_cap = round(data['Market Cap']/100000000)

    # 発行済株式数（Shares Outstanding）
    shares_outstanding = round(data['Shares Outstanding'])

    # EPS
    eps = data['EPS']
    
    # 配当金（Dividend）利回り（Yield）と同時に取得されるため分割する
    dividend = 0
    if data['Dividend (Yield)'] != 'N/A(N/A)':
      split_data = data['Dividend (Yield)'].split('(')
      dividend = float(split_data[0])

    # 配当利回り（株価÷配当金）を計算する   (100%に換算)
    dividend_yield = round(dividend /close_val * 100, 2) 

    # PER（P/E Ratio）
    per = round(data['P/E Ratio'],1)

    # 益回りを計算する
    profit_margin = round((100 / per), 1)

    # PBR（時価総額÷純資産）を計算する
    pbr = round((data['Market Cap']/1000000) / total_equity, 2)

    # PBRの逆数を計算する
    pbr_reciprocal = round((100 / pbr), 2)

    # スコア1（ROE x 益回り x 自己資本）
    score1 = round((roe * profit_margin * equity_ratio))

    # スコア2（ROE + 益回り + 自己資本）
    score2 = round((roe + profit_margin + equity_ratio), 1)

    # スコア3（ROE x PBR逆数 x 自己資本）
    score3 = round((roe * pbr_reciprocal * equity_ratio))

    # スコア4（ROE + PBR逆数 + 自己資本）
    score4 = round((roe + pbr_reciprocal + equity_ratio), 1)


    # デバッグ用
    # print("証券コード = " + str(s_code))
    # print("企業名 = " + str(c_name))
    # print('株価 = ' + str(close_val))
    # print('EPS = ' + str(eps))
    # print('PER = ' + str(per))
    # print('益回り = ' + str(profit_margin) )
    # print('ROE = ' +  str(roe))
    # print('自己資本比率 = ' +  str(equity_ratio))
    # print('score1(ROE x 益回り x 自己資本) = ' +  str(score1))
    # print('score1(ROE + 益回り + 自己資本) = ' +  str(score2))

    # CSV 出力用レコード
    rec = [s_code,c_name,close_val,market_cap,shares_outstanding,total_revenue,gross_profit,operation_income,net_income,
    total_assets,total_liabilities,total_equity,eps,dividend,dividend_yield,per,profit_margin,
    pbr,pbr_reciprocal,roe,roa,equity_ratio,score1,score2,score3,score4]
    # レコードを1行、2次元配列へ追加
    csv_buf.append(rec)

#print(csv_buf)

# CSVファイルを上書きモード(w)でオープン
f = open('output.csv', mode="w", newline="",encoding="utf_8_sig")
writer = csv.writer(f)

# CSVヘッダの出力
writer.writerow(['コード', '企業名', '株価','時価総額（億）','発行済株式数','売上高（百万）','粗利益','営業利益','当期利益',
 '総資産','総負債','純資産','EPS', '配当金','配当利回り','PER', '益回り', 'PBR','PBR逆数','ROE','ROA',
'自己資本比率', 'ROEx益回りx自己資本', 'ROE+益回り+自己資本','ROExPBR逆数x自己資本','ROE+PBR逆数+自己資本'])   

# 2次元配列を取り出し、CSVファイルへ1行ずつ書き込み
for data in csv_buf:
    writer.writerow(data)
f.close()    