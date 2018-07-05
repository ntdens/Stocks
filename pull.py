import pandas as pd
import requests
import plotly.offline as py
import plotly.graph_objs as go
import io

index = ['MU','GE','AMD','BAC']


def main():
    stocks = pd.DataFrame()
    i = 0
    while i < len(index):
        r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + str(
            index[i]) + '&datatype=csv&apikey=603MDIJGG9TGNV60').content
        df = pd.read_csv(io.StringIO(r.decode()))
        df.set_index('timestamp', inplace=True)
        df = df.drop(columns=['high', 'low', 'close', 'volume'])
        df = df.rename(columns={'open': str(index[i])})
        if stocks.empty:
            stocks = df
        else:
            stocks = stocks.join(df)
        i += 1

    py.plot({
        "data": [go.Scatter(
            x=stocks.index,
            y=stocks[col],
            name=col)
            for col in stocks.columns],
        "layout": go.Layout(title="Daily Openings")
    }, auto_open=True)

if __name__ == '__main__':
    main()


