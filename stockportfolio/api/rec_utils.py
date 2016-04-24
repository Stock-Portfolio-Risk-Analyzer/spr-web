import random
import time

from stockportfolio.api.models import Portfolio, Stock, UserSettings, PortfolioRank, StockPortfolio

def get_sector_stocks(portfolio, all_stocks, num_stocks, diversify=False):
    """
    Helper function to pick stocks by sector
    :param portfolio:
    :param all_stocks: list all available stocks
    :param num_stocks: number of stocks to fetch
    :param diversify: pick stocks from different sectors
    """
    stocks = []
    tickers = []
    sectors = _get_all_sectors(portfolio)
    while len(stocks) != num_stocks:
        new_stock = all_stocks[random.randint(0, len(all_stocks)-1)]
        if diversify and new_stock.stock_sector in sectors:
           continue
        else:
           if new_stock.stock_ticker in tickers:
             continue
           else:
                stocks.append(new_stock)
                tickers.append(new_stock.stock_ticker)
    return stocks

def get_recommendations(compare, stocks, num_stocks):
    """
    Fetches stock recommendations based on the result of a parameter function
    :param compare: function that returns a bool when given stock risk
    :param stocks: 
    :param num_stocks: number of stocks to fetch
    """
    recs = []
    for stock in stocks:
        if len(recs) == num_stocks:
            break
        risk = _get_latest_stock_risk(stock)
        if compare(risk):
            recs.append(stock)
    return recs

def get_portfolio_and_risk(user, user_settings):
    """
    Acquires the user portfolio if it exists, as well as risk
    If the user has no portfolios, a portfolio risk between -2.5 and 2.5 is chosen
    :param user
    :param user_settings
    """
    p_risk = random.uniform(-2.5, 2.5)
    portfolio = None
    is_user_portfolio = False
    if user_settings.default_portfolio:
        portfolio = user_settings.default_portfolio
        p_risk = _get_latest_portfolio_risk(portfolio)
        is_user_portfolio = True
    elif user.portfolio_set.all().first():
        portfolio = user.portfolio_set.all().first()
        p_risk = _get_latest_portfolio_risk(portfolio)
        is_user_portfolio = True
    return portfolio, p_risk, is_user_portfolio

def fetch_tickers(portfolio):
    """
    Helper function to get all stock tickers in a current portfolio
    :param portfolio
    """
    tickers = None
    if portfolio is not None:
        tickers = [sp.stock.stock_ticker for sp in portfolio.portfolio_stocks.all()]
    return tickers

def stock_slice(all_stocks, limit):
    """
    Helper function to get a random subset of stocks
    :param all_stocks: list of stocks
    :param limit: number of stocks to select
    """
    stocks = []
    tickers = []
    while len(stocks) != limit:
        idx = random.randint(0, all_stocks.count()-1)
        stock = all_stocks[idx]
        if stock.stock_ticker in tickers:
            continue
        else:
            stocks.append(stock)
            tickers.append(stock.stock_ticker)
    return stocks

def determine_stock_quantities(curr_portfolio, new_portfolio):
    tvalue_low, tvalue_high  = _fetch_target_value(curr_portfolio)
    portfolio = []
    upper = random.randint(10, 15)
    lower = random.randint(1, 8)
    for stock in new_portfolio:
        p = _get_latest_stock_price(stock)
        if p > 0.2*tvalue_low:
            continue
        q = random.randint(1, int((tvalue_high-tvalue_low)/p))
        portfolio.append((stock.stock_ticker, q, p))
    value = _calculate_portfolio_value(portfolio)
    iterations = 0
    portfolio = sorted(portfolio, key=lambda s: s[2])
    while value < tvalue_low or value > tvalue_high:
        if iterations == 10:
            break
        next_ticker = len(portfolio)-1
        s = portfolio[next_ticker]
        if value < tvalue_low:
            portfolio[next_ticker] = (s[0], s[1]+1, s[2]) 
        elif value > tvalue_high:
            #if s[1] == 0:
                #p_dict.pop(next_ticker, None)
            #    continue
            portfolio[next_ticker] = (s[0], s[1]-1, s[2])
        iterations+=1
        value = _calculate_portfolio_value(portfolio)
    return portfolio, value, tvalue_low, tvalue_high

def get_all_stocks(all_stocks, sort_by_risk=False):
    """
    Fetches all stocks and optionally sorts by risk
    :param all_stocks: list of stocks
    """
    stock_tuples = []
    for stock in all_stocks:
       risk = _get_latest_stock_risk(stock)
       if risk is None:
            continue
       else:
        stock_tuples.append((stock.stock_ticker, risk))
    if(sort_by_risk):
       stock_tuples = sorted(stock_tuples, key=lambda s: s[1])
    ret_stocks = []
    for s in stock_tuples:
       ret_stocks.append(all_stocks.get(stock_ticker=s[0]))
    return ret_stocks

def _fetch_target_value(portfolio):
    tvalue_low  = 0
    tvalue_high = 0
    if portfolio is not None:
        value = 0
        for sp in portfolio.portfolio_stocks.all():
            stock = sp.stock
            price = _get_latest_stock_price(stock)
            value  += price*sp.quantity
        tvalue_low  = value-0.2*value
        tvalue_high = 0.2*value+value
    else:
        tvalue_low  = random.uniform(10000.0, 20000.0)
        tvalue_high = random.uniform(20000.0, 50000.0)
    return tvalue_low, tvalue_high

def _calculate_portfolio_value(portfolio):
    """
    Determines portfolio value
    :param portfolio: a list of (ticker, quantity, price)
    """
    value = 0
    for price_info in portfolio:
        value += price_info[1]*price_info[2]
    return value

def _get_latest_stock_price(stock):
    stock_price = 0
    try:
        stock_price = stock.stock_price.all().order_by('date').last().value
    except:
        pass
    return stock_price

def _get_latest_stock_risk(stock):
    """
    Helper function to acquire the latest stock risk, if it exists. 
    :param portfolio
    """
    stock_risk = None
    try:
       stock_risk = stock.stock_risk.all().order_by('risk_date').last().risk_value
    except AttributeError:
       pass
    return stock_risk

def _get_latest_portfolio_risk(portfolio):
    """
    Helper function to fetch the latest portfolio risk, if it exists. 
    :param portfolio
    """
    p_risk = None
    try:
       p_risk = portfolio.portfolio_risk.all().order_by('risk_date').last().risk_value
    except AttributeError:
       pass
    return p_risk

def _get_all_sectors(portfolio):
    """
    Function to fetch all the sectors a portfolio has
    """
    sectors = []
    if portfolio is not None:
       for sp in portfolio.portfolio_stocks.all():
            sector = sp.stock.stock_sector
            if sector in sectors:
                continue
            else:
                sectors.append(sector)
    return sectors