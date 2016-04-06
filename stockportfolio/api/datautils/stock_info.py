import csv
import os
import ystockquote
import pandas as pd
import pandas_datareader.data as web
from collections import OrderedDict
from datetime import datetime as dt
from rri import *
from datetime import date, timedelta

def get_company_industry(symbol):
    """
    Returns the industry of the company given the stock symbol / ticker
    Parameter:  symbol -> ticket of the stock (string)
    Return: company industry (string)
    """
    fpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'secwiki_tickers.csv')
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
            start_date, end_date -> range you want to compute rri on (Type -> String)
    return: float
    """
	return compute_stock_rri_for_range(symbol, start_date, end_date)

def get_company_name(symbol):
    """
    Returns the name of the company given the stock symbol / ticker
    Parameter:  symbol -> ticket of the stock (string)
    Return: company name (string)
    """
    fpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'secwiki_tickers.csv')
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
    fpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'secwiki_tickers.csv')
    df = pd.read_csv(fpath)
    company_info = df[df.Ticker == symbol]
    code = company_info['Name'].keys()[0]
    company_name = company_info.to_dict()['Sector'][code]
    return company_name
