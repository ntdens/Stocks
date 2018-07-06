import pandas as pd
import requests
import plotly.offline as py
import plotly.graph_objs as go
import io
import argparse as ag
from datetime import date, timedelta

def main():
    parser = ag.ArgumentParser(prog='pull', description='Pulls stock data from AlphaVantage.co')
    parser.add_argument('stocks',nargs='*',help='Enter a comma separated list of stock tickers',metavar='XXX',default='T,ATVI,MSFT')
    parser.add_argument('--start-date',help='Enter a starting date in the YYYY-MM-DD format',dest='start')
    parser.add_argument('--end-date', help='Enter a ending date in the YYYY-MM-DD format', dest='end')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--mode-high', help='Prints out the highest price reached during the period')
    mode.add_argument('--mode-low', help='Prints out the lowest price reached during the period')
    mode.add_argument('--mode-last',help='Prints out the most recent price')
    mode.add_argument('--mode-earliest', help='Prints out the earliest date')
    mode.add_argument('--mode-change',help='print out the change between the last and the earliest')
    mode.add_argument('--mode-all', help='Prints all of the above')
    args = parser.parse_args()
    index = args.stocks.split(',')
    start_date = args.start
    if not start_date:
        start_date = date.today() - timedelta(days=1)
        start_date = start_date.strftime('%Y-%m-%d')
    end_date = args.end
    if not end_date:
        end_date = date.today()
        end_date = end_date.strftime('%Y-%m-%d')


    stocks = pd.DataFrame()
    for ticker in index:
        r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&datatype=csv&apikey=603MDIJGG9TGNV60'.format(ticker)).content
        df = pd.read_csv(io.StringIO(r.decode()))
        df.set_index('timestamp', inplace=True)
        df = df.drop(['high', 'low', 'close', 'volume'], axis=1)
        df = df.rename(columns={'open': ticker})
        if stocks.empty:
            stocks = df
        else:
            stocks = stocks.join(df)


    stocks.index = pd.to_datetime(stocks.index)
    print (stocks.loc[end_date:start_date])


#    py.plot({
#        "data": [go.Scatter(
#            x=stocks.index,
#            y=stocks[col],
#            name=col)
#            for col in stocks.columns],
#        "layout": go.Layout(title="Daily Openings")
#    }, auto_open=True)

if __name__ == '__main__':
    main()


