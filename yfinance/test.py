# ライブラリの読み込み
import yfinance as yf

# 証券コードを指定する
# 日本株の場合は、証券コードの最後に'.T'を付ける
# トヨタ7203の場合は、'7203.T'となる
s_code = '1821'

# 指定の証券コードの情報を取得する
ticker_info = yf.Ticker(s_code+'.T')

# 会社概要を取得する
company_info = ticker_info.info
print(company_info)

# BS情報を取得する
bs_info = ticker_info.balance_sheet

# BSのキー情報を取得する
str_keys = bs_info.keys() 
#print(str_keys)

# 4年分取得されてしまうため、直近のBS情報を取得する
bs_info_now = bs_info[str_keys[0]]
#print(bs_info_now)

# 株価終値
close_val = company_info['currentPrice']




