import investpy
import os,csv
import time

s_code = "1375"

# 各種株価データを取得する(3番目のパラメータ： json=true)
#data = investpy.get_stock_information(s_code,'japan',True)
#print(data)

# 財務諸表(PL)の取得
pl_data = investpy.stocks.get_stock_financial_summary(s_code, 'japan',
summary_type='income_statement', period='annual')

print(pl_data)