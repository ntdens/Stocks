import pandas as pd
import plotly
import plotly.offline as py
import cufflinks as cf
import plotly.graph_objs as go
import ipywidgets as widgets
import numpy as np

stocks = pd.read_csv('CME-FCK2019.csv')
print(stocks)
py.plot({
    "data": [go.Scatter(x=stocks.Date, y=stocks.Change)],
    "layout": go.Layout(title="Change Over Time")
}, auto_open=True)
