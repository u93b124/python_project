import investpy
import os,csv
import time

csv_buf = []

# 証券コードcsvファイルを読み込み、ループしながら1行ごとに処理を行う
with open('test.csv') as f:
  reader = csv.reader(f)
  header = next(reader) # ヘッダを読み飛ばす
  for row in reader:
    #print(row)
    s_code = row[0] # CSVから取得した証券コード
    c_name = row[1] # CSVから取得した企業名

    # 株価データを取得する(3番目のパラメータ： json=true)
    data = investpy.get_stock_information(s_code,'japan',True)

    # 財務諸表(PL)の取得
    pl_data = investpy.stocks.get_stock_financial_summary(s_code, 'japan',
    summary_type='income_statement', period='annual')

    # 財務諸表(BS)の取得
    bs_data = investpy.stocks.get_stock_financial_summary(s_code, 'japan',
    summary_type='balance_sheet', period='annual')

    # サーバからブロックされないよう 1.5秒間 waitする
    time.sleep(1.5)

    # 当期利益（Net Income）
    net_income = pl_data.iloc[0]['Net Income']

    # 株主資本（Total Equity）
    total_equity = bs_data.iloc[0]['Total Equity']

    # 総資産（Total Assets）
    total_assets = bs_data.iloc[0]['Total Assets']

    # 自己資本比率（株主資本÷総資産）を計算する (100%に換算)
    equity_ratio = round(((total_equity / total_assets) * 100) , 1)

    # ROE（当期利益÷株主資本）を計算する (100%に換算)
    roe = round(((net_income / total_equity) * 100 ), 1) 

    # EPS
    eps = data['EPS']

    # 株価終値
    close_val = round(data['Prev. Close'])
    #print('株価 = ' + str(close_val))

    # PER（終値 ÷ EPS） を計算する
    per = round((data['Prev. Close'] / data['EPS']) , 1)

    # 益回りを計算する
    profit_margin = round((100 / per), 1)

    # スコア1（ROE x 益回り x 自己資本）
    score1 = round((roe * profit_margin * equity_ratio))

    # スコア2（ROE + 益回り + 自己資本）
    score2 = round((roe + profit_margin + equity_ratio), 1)

    # デバッグ用
    print("証券コード = " + str(s_code))
    print("企業名 = " + str(c_name))
    print('株価 = ' + str(close_val))
    print('EPS = ' + str(eps))
    print('PER = ' + str(per))
    print('益回り = ' + str(profit_margin) )
    print('ROE = ' +  str(roe))
    print('自己資本比率 = ' +  str(equity_ratio))
    print('score1(ROE x 益回り x 自己資本) = ' +  str(score1))
    print('score1(ROE + 益回り + 自己資本) = ' +  str(score2))

    # CSV 出力用レコード
    rec = [s_code,c_name,close_val,eps,per,profit_margin,roe,equity_ratio,score1,score2]
    # レコードを1行、2次元配列へ追加
    csv_buf.append(rec)

print(csv_buf)

# CSVファイルを上書きモード(w)でオープン
f = open('output.csv', mode="w", newline="",encoding="utf_8_sig")
writer = csv.writer(f)

# CSVヘッダの出力
writer.writerow(['コード', '企業名', '株価', 'EPS', 'PER', '益回り', 'ROE',
'自己資本比率', 'ROEx益回りx自己資本', 'ROE+益回り+自己資本'])   

# 2次元配列を取り出し、CSVファイルへ1行ずつ書き込み
for data in csv_buf:
    writer.writerow(data)
f.close()    