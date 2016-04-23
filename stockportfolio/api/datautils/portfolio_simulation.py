import scipy.stats
import pandas as pd
import datetime as dt
from yahoo_finance import get_stock_data

def get_benchmark_returns(benchmark='SPY', start_date=None, end_date=None, price_field='Adj Close'):
    """
    Get the daily (non-cumulative) percent returns for the benchmark.
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :param benchmark: (str) default: SPY (S&P 500 index)
    :return: (pd.Series)
    """
    if start_date is None:
        start_date = dt.datetime(year=2008, month=1, day=1)
    if end_date is None:
        end_date = dt.datetime.today()

    benchmark_price_series = get_stock_data(benchmark, start_date=start_date, end_date=end_date)[price_field]

    return benchmark_price_series.pct_change().dropna()

def get_portfolio_returns_series(portfolio, start_date=None, end_date=None, price_field='Adj Close'):
    """
    Simulates portfolio returns assuming the portfolio was bought on start_date and held through end_date
    :param portfolio:
    :param start_date:
    :param end_date:
    :param price_field:
    :return:
    """
    if start_date is None:
        start_date = dt.datetime(year=2008, month=1, day=1)
    if end_date is None:
        end_date = dt.datetime.today()

    portfolio_value_series = get_portfolio_value_series(portfolio,
                                                        start_date=start_date,
                                                        end_date=end_date,
                                                        price_field=price_field)


    portfolio_returns_series = portfolio_value_series.pct_change().dropna()
    return portfolio_returns_series

def get_portfolio_value_series(portfolio, start_date=None, end_date=None, price_field='Adj Close'):
    """
    Generate a time-series of the portfolio assuming the portfolio was bought on start_date and held through end_date.
    :param portfolio: (dict) symbol:quantity
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :param price_field: (str) default: 'Adj Close'
    :return:
    """
    if start_date is None:
        start_date = dt.datetime(year=2008, month=1, day=1)
    if end_date is None:
        end_date = dt.datetime.today()

    position_values = []
    date_range = pd.date_range(start_date, end_date)
    for symbol, quantity in portfolio.items():
        position_value_series = get_position_value_series(symbol, quantity, start_date, end_date, price_field)
        position_values.append(position_value_series)

    portfolio_value_series = pd.Series(data=0, index=date_range)
    for symbol_value_series in position_values:
        portfolio_value_series = portfolio_value_series+symbol_value_series

    portfolio_value_series = portfolio_value_series.dropna()
    return portfolio_value_series

def get_position_value_series(symbol, quantity, start_date=None, end_date=None, price_field='Adj Close'):
    """
    Generate a time-series of a single position's value assuming it was bought on start_date and held through end_date.
    :param symbol: (str)
    :param quantity: (float)
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :param price_field: (str)
    :return: (pd.Series)
    """

    if start_date is None:
        start_date = dt.datetime(year=2008, month=1, day=1)
    if end_date is None:
        end_date = dt.datetime.today()

    price_series = get_stock_data(symbol, start_date, end_date)[price_field]
    holdings = pd.Series(data=quantity, index=pd.date_range(start_date, end_date))
    position_value_series = (price_series*holdings).dropna()
    return position_value_series

def calculate_alpha_beta(returns, benchmark_returns=None):
    """
    Calculates alpha and beta.
    :param returns:
    :param benchmark_returns: (
    :return: (float) alpha, (float) beta
    """
    ret_index = returns.index
    beta, alpha = scipy.stats.linregress(benchmark_returns.loc[ret_index].values, returns.values)[:2]
    return alpha * 30, beta
