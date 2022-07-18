from IPython.display import display
import investpy

code = "1301"

start = "01/01/2000" #2000年初
end = "31/12/2021" #2021年末


#★ここが最重要。「investpy.get_stock_historical_data」だと過去の私の判断と同じように・・★
search_result = investpy.search_quotes(text=code, countries=["japan"], products=["stocks"], n_results=1)

historical_data = search_result.retrieve_historical_data(from_date=start, to_date=end)

print(historical_data.shape) #約20年分なので6千弱日のデータが取れてればOK
display(historical_data.head(2)) #最初2日
display(historical_data.tail(2)) #最後2日

