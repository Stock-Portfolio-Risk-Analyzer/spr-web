from django.http import Http404

from stockportfolio.api.models import Portfolio, Stock
from datautils.yahoo_finance import get_current_price, get_company_name

def add_stock(request, portfolio_id, stock):
    portfolio = Portfolio.objects.get(portfolio_id)
    stock_price = get_current_price(stock)
    stock_name = get_company_name(stock)
    if stock_name is None or stock_price is None:
        raise Http404
    stock = Stock.objects.create(stock_price=stock_price, stock_name=stock_name, stock_ticker=stock)

def remove_stock(request, stock):
    pass

def create_portfolio(request, user_id):
    # user = User.objects.get()
    Portfolio.objects.create()

def delete_portfolio(request):
    pass

def get_portfolio(request):
    pass

