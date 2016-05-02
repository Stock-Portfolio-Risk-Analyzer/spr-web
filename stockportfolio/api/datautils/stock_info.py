import os
from datetime import date, timedelta

import numpy as np
import pandas as pd

import yahoo_finance
from stockportfolio.api.datautils.rri import (compute_stock_rri_for_range,
                                              compute_stock_rri_for_today)


def get_company_industry(symbol):
    """
    Returns industry associated with the given ticker
    :param symbol: (String) ticker symbol of the stock
    :return: (String) Industry
    """
    fpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'secwiki_tickers.csv')
    df = pd.read_csv(fpath)
    company_info = df[df.Ticker == symbol]
    code = company_info['Name'].keys()[0]
    company_name = company_info.to_dict()['Industry'][code]
    return company_name


def get_company_rri_for_today(symbol, number_of_days_back):
    """
    Computes RRI for a symbol for given number of days
    :param symbol: (String) ticker symbol of the stock
    :param number_of_days_back: (int) number of days back from today
    :return: (float) RRI
    """
    return compute_stock_rri_for_today(symbol, number_of_days_back)


def get_company_rri_for_range(symbol, start_date, end_date):
    """
    Computes RRI for a symbol for a range
    :param symbol: (String) ticker symbol of the stock
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :return: (float) RRI
    """
    return compute_stock_rri_for_range(symbol, start_date, end_date)


def get_company_rri_for_days_back(symbol, days_back):
    """
    Computes RRI for a symbol for given number of days back
    :param symbol: (String) ticker symbol of the stock
    :param days_back: (int) number of days back from today
    :return: (float) RRI
    """
    rri_list = []
    for i in range(days_back + 5, 5, -1):
        start_date = date.today() - timedelta(days=i)
        end_date = date.today() - timedelta(days=i - 5)
        value = round(
            compute_stock_rri_for_range(symbol, start_date, end_date), 3)
        rri_list.append((start_date, value))

    return rri_list


def get_company_name(symbol):
    """
    Returns company name associated with the given ticker
    :param symbol: (String) ticker symbol of the stock
    :return: (String) Name
    """
    fpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'secwiki_tickers.csv')
    df = pd.read_csv(fpath)
    company_info = df[df.Ticker == symbol]
    code = company_info['Name'].keys()[0]
    company_name = company_info.to_dict()['Name'][code]
    return company_name


def get_company_sector(symbol):
    """
   Returns company sector associated with the given ticker
    :param symbol: (String) ticker symbol of the stock
    :return: (String) Sector
    """
    fpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'secwiki_tickers.csv')
    df = pd.read_csv(fpath)
    company_info = df[df.Ticker == symbol]
    code = company_info['Name'].keys()[0]
    company_name = company_info.to_dict()['Sector'][code]
    return company_name


def get_price_for_number_of_days_back_from_today(symbol, number_of_days_back):
    """
    Returns a list of closing prices
    :param symbol: (String) ticker symbol of the stock
    :param number_of_days_back: (int) number of days back from today
    :return: (float) daily closing prices
    """
    start_date = date.today() - timedelta(days=number_of_days_back)
    end_date = date.today()
    symbol_data = yahoo_finance.get_stock_data(symbol, start_date, end_date)
    graphing_tuples = []
    value_timestamps = symbol_data.index
    values = symbol_data["Close"]
    for i in range(len(values)):
        graphing_tuples.append((value_timestamps[i], round(values[i], 3)))
    return graphing_tuples


def get_company_rri_for_a_week(symbol):
    """
    Gets a week's worth of risk values.
    :param symbol: (str)
    :return: (list) [ [date1, rri], [date2, rri], .... [date7, rri] ]
    """
    rri_list = []

    for i in [7, 6, 5, 4, 3, 2, 1]:
        start_date = date.today() - timedelta(days=i)
        end_date = date.today() - timedelta(days=i - 1)
        day_rri = [str(start_date), compute_stock_rri_for_range(
            symbol, start_date, end_date)]
        rri_list.append(day_rri)

    return rri_list


def get_company_rri_for_a_month(symbol):
    """
    Gets a month's worth of risk values.
    :param symbol: (str)
    :return: (list) [ [date1, rri], [date2, rri], .... [date30, rri] ]
    """
    rri_list = []
    month_range = range(100)[1:31]
    month_range.reverse()
    for i in month_range:
        start_date = date.today() - timedelta(days=i)
        end_date = date.today() - timedelta(days=i - 1)
        day_rri = [str(start_date), compute_stock_rri_for_range(
            symbol, start_date, end_date)]
        rri_list.append(day_rri)

    return rri_list


def get_company_rri_for_a_year(symbol):
    """
    :param symbol: (str)
    :return: (list) [ [date1, rri], [date2, rri], .... [date365, rri] ]
    """
    rri_list = []
    month_range = range(400)[1:366]
    month_range.reverse()
    for i in month_range:
        start_date = date.today() - timedelta(days=i)
        end_date = date.today() - timedelta(days=i - 1)
        day_rri = [str(start_date), compute_stock_rri_for_range(
            symbol, start_date, end_date)]
        rri_list.append(day_rri)

    return rri_list


def get_stock_volume_traded_for_a_week(symbol):
    """

    :param symbol: (str)
    :return: (list) [ [date1, rri], [date2, rri], .... [date365, rri] ]
    """
    start_date = date.today() - timedelta(days=7)
    end_date = date.today()
    volume_list = yahoo_finance.get_stock_data(
        symbol, start_date, end_date)["Volume"]
    return volume_list


def get_stock_volume_traded_for_a_month(symbol):
    """

    :param symbol: (str)
    :return: (list) [ [date1, rri], [date2, rri], .... [date365, rri] ]
    """
    start_date = date.today() - timedelta(days=30)
    end_date = date.today()
    volume_list = yahoo_finance.get_stock_data(
        symbol, start_date, end_date)["Volume"]
    return volume_list
