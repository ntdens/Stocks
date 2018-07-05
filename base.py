import pandas as pd
import plotly
import plotly.offline as py
import plotly.graph_objs as go

stocks = pd.read_csv('CME-FCK2019.csv')
stocks.set_index('Date', inplace=True)
price = stocks.drop(columns=['Change','Volume','Previous Day Open Interest'])
print(price)
py.plot({
    "data": [go.Scatter(
        x=price.index,
        y=price[col],
        name= col)
        for col in price.columns],
    "layout": go.Layout(title="Change Over Time")
}, auto_open=True)

