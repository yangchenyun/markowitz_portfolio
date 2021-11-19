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
    return df

def from_yf(tickers, from_date, to_date, interval='weekly', sample=True):
    yahoo_financials = YahooFinancials(tickers)
    raw_data = yahoo_financials.get_historical_price_data(start_date=from_date,
                                                          end_date=to_date,
                                                          time_interval=interval)
    result = []
    for a in tickers:
        for x in raw_data[a]['prices']:
            result += [[x['formatted_date'], a, x['adjclose']]]

    df = pd.DataFrame(np.array(result), columns=column_names)
    df['date'] = df['date'].astype('datetime64')
    df['adj_close'] = df['adj_close'].astype('float64')
    df = df.set_index('date')
    return df
