from datetime import date, timedelta
from functools import partial
import scipy.stats
import pandas as pd
import numpy as np
import yahoo_finance

"""
API that computes Relative Risk Index for a given Stock or Portfolio
Author - Shivam Gupta (sgupta40@illinois.edu)
         Rohan Kapoor (rkapoor6@illinois.edu)
"""


def compute_daily_change_for_past_given_days(symbol, n_days_back=1):
    """
    Parameter:  symbol (str):      ticker symbol of the stock (Type -> String)
                n_days_back (int): number of days back from today for which you want the daily change
    return: list of daily change (list(float))
    """
    start_date = date.today() - timedelta(days=n_days_back)
    end_date = date.today()
    symbol_data = yahoo_finance.get_stock_data(symbol, start_date, end_date)
    return list(symbol_data['Close'].pct_change()*100)[1:]


def compute_daily_change_for_range(symbol, start_date, end_date):
    """
    Parameter:  symbol (str):               ticker symbol of the stock (Type -> String)
                start_date, end_date (str): range you want to compute on (Type -> String)

    return: list of daily change (list(float))
    """
    symbol_data = yahoo_finance.get_stock_data(symbol, start_date, end_date)
    return list(symbol_data['Close'].pct_change()*100)[1:]


def compute_covariance(a, b):
    """
    Computes covariance.
    Parameter: a, b (list(float))
    Return: float
    """
    return np.cov(np.array([a, b]))[0, 1]


def compute_variance(a):
    """
    Computes Variance
    Parameter: a (float):
    Return: (float)
    """
    return np.var(a)


def compute_stock_rri_for_today(symbol, n_days_back=1):
    """
    Parameter:  symbol (str):      ticker symbol of the stock
                n_days_back (int): number of days back from today for which you want rri
    return: float
    """
    stock_daily_change  = compute_daily_change_for_past_given_days(symbol, n_days_back)
    index_daily_change  = compute_daily_change_for_past_given_days("NYA", n_days_back)
    covariance_val = compute_covariance(stock_daily_change, index_daily_change)
    variance_val   = compute_variance(index_daily_change)
    rri = covariance_val/variance_val
    return (rri + 1)


def compute_stock_rri_for_range(symbol, start_date, end_date):
    """
    Parameter:  symbol (str):               ticker symbol of the stock
                start_date, end_date (str): range you want to compute rri on
    return: (float)
    """
    stock_daily_change  = compute_daily_change_for_range(symbol, start_date, end_date)
    index_daily_change  = compute_daily_change_for_range("NYA", start_date, end_date)

    covariance_val = compute_covariance(stock_daily_change, index_daily_change)
    variance_val = compute_variance(index_daily_change)
    rri = covariance_val/variance_val
    return (rri + 1)


def compute_portfolio_rri_for_today(stocks, n_days_back=1):
    """
    Computes RRI for a portfolio.
    Parameter:  stocks (list(Stock)): list of stock objects
                n_days_back (int):    number of days back from today for which you want rri
    Return: (float)
    """
    total_rri = 0.0
    total_quantity = 0
    for stock in stocks:
        ticker = stock.stock_ticker
        quantity = stock.stock_quantity
        stock_rri = compute_stock_rri_for_today(ticker, n_days_back)
        total_rri = total_rri + (stock_rri * quantity)
        total_quantity = total_quantity + quantity

    portfolio_rri = (total_rri / total_quantity)
    return portfolio_rri


def compute_portfolio_rri_for_range(stocks, start_date, end_date):
    """
    Computes RRI for a portfolio
    Parameter:  stocks (list(Stock)):       list of stock objects
                start_date, end_date (str): range you want to compute rri on
    Return: (float)
    """
    total_rri = 0.0
    total_quantity = 0
    for stock in stocks:
        ticker = stock.stock_ticker
        quantity = stock.stock_quantity
        stock_rri = compute_stock_rri_for_range(ticker, start_date, end_date)
        total_rri = total_rri + (stock_rri * quantity)
        total_quantity = total_quantity + quantity
    return (total_rri / total_quantity)


def compute_portfolio_returns(stocks, start_date, end_date):
    """
    Get weighted returns of a portfolio from start_date to end_date
    (assuming we bought the portfolio on start_date and held through end_date)
    :param stocks: (dict) {symbol: quantity}
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :return: (Series) of daily returns
    """
    date_range = pd.date_range(start_date, end_date)
    portfolio_returns = pd.Series(data=[1]*len(date_range), index=date_range)
    for symbol, quantity in stocks.iteritems():
        symbol_returns = yahoo_finance.get_pct_returns(symbol, start_date, end_date)
        portfolio_returns = portfolio_returns*quantity*symbol_returns
    return portfolio_returns


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

def compute_portfolio_rolling_beta(stocks, start_date, end_date, rolling_window=30):
    """
    Calculate the rolling beta of the strategy from start_date to end_date
    :param stocks: (dict) {symbol: quantity}
    :param returns: (daily simulated returns of the strategy)
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :param rolling_window: (int) rolling window for which to compute the beta,
                                 default is 1 month
    :return: (series) of rolling beta
    """
    portfolio_returns = compute_portfolio_returns(stocks, start_date, end_date)
    factor_returns = yahoo_finance.get_pct_returns('SPY', start_date, end_date)  # the benchmark
    if factor_returns.ndim > 1:
        # apply column-wise
        return factor_returns.apply(partial(compute_portfolio_rolling_beta, portfolio_returns),
                                    rolling_window=rolling_window)
    else:
        rolling_beta = pd.Series(index=portfolio_returns.index)
        for beg, end in zip(portfolio_returns.index[0:-rolling_window],
                            portfolio_returns.index[rolling_window:]):
            rolling_beta.loc[end] = calculate_alpha_beta(portfolio_returns.loc[beg:end],
                                      factor_returns.loc[beg:end])[1]
        return rolling_beta

