import plotly.graph_objects as go
import sqlite3

file_sqlite3 = "./japan_stock_price.db"
conn = sqlite3.connect(file_sqlite3)
df=pd.read_sql_query('SELECT * FROM price', conn)

toyota_df = df[df['code']==str(7203)]#TOYOTAのみ抜粋
display(toyota_df.head(2)) #抜粋したDFを確認(2行)

fig = go.Figure(
    data=[go.Candlestick(x=toyota_df["Date"], 
                         open=toyota_df["Open"], 
                         high=toyota_df["High"], 
                         low=toyota_df["Low"], 
                         close=toyota_df["Close"], 
                         name="TOYOTA")]
)

fig.show()
