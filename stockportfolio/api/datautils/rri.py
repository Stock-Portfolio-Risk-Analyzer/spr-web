from datetime import date, timedelta
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