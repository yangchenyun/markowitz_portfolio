import pandas as pd
import numpy as np

import quandl
import yfinance as yf
from yahoofinancials import YahooFinancials

# Get API key from quandl.com
quandl.ApiConfig.api_key = 'z-ZRHshTiaYCFv3MpYwY'

column_names = ['date', 'ticker', 'adj_close']


def from_nasdaq(tickers, from_date, to_date, sample=True):
    """
    tickers: []str
    from_date: str, yyyy-mm-dd
    to_date: str, yyyy-mm-dd
    """
    # None sample data requires subscription
    table_name = 'WIKI/PRICES' if sample else 'QUOTEMEDIA/PRICES'
    data = quandl.get_table(table_name,
                            ticker = tickers,
                            qopts = { 'columns': column_names },
                            date = { 'gte': from_date, 'lte': to_date },
                            paginate=True)
    df = data.set_index('date')
    table = df.pivot(columns='ticker')
    # By specifying col[1] in below list comprehension
    # You can select the stock names under multi-level column
    table.columns = [col[1] for col in table.columns]
    return table

def from_yf(tickers, from_date, to_date, interval='1d', sample=True):
    data = yf.download(tickers, interval=interval, start=from_date, end=to_date)
    # pick only adj_close
    data = data.xs('Adj Close', level=0, axis=1)
    return data
