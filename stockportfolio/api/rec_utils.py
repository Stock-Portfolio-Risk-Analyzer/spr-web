from stockportfolio.api.models import Portfolio, Stock, UserSettings, PortfolioRank, StockPortfolio

def _get_sector_stocks(portfolio, all_stocks, num_stocks, diversify=False):
    """
    Helper function to pick stocks by sector
    :param portfolio:
    :param all_stocks: all available stocks
    :param num_stocks: number of stocks to fetch
    :param diversify: pick stocks from different sectors
    """
    return "muh dick"

def _get_portfolio_and_risk(user_settings):
    p_risk = 3.0
    portfolio = None
    if user_settings.default_portfolio:
        portfolio = user_settings.default_portfolio
        p_risk = _get_latest_portfolio_risk(portfolio)
    elif user.portfolio_set.all().first():
        portfolio = user.portfolio_set.all().first()
        p_risk = _get_latest_portfolio_risk(portfolio)
    return portfolio, p_risk

def _fetch_tickers(portfolio):
	tickers = None
    if portfolio is not None:
        tickers = [sp.stock.stock_ticker for sp in portfolio.portfolio_stocks.all()]
    return tickers

def _determine_stock_quantity(portfolio):

def _get_latest_stock_risk(stock):
	stock_risk = None
	try:
		stock.stock_risk.all().order_by('risk_date').last().risk_value
	except AttributeError:
		pass
	return stock_risk

def _get_latest_portfolio_risk(portfolio):
	p_risk = None
	try:
		portfolio.portfolio_risk.all().order_by('risk_date').last().risk_value
	except AttributeError:
		pass
	return p_risk

def _all_eligible_stocks(all_stocks):
	ret_stocks = []
	for stock in all_stocks:
		