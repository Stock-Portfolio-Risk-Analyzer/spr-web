import os
from datetime import date, timedelta

import numpy as np
import pandas as pd

import yahoo_finance
from stockportfolio.api.datautils.rri import (compute_stock_rri_for_range,
                                              compute_stock_rri_for_today)


def get_company_industry(symbol):
    """
    Returns the industry of the company given the stock symbol / ticker
    Parameter:  symbol -> ticket of the stock (string)
    Return: company industry (string)
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
    Parameter:  symbol -> ticker symbol of the stock (Type -> String)
                number_of_days_back ->  number of days back from today
                                        for which you want rri
                                        (Type -> integer)
    return: float
    """
    return compute_stock_rri_for_today(symbol, number_of_days_back)


def get_company_rri_for_range(symbol, start_date, end_date):
    """
    Parameter:  symbol -> ticker symbol of the stock (Type -> String)
            start_date, end_date ->
                range you want to compute rri on (Type -> String)
    return: float
    """
    return compute_stock_rri_for_range(symbol, start_date, end_date)


def get_company_rri_for_days_back(symbol, days_back):
    """
    Parameter:  symbol -> ticker symbol of the stock (Type -> String)
    return: List [ [date1, rri], [date2, rri], .... [date7, rri] ]
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
    Returns the name of the company given the stock symbol / ticker
    Parameter:  symbol -> ticket of the stock (string)
    Return: company name (string)
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
    Returns the sector of the company given the stock symbol / ticker
    Parameter:  symbol -> ticket of the stock (string)
    Return: company sector (string)
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
    Parameter:  symbol -> ticker symbol of the stock (Type -> String)
                number_of_days_back -> number of days back from today
                        for which you want the closing price
                        (Type -> integer)
    return: list of daily closing prices (Type -> list float)
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
    Parameter:  symbol -> ticker symbol of the stock (Type -> String)
    return: List [ [date1, rri], [date2, rri], .... [date7, rri] ]
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
    Parameter:  symbol -> ticker symbol of the stock (Type -> String)
    return: List [ [date1, rri], [date2, rri], .... [date30, rri] ]
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
    Parameter:  symbol -> ticker symbol of the stock (Type -> String)
    return: List [ [date1, rri], [date2, rri], .... [date365, rri] ]
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
    Parameter:  symbol -> ticker symbol of the stock (Type -> String)
    return: List [ [date1, rri], [date2, rri], .... [date365, rri] ]
    """
    start_date = date.today() - timedelta(days=7)
    end_date = date.today()
    volume_list = yahoo_finance.get_stock_data(
        symbol, start_date, end_date)["Volume"]
    return volume_list


def get_stock_volume_traded_for_a_month(symbol):
    """
    Parameter:  symbol -> ticker symbol of the stock (Type -> String)
    return: List [ [date1, rri], [date2, rri], .... [date365, rri] ]
    """
    start_date = date.today() - timedelta(days=30)
    end_date = date.today()
    volume_list = yahoo_finance.get_stock_data(
        symbol, start_date, end_date)["Volume"]
    return volume_list


def get_average_stock_volume_traded(list):
    val = int(np.average(list))
    return val
