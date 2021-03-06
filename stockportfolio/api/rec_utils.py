import random

from stockportfolio.api.datautils.yahoo_finance import (get_company_name,
                                                        get_company_sector)
from stockportfolio.api.models import Portfolio, Stock

""" Functions to assist in portfolio and stock recommendation """


def get_sector_stocks(portfolio, all_stocks, num_stocks, diversify=False):
    """
    Helper function to pick stocks by sector


    :param portfolio: user's portfolio
    :param all_stocks: list of all available stocks
    :param num_stocks: number of stocks to fetch
    :param diversify: pick stocks from different sectors
    """
    stocks = []
    tickers = []
    sectors = _get_all_sectors(portfolio)
    iterations = 0
    while len(stocks) < num_stocks:
        if iterations > 100:
            return stocks
        new_stock = all_stocks[random.randint(0, len(all_stocks) - 1)]
        if new_stock is None:
            iterations += 1
            continue
        if diversify and new_stock.stock_sector in sectors:
            continue
        else:
            if new_stock.stock_ticker in tickers:
                continue
            else:
                stocks.append(new_stock)
                tickers.append(new_stock.stock_ticker)
        iterations += 1
    return stocks


def get_recommendations(compare, stocks, num_stocks, p_risk):
    """
    Fetches stock recommendations based on the result of a parameter function

    :param compare: function that returns a bool when given stock risk
    :param stocks:
    :param num_stocks: number of stocks to fetch
    """
    iterations = 0
    recs = []
    while len(recs) < num_stocks:
        if iterations > 100:
            return recs
        new_stock = stocks[random.randint(0, len(stocks) - 1)]
        risk = _get_latest_stock_risk(new_stock)
        if compare(risk, p_risk):
            recs.append(new_stock)
        iterations += 1
    return recs


