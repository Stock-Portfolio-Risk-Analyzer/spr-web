from stockportfolio.api.models import Portfolio, Stock;
from stockportfolio.api.datautils.yahoo_finance.py 

def add_stock(request, portfolio_id, stock):
    portfolio = Portfolio.objects.get(portfolio_id)

    stock = Stock.objects.create(stock_price)

def remove_stock(request, stock):
    pass

def create_portfolio(request, user_id):
    pass

def delete_portfolio(request):
    pass

def get_portfolio(request):
    pass

