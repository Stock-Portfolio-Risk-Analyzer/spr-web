import ystockquote
import pandas as pd
import pandas_datareader.data as web
from collections import OrderedDict
from datetime import datetime as dt


def get_stock_data(symbol, start_date=None, end_date=None):
    """
    Get OHLC stock data from Yahoo Finance for a single stock
    :param symbol: string
    :param start_date: datetime
    :param end_date: datetime
    :return: DataFrame of stock data from start_date to end_date
    """
    if start_date is None:
        start_date = dt(year=1990, month=1, day=1)

    if end_date is None:
        end_date = dt.today()

    if start_date is not None and end_date is not None:
        assert start_date < end_date, "Start date is later than end date."

    # log.info("Loading symbol: {}".format(symbol))
    symbol_data = web.DataReader(symbol, 'yahoo', start_date, end_date)

    return symbol_data


def get_stock_data_multiple(symbols=None, start_date=None, end_date=None):
    """
    Get OHLC stock data from Yahoo Finance for multiple stocks
    :param symbols: list of symbols (strings)
    :param start_date: datetime
    :param end_date: datetime
    :return: OrderedDict of DataFrames of stock data from start_date to end_date
    """
    data = OrderedDict()

    if symbols is not None:
        for symbol in symbols:
            symbol_data = get_stock_data(symbol, start_date, end_date)
            data[symbol] = symbol_data

    return data


def get_pct_returns(symbol, start_date=None, end_date=None, col='Adj Close'):
    """

    :param symbol:
    :param start_date:
    :param end_date:
    :param col: (string) name of column to calculate the pct returns from
    :return:
    """
    data = get_stock_data(symbol, start_date, end_date)[col]
    return data.pct_change().fillna(0)


def get_returns(symbol, start_date=None, end_date=None, col='Adj Close'):
    """

    :param symbol:
    :param start_date:
    :param end_date:
    :param col:  (string) name of column to calculate the returns from
    :return:
    """
    data = get_stock_data(symbol, start_date, end_date)[col]
    return data.diff().fillna(0)


def get_options_data_yahoo(symbols=None, start_date=None, end_date=None):
    raise NotImplementedError()


def get_current_price(symbol):
    """
    Get the latest price!
    :param symbol:
    :return:
    """
    quote = ystockquote.get_price(symbol)
    if quote == 'N/A':
        return None
    return float(quote)


def get_company_name(symbol):
    """
    Get the full name of the company by the symbol
    :param symbol:
    :return:
    """
    df = pd.read_csv('secwiki_tickers.csv')
    company_info = df[df.Ticker==symbol]
    code = company_info['Name'].keys()[0]
    company_sector = company_info.to_dict()['Name'][code]
    return company_sector



def get_company_sector(symbol):
    """
    Get the sector of the company
    :param symbol: (str)
    :return: (str)
    """
    df = pd.read_csv('secwiki_tickers.csv')
    company_info = df[df.Ticker==symbol]
    code = company_info['Name'].keys()[0]
    company_sector = company_info.to_dict()['Sector'][code]
    return company_sector