def get_portfolio_and_risk(user, user_settings):
    """
    Acquires the user portfolio if it exists, as well as risk
    If the user has no portfolios, a portfolio risk between
    -2.5 and 2.5 is chosen

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
        tickers = [
            sp.stock.stock_ticker for sp in portfolio.portfolio_stocks.all()]
    return tickers


def stock_slice(all_stocks, limit):
    """
    Helper function to get a random subset of stocks

    :param all_stocks: list of stocks
    :param limit: number of stocks to select
    """
    stocks = []
    tickers = []
    if all_stocks is None:
        return None
    count = all_stocks.count() - 1
    if count < limit:
        return None
    while len(stocks) < limit:
        idx = random.randint(0, count)
        stock = all_stocks[idx]
        if stock.stock_ticker not in tickers:
            tickers.append(stock.stock_ticker)
            stocks.append(stock)
    return stocks


def determine_stock_quantities(curr_portfolio, new_portfolio):
    """
    Given an old portfolio and a list of stocks, this function tries to
    generate an appropriate quantity for each stock, s.t. the value of the
    resulting portfolio is within +/- 20 percent of the old

    :param curr_portfolio: portfolio to match
    :param new_portfolio: list of stocks to weight w/ quantities
    """
    if len(new_portfolio) == 0:
        return new_portfolio, 0, 0, 0
    tvalue_low, tvalue_high = _fetch_target_value(curr_portfolio)
    portfolio = []
    for stock in new_portfolio:
        p = _get_latest_stock_price(stock)
        if p == 0:
            continue
        if p > 0.2 * tvalue_low and len(portfolio) > 5:
            continue
        upper = int(((tvalue_high - tvalue_low) / 2) / p)
        if upper == 0:
            upper = 2
        q = random.randint(1, upper)
        portfolio.append((stock.stock_ticker, q, p))
    value = _calculate_portfolio_value(portfolio)
    iterations = 0
    portfolio = sorted(portfolio, key=lambda s: s[2])
    if len(portfolio) == 0:
        return [], 0, 0, 0
    for iterations in range(0, 10):
        if value > tvalue_low and value < tvalue_high:
            break
        next_ticker = -1
        s = portfolio[next_ticker]
        if value < tvalue_low:
            portfolio[next_ticker] = (s[0], s[1] + 1, s[2])
        elif value > tvalue_high:
            portfolio[next_ticker] = (s[0], s[1] - 1, s[2])
            if s[1] == 0:
                del portfolio[next_ticker]
                continue
        value = _calculate_portfolio_value(portfolio)
    final_port = []
    for r in portfolio:
        s = Stock.objects.get(stock_ticker=r[0])
        final_port.append({
            'ticker': r[0],
            'name': s.stock_name,
            'sector': s.stock_sector,
            'risk': _get_latest_stock_risk(s),
            'price': '${:,.2f}'.format(r[2]),
            'quantity': r[1]}
        )
    return final_port, value, tvalue_low, tvalue_high


def stock_to_dict(stock):
    """
    Given a stock, this function converts all its data to a dictionary and
    returns that dictionary

    :param stock: stock to convert
    :return dictionary_of_stock
    """
    risk = _get_latest_stock_risk(stock)
    price = _get_latest_stock_price(stock)
    date = None
    if risk is not None:
        date = stock.stock_risk.all().order_by('risk_date').last().risk_date
        date = '{:%d %B %Y}'.format(date)
    blurb = stock.stock_ticker + ' is currently valued at '
    blurb += '${:,.2f}'.format(price) + '. '
    if date is None:
        blurb += (' We currently don\'t have any risk information for {}.'
                  .format(stock.stock_ticker))
    else:
        blurb += 'As of {}, {} had a risk of {:,.2f}'.format(
            date, stock.stock_ticker, risk)
    return {'ticker': stock.stock_ticker,
            'name': stock.stock_name,
            'sector': stock.stock_sector,
            'price': price,
            'risk': risk,
            'blurb': blurb}


def stock_recommender(request, portfolio_id, rec_type):
    """
    Given a request, portfolio_id and a recommendation type, this function
    generates a map that contains stock recommendations for the user

    :param request: request object
    :param portfolio_id: portfolio id for the specific portfolio
    :param rec_type: the type of recommendation
    :return recs: list of stocks to weight w/ quantities
    """
    portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
    p_risk = _get_latest_portfolio_risk(portfolio)
    if not p_risk:
        p_risk = 2
    upper_bound = 5
    lower_bound = 2
    all_stocks = stock_slice(Stock.objects.all(), 1000)
    recs = []
    if rec_type == 'diverse':
        recs = get_sector_stocks(portfolio, all_stocks,
                                 random.randint(lower_bound,
                                                upper_bound), True)
    else:
        rec_fn = None
        if rec_type == 'low_risk':
            rec_fn = _recommender_low_risk
        elif rec_type == 'high_risk':
            rec_fn = _recommender_high_risk
        elif rec_type == 'stable':
            rec_fn = _recommender_stable
        recs = get_recommendations(rec_fn, all_stocks,
                                   random.randint(lower_bound,
                                                  upper_bound),
                                   p_risk)
    recs = map(stock_to_dict, recs)
    return recs


def _recommender_low_risk(x, p_risk):
    """
    Helper function that returns recommendations lower than portfolio risk

    :param x: recommendation risk
    :param p_risk: portfolio risk
    """
    return x <= p_risk


def _recommender_high_risk(x, p_risk):
    """
    Helper function that returns recommendations greater than portfolio risk

    :param x: recommendation risk
    :param p_risk: portfolio risk
    """
    return x > p_risk


def _recommender_stable(x, p_risk):
    """
    Helper function that returns recommendations within 1.2 and 0.8 of
    portfolio risk

    :param x: recommendation risk
    :param p_risk: portfolio risk
    """
    return x < p_risk * 1.2 and x > p_risk * 0.8


def _fetch_target_value(portfolio):
    """
    Given a portfolio, this function returns a range within which the value of
    the portfolio lies. Used to calculate quantities for generated portfolios

    :param portfolio:
    """
    tvalue_low = 0
    tvalue_high = 0
    if portfolio is not None:
        value = 0
        for sp in portfolio.portfolio_stocks.all():
            stock = sp.stock
            price = _get_latest_stock_price(stock)
            value += price * sp.quantity
        tvalue_low = value - 0.2 * value
        tvalue_high = 0.2 * value + value
    else:
        tvalue_low = random.uniform(10000.0, 20000.0)
        tvalue_high = random.uniform(20000.0, 50000.0)
    return tvalue_low, tvalue_high


def _calculate_portfolio_value(portfolio):
    """
    Determines portfolio value

    :param portfolio: a list of (ticker, quantity, price)
    """
    value = 0
    for price_info in portfolio:
        value += price_info[1] * price_info[2]
    return value


def _get_latest_stock_price(stock):
    """
    Helper function that returns the latest stock price lower than
    portfolio risk

    :param stock: stock whose price has to be checked
    :param stock_price: latest stock price
    """
    stock_price = 0
    try:
        stock_price = stock.stock_price.all().order_by('date').last().value
    except:
        pass
    return stock_price


def _get_latest_stock_risk(stock):
    """
    Helper function to acquire the latest stock risk, if it exists.

    :param stock
    """
    stock_risk = None
    try:
        stock_risk = (stock.stock_risk.all()
                      .order_by('risk_date')
                      .last().risk_value)
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
        p_risk = (portfolio.portfolio_risk.all()
                  .order_by('risk_date')
                  .last().risk_value)
    except AttributeError:
        pass
    return p_risk


def _get_all_sectors(portfolio):
    """
    Function to fetch all the sectors a portfolio has

    :param portfolio
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


def _add_stock(symbol, quantity, portfolio):
    """
    Function to add certain quantities of a stock to a portfolio

    :param symbol: symbol for stock to be added
    :param quantity: quantity to be added
    :param portfolio: portfolio to which stock has to be added
    """
    name = get_company_name(symbol)
    sector = get_company_sector(symbol)
    s = Stock.objects.get_or_create(
        stock_name=name,
        stock_ticker=symbol,
        stock_sector=sector)[0]
    sp = portfolio.portfolio_stocks.get_or_create(
        stock=s,
        defaults={'quantity': float(quantity)})[0]
    sp.save()
    return s
