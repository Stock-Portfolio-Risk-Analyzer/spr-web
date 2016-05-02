import csv
import os
from datetime import date

import numpy as np
import Quandl

from stockportfolio.settings.base import BASE_DIR

"""
API that computes sentiment for a given Stock or Portfolio
Author - Shivam Gupta (sgupta40@illinois.edu)
"""

quandl_key = '-6X6UvP1aeit_zybGREM'

tickers = []
ticker_sentiment = {}

fpath = os.path.join(BASE_DIR, 'api', 'datautils', 'alpha_one.csv')

with open(fpath, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        tickers.append(row[0].lower())
        ticker_sentiment[row[0]] = row[3]

tickers = list(set(tickers))

def get_stock_sentiment(symbol):
    """
    This function returns the sentiment for a stock

    :param symbol: symbol for stock
    :return: returns 1 or -1 depending on function run
    """
    if symbol.lower() in tickers:
        return 1 if float(ticker_sentiment[symbol.upper()]) > 0 else -1
    else:
        return 1 if float(np.random.randint(-2, 2)) > 0 else -1


def get_sentiment_of_a_portfolio(stocks):
    """
    This function returns the sentiment for a portfolio by calculating
    sentiment for each stock and averaging them.

    :param stocks: Stocks is a list of stocks
    :return: returns a sentiment value
    """
    sentiment = []
    for stock in stocks:
        stock_sentiment = get_stock_sentiment(stock)
        sentiment.append(stock_sentiment)

    return np.average(sentiment)


def get_stock_sentiment_for_a_range(symbol, start_date, end_date):
    """
    This function calculates the stock sentiment for a certain symbol
    for a certain start and end date

    :param symbol: Symbol for stock
    :param start_date: Start date for the range
    :param end_date: End date for the range
    :return: list of sentiments for range
    """
    link = str("AOS/" + symbol)
    temp_sentiment_list = Quandl.get(
        link, authtoken=quandl_key, trim_start=start_date, trim_end=end_date)
    temp_sentiment_list = temp_sentiment_list["Article Sentiment"]
    sentiment_list = []

    for i in range(0, len(temp_sentiment_list)):
        sentiment_list.append(temp_sentiment_list[i])

    return sentiment_list


def get_average_stock_sentiment_for_a_range(symbol, start_date, end_date):
    """
    This function calculates the average stock sentiment for a certain symbol
    for a certain range between start date and end date

    :param symbol: Symbol for stock
    :param start_date: Start date for the range
    :param end_date: End date for the range
    :return: average sentiment for range
    """
    sentiment_list = get_stock_sentiment_for_a_range(
        symbol, start_date, end_date)
    return np.average(sentiment_list)


def get_market_sentiment():
    """
    This function calculates the market sentiment by calling the Quandl
    API

    :return: market sentiment
    """
    sentiment = Quandl.get(
        "AOS/SNP", authtoken=quandl_key, trim_end=date.today())
    return sentiment["Article Sentiment"][len(sentiment) - 1]
