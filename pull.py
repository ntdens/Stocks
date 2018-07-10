import argparse as ag
from datetime import date, timedelta
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import plotly.offline as py
import plotly.graph_objs as go
from tabulate import tabulate


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
    plot = parser.add_mutually_exclusive_group()
    plot.add_argument('--plot-line', action='store_true', help='Creates a line graph of the data')
    plot.add_argument('--plot-ohlc', action='store_true', help='Creates OHLC graphs of the data')
    plot.add_argument('--plot-combined', action='store_true', help='Creates combined OHLC and line graphs of the data')
    plot.add_argument('--plot-table', action='store_true', help='Creates a table based on the data')
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

    ohlc = {}
    mulstock = {}
    tick = []
    for ticker in index:
        ts = TimeSeries(key='603MDIJGG9TGNV60', output_format='pandas')
        data, metadata = ts.get_daily(symbol='{}'.format(ticker))
        df = data
        df = df.drop(['5. volume'], axis=1)
        df = df.rename(
            columns={'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close'})
        ohlc[ticker] = go.Ohlc(
            x=df.index,
            open=df.Open,
            high=df.High,
            low=df.Low,
            close=df.Close,
            name=ticker)
        df = df.transpose()
        df['Stocks'] = ticker
        df.index.name = 'Price'
        df = df.set_index(['Stocks', df.index])
        df = df.transpose()
        df.index.name = 'Date'
        mulstock[ticker] = df
        tick.append(ticker)

    stocks = pd.DataFrame()
    for k in mulstock:
        if stocks.empty:
            stocks = mulstock[k]
        else:
            stocks = stocks.join(mulstock[k])
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

    if args.plot_line:
        stocks = stocks.transpose()
        line = stocks.xs('Open', level='Price')
        line = line.transpose()
        py.plot({
            "data": [go.Scatter(
                x=line.index,
                y=line[col],
                name=col)
                for col in line.columns],
            "layout": go.Layout(title="Daily Openings")
        }, auto_open=True)

    if args.plot_ohlc:
        for k in ohlc:
            layout = go.Layout(
                title=k,
                xaxis = dict(
                rangeslider=dict(
                    visible=False
                    )
                )
            )
            stock_update = go.Ohlc(x=stocks.index)
            ohlc[k].update(stock_update)
            data = [ohlc[k]]
            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename=str(k) + '.html', auto_open=True)

    if args.plot_combined:
        dataline = {}
        for k in tick:
            layout = go.Layout(
                title=k,
                xaxis = dict(
                rangeslider=dict(
                    visible=False
                    )
                )
            )
            stock_update = go.Ohlc(x=stocks.index)
            ohlc[k].update(stock_update)
            dataline[k] = go.Scatter(
                x=stocks.index,
                y=stocks[k, "Open"],
                name= 'Trend',
                line={'shape': 'spline', 'smoothing': 1})
            data = [ohlc[k], dataline[k]]
            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename=str(k) + '.html', auto_open=True)


    if args.plot_table:
        print(tabulate(stocks, tablefmt='psql'))

if __name__ == '__main__':
    main()
