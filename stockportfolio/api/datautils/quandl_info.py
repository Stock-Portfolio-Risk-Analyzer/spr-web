from collections import OrderedDict
from datetime import datetime as dt

import Quandl as qd

quandl_key = '-6X6UvP1aeit_zybGREM'

""" Helper methods over the Quandl api"""


def get_stock_data(symbol, start_date=None, end_date=None, db_code="WIKI"):
    """
    Get OHLC stock data from Quandl for a single stock

    :param symbol: string
    :param start_date: datetime
    :param end_date: datetime
    :param db_code: Quandl database code
    :return: DataFrame of stock data from start_date to end_date
    """

    if start_date is None:
        start_date = dt(year=1990, month=1, day=1)

    if end_date is None:
        end_date = dt.today()

    if start_date is not None and end_date is not None:
        assert start_date < end_date, "Start date is later than end date."

    quandl_code = db_code + "/" + symbol
    symbol_data = qd.get(quandl_code, returns="pandas",
                         trim_start=start_date, trim_end=end_date,
                         authtoken=quandl_key)
    return symbol_data


def get_stock_data_multiple(
        symbols=None, start_date=None, end_date=None, db_code="WIKI"):
    """
    Get OHLC stock data from Quandl for multiple stocks

    :param symbols: list of symbols (strings)
    :param start_date: datetime
    :param end_date: datetime
    :param db_code: Quandl database code.
    :return: OrderedDict of DataFrames of data from start_date to end_date
    """

    data = OrderedDict()

    if symbols is not None:
        for symbol in symbols:
            quandl_code = db_code + "/" + symbol
            symbol_data = qd.get(quandl_code, returns="pandas",
                                 trim_start=start_date, trim_end=end_date,
                                 authtoken=quandl_key)
            data[symbol] = symbol_data

    return data


def get_pct_returns(symbol, start_date=None, end_date=None, col='Adj. Close'):
    """
    Get OHLC stock percentage returns from Quandl for a single stock

    :param symbol: stock ticker to look up
    :param start_date: datetime
    :param end_date: datetime
    :param col: (string) name of column to calculate the pct returns from
    :return: stock percentage returns from Quandle for a specified stock
    """

    data = get_stock_data(symbol, start_date, end_date)[col]
    return data.pct_change().fillna(0)


def get_returns(symbol, start_date=None, end_date=None, col='Adj. Close'):
    """
    Get OHLC stock returns from Quandl for a single stock

    :param symbol: stock ticker to look up
    :param start_date: datetime
    :param end_date: datetime
    :param col:  name of column to calculate the returns from
    :return: stock returns from Quandl for a specified input stock
    """

    data = get_stock_data(symbol, start_date, end_date)[col]
    return data.diff().fillna(0)


def get_options_data_quandl(symbol=None):
    """
    Get OHLC stock options from Quandl for a single stock

    :param symbol: ticker symbol
    :return: list of column names
    """

    return list(get_stock_data(symbol).columns.values)
