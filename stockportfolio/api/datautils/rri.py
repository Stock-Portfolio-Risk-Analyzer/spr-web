import csv
import os
from datetime import date, timedelta

import numpy as np
import Quandl

import yahoo_finance
from stockportfolio.settings.base import BASE_DIR

"""
API that computes Relative Risk Index for a given Stock or Portfolio
"""

tickers = []

fpath = os.path.join(BASE_DIR, 'api', 'datautils', 'alpha_one.csv')
with open(fpath, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        tickers.append(row[0].lower())


def verify_data_with_quandl(symbol, start_date, end_date, yahoo_data):
    """
    Verifies the given data with Quandl data
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :param yahoo_data: (list)
    :return: (list) List of verified data
    """
    link = str("WIKI/" + symbol)
    quandl_key = "SyH7V4ywJGho77EC6W7C"
    quandl_data = Quandl.get(
        link, authtoken=quandl_key, trim_start=start_date, trim_end=end_date)
    quandl_data = quandl_data["Close"]
    verify = []

    if len(yahoo_data) == len(quandl_data):
        for i in range(0, len(yahoo_data)):
            cur_quandl = quandl_data[i]
            tolerance = ((cur_quandl - (cur_quandl * 0.02)) <
                         yahoo_data[i] < (cur_quandl + (cur_quandl * 0.02)))
            if tolerance:
                verify.append(1)
            else:
                verify.append(0)

    for i in range(len(verify)):
        if verify[i] == 0:
            return yahoo_data
        else:
            return quandl_data

def compute_daily_change_for_past_given_days(symbol, number_of_days_back):
    """
    Computes daily change in value
    :param symbol: (String) ticker symbol of the stock
    :param number_of_days_back: (Int) number of days back from today
    :return: (list) List of daily changes
    """
    start_date = date.today() - timedelta(days=number_of_days_back)
    end_date = date.today()
    symbol_data = yahoo_finance.get_stock_data(symbol, start_date, end_date)
    closing_price = list(symbol_data["Close"])

    # Data Integrity
    if symbol.lower() in tickers:
        closing_price = verify_data_with_quandl(
            symbol, start_date, end_date, closing_price)

    daily_change = []
    for i in range(0, len(closing_price) - 1):
        cur = closing_price[i]
        daily_change.append(
            ((closing_price[i + 1] - cur) / cur) * 100)

    return daily_change


def compute_daily_change_for_range(symbol, start_date, end_date):
    """
    Computes daily change in value over a range
    :param symbol: (String) ticker symbol of the stock
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :return: (list) List of daily changes
    """
    symbol_data = yahoo_finance.get_stock_data(symbol, start_date, end_date)
    closing_price = list(symbol_data["Close"])

    # Data Integrity
    if symbol.lower() in tickers:
        closing_price = verify_data_with_quandl(
            symbol, start_date, end_date, closing_price)

    daily_change = []
    if closing_price is None:
        return daily_change
    for i in range(0, len(closing_price) - 1):
        cur = closing_price[i]
        daily_change.append(((closing_price[i + 1] - cur) / cur) * 100)

    return daily_change


def compute_covariance(a, b):
    """
    Computes covariance
    :param a: (list) first list
    :param b: (list) second list
    :return: (float) covariance
    """

    if len(a) == 0 or len(b) == 0:
        return 0.0

    a_mean = (sum(a) / len(a))
    b_mean = (sum(b) / len(b))

    a_mean = (sum(a) / len(a))
    b_mean = (sum(b) / len(b))

    total = 0

    for i in range(0, len(a)):
        total += ((a[i] - a_mean) * (b[i] - b_mean))

    return (total / (len(a) - 1))


def compute_variance(a):
    """
    Computes variance
    :param a: (list) first list
    :return: (float) variance
    """
    return np.var(a)


def compute_stock_rri_for_today(symbol, number_of_days_back):
    """
    Computes RRI for a symbol for given number of days
    :param symbol: (String) ticker symbol of the stock
    :param number_of_days_back: (int) number of days back from today
    :return: (float) RRI
    """
    stock_daily_change = compute_daily_change_for_past_given_days(
        symbol, number_of_days_back)
    index_daily_change = compute_daily_change_for_past_given_days(
        "NYA", number_of_days_back)

    covariance_val = compute_covariance(stock_daily_change, index_daily_change)
    vairance_val = compute_variance(index_daily_change)
    rri = covariance_val / vairance_val
    return (rri + 1)


def compute_stock_rri_for_range(symbol, start_date, end_date):
    """
    Computes RRI for a symbol for a range
    :param symbol: (String) ticker symbol of the stock
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :return: (float) RRI
    """
    stock_daily_change = compute_daily_change_for_range(
        symbol, start_date, end_date)
    index_daily_change = compute_daily_change_for_range(
        "NYA", start_date, end_date)

    covariance_val = compute_covariance(stock_daily_change, index_daily_change)
    vairance_val = compute_variance(index_daily_change)
    rri = covariance_val / vairance_val
    return (rri + 1)


def compute_portfolio_rri_for_today(stocks, number_of_days_back):
    """
    Computes RRI for a portfolio for given number of days
    :param stocks: (list) list of stocks in a portfolio
    :param number_of_days_back: (int) number of days back from today
    :return: (float) RRI
    """
    total_rri = 0.0
    total_quantity = 0
    for i in range(len(stocks)):
        ticker = stocks[i].stock.stock_ticker
        quantity = stocks[i].quantity
        stock_rri = compute_stock_rri_for_today(ticker, number_of_days_back)
        total_rri = total_rri + (stock_rri * quantity)
        total_quantity = total_quantity + quantity

    portfolio_rri = (total_rri / total_quantity)

    return portfolio_rri


def compute_portfolio_rri_for_range(stocks, start_date, end_date):
    """
    Computes RRI for a portfolio for a range
    :param stocks: (list) list of stocks in a portfolio
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :return: (float) RRI
    """
    total_rri = 0.0
    total_quantity = 0
    for i in range(len(stocks)):
        ticker = stocks[i].stock.stock_ticker
        quantity = stocks[i].quantity
        stock_rri = compute_stock_rri_for_range(ticker, start_date, end_date)
        total_rri = total_rri + (stock_rri * quantity)
        total_quantity = total_quantity + quantity

    portfolio_rri = (total_rri / total_quantity)

    return portfolio_rri
