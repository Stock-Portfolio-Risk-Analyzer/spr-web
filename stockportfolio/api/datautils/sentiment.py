import csv
import os
from datetime import date, timedelta

import numpy as np
import Quandl

from stockportfolio.settings.base import BASE_DIR

"""
API that computes sentiment for a given Stock or Portfolio
Author - Shivam Gupta (sgupta40@illinois.edu)
"""

#quandl_key = "SyH7V4ywJGho77EC6W7C"

#quandl_key = "svyaA69jUs7XUNys34W7"

quandl_key = "hJFsm6TLFgZmhD8NtsS9"

tickers = []
ticker_sentiment = {}

fpath = os.path.join(BASE_DIR, 'api', 'datautils', 'alpha_one.csv')

with open(fpath, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        tickers.append(row[0].lower())
        ticker_sentiment[row[0]] = row[3]

tickers = list(set(tickers))

def get_stock_sentiment_api(symbol):
	link = str("AOS/" + symbol)
	today = date.today()
	sentiment = Quandl.get(link, authtoken=quandl_key, trim_start=today)["Article Sentiment"][0]
	return sentiment

def get_stock_sentiment(symbol):
	if symbol.lower() in tickers:
		return 1 if float(ticker_sentiment[symbol.upper()]) > 0  else -1 
	else:
		return 1 if float(np.random.randint(-2, 2)) > 0 else -1

def get_sentiment_of_a_portfolio(stocks):
	sentiment = []

	for stock in stocks:
		stock_sentiment = get_stock_sentiment(stock)
		sentiment.append(stock_sentiment)
	
	return np.average(sentiment)

def get_stock_sentiment_for_a_range(symbol, start_date, end_date):
	link = str("AOS/" + symbol)
	temp_sentiment_list = Quandl.get(link, authtoken=quandl_key, trim_start=start_date, trim_end=end_date)["Article Sentiment"]
	sentiment_list = []

	for i in range(0, len(temp_sentiment_list)):
		sentiment_list.append(temp_sentiment_list[i])

	return sentiment_list

def get_average_stock_sentiment_for_a_range(symbol, start_date, end_date):
	sentiment_list = get_stock_sentiment_for_a_range(symbol, start_date, end_date)
	return np.average(sentiment_list)

def get_market_sentiment():
	sentiment = Quandl.get("AOS/SNP", authtoken=quandl_key, trim_end=date.today())
	return sentiment["Article Sentiment"][len(sentiment)-1]
