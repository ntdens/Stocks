import argparse as ag
from datetime import date, timedelta
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import plotly.offline as py
import plotly.graph_objs as go


def main():
    parser = ag.ArgumentParser(prog='pull', description='Pulls stock data from AlphaVantage.co')
    parser.add_argument('--stocks', nargs='*', help='Enter a list of stock tickers', metavar='XXX',
                        default=['T', 'ATVI', 'MSFT'])
    parser.add_argument('--start-date', help='Enter a starting date in the YYYY-MM-DD format', dest='start')
    parser.add_argument('--end-date', help='Enter a ending date in the YYYY-MM-DD format', dest='end')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--mode-high', action='store_true', help='Prints out the highest price reached during the period')
    mode.add_argument('--mode-low', action='store_true', help='Prints out the lowest price reached during the period')
    mode.add_argument('--mode-last', action='store_true', help='Prints out the most recent price')
    mode.add_argument('--mode-earliest', action='store_true', help='Prints out the earliest date')
    mode.add_argument('--mode-change', action='store_true',
                      help='Prints out the change between the last and the earliest')
    mode.add_argument('--mode-all', action='store_true', help='Prints all of the above')
    args = parser.parse_args()
    index = args.stocks
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
        ts = TimeSeries(key='603MDIJGG9TGNV60', output_format='pandas')
        data, metadata = ts.get_daily(symbol='{}'.format(ticker))
        df = data
        df = df.drop(['2. high', '3. low', '4. close', '5. volume'], axis=1)
        df = df.rename(columns={'1. open': ticker})
        if stocks.empty:
            stocks = df
        else:
            stocks = stocks.join(df)

    stocks = stocks.loc[start_date:end_date]
    print(stocks)

    if args.mode_high:
        print('Peak Values:')
        print(stocks.max())

    if args.mode_low:
        print('Lowest Values:')
        print(stocks.min())

    if args.mode_last:
        print('Latest Values:')
        print(stocks.iloc[0])

    if args.mode_earliest:
        print('Earliest Values:')
        print(stocks.iloc[-1])

    if args.mode_change:
        print('Change in Values:')
        stocks.loc['Change'] = stocks.iloc[0] - stocks.iloc[-1]
        print(stocks.loc['Change'])

    if args.mode_all:
        print('Peak Values:')
        print(stocks.max())
        print('Lowest Values:')
        print(stocks.min())
        print('Latest Values:')
        print(stocks.iloc[0])
        print('Earliest Values:')
        print(stocks.iloc[-1])
        print('Change in Values:')
        stocks.loc['Change'] = stocks.iloc[0] - stocks.iloc[-1]
        print(stocks.loc['Change'])

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
