from datetime import date, timedelta
import numpy as np
import Quandl
import yahoo_finance

"""
API that computes sentiment for a given Stock or Portfolio
Author - Shivam Gupta (sgupta40@illinois.edu)
"""

quandl_key = "SyH7V4ywJGho77EC6W7C"

def get_stock_sentiment_for_today(symbol):
	link = str("AOS/" + symbol)
	today = date.today()
	sentiment = Quandl.get(link, authtoken=quandl_key, trim_start=today)["Article Sentiment"][0]
	return sentiment

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
	sentiment = Quandl.get("AOS/SNP", authtoken=quandl_key, trim_end="2016/04/20")
	return sentiment["Article Sentiment"][len(sentiment)-1]

def get_sentiment_of_a_portfolio_for_today(stocks):
	sentiment = []

	for stock in stocks:
		stock_sentiment = get_stock_sentiment_for_today(stock)
		sentiment.append(stock_sentiment)
	
	return np.average(sentiment)
