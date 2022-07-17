import investpy

# 証券コード
code = "3695"

# 財務諸表(PL)の取得
pl_data = investpy.stocks.get_stock_financial_summary(code, 'japan',
summary_type='income_statement', period='annual')
#print(pl_data)
#print(pl_data.iloc[0])

# 当期利益（Net Income）
net_income = pl_data.iloc[0]['Net Income']
#print("当期利益 =  " + str(net_income))

# 財務諸表(BS)の取得
bs_data = investpy.stocks.get_stock_financial_summary(code, 'japan',
summary_type='balance_sheet', period='annual')
#print(bs_data)

# 株主資本（Total Equity）
total_equity = bs_data.iloc[0]['Total Equity']
#print("株主資本 =  " + str(total_equity))

# 総資産（Total Assets）
total_assets = bs_data.iloc[0]['Total Assets']
#print("総資産 =  " + str(total_assets))

# 自己資本比率（株主資本÷総資産）を計算する (100%に換算)
equity_ratio = round(((total_equity / total_assets) * 100) , 1)
#print('自己資本比率 = ' +  str(equity_ratio))

# ROE（当期利益÷株主資本）を計算する (100%に換算)
roe = round(((net_income / total_equity) * 100 ), 1) 
#print('ROE = ' +  str(roe))

# 株価データを取得する(3番目のパラメータ： json=true)
data = investpy.get_stock_information(code,'japan',True)
#print(data)

# EPS
eps = data['EPS']
#print('EPS = ' + str(eps))

# 株価終値
close_val = round(data['Prev. Close'])
#print('株価 = ' + str(close_val))

# PER（終値 ÷ EPS） を計算する
per = round((data['Prev. Close'] / data['EPS']) , 1)
#print('PER = ' + str(per))

# 益回りを計算する
profit_margin = round((100 / per), 1)
#print('益回り = ' + str(profit_margin) )

# スコア1（ROE x 益回り x 自己資本）
score1 = round((roe * profit_margin * equity_ratio))
#print('score1(ROE x 益回り x 自己資本) = ' +  str(score1))

# スコア2（ROE + 益回り + 自己資本）
score2 = round((roe + profit_margin + equity_ratio), 1)
#print('score1(ROE + 益回り + 自己資本) = ' +  str(score2))

# デバッグ用
print('株価 = ' + str(close_val))
print('EPS = ' + str(eps))
print('PER = ' + str(per))
print('益回り = ' + str(profit_margin) )
print('ROE = ' +  str(roe))
print('自己資本比率 = ' +  str(equity_ratio))
print('score1(ROE x 益回り x 自己資本) = ' +  str(score1))
print('score1(ROE + 益回り + 自己資本) = ' +  str(score2))