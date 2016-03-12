from django.contrib.auth.models import User
from django.http import Http404, HttpResponse

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
    user = User.objects.get(pk=user_id)
    if user is not None:
        portfolio = Portfolio.objects.create(portfolio_user=user)
        portfolio.save()
        raise Http404
    else:
        raise HttpResponse(status=200)

def delete_portfolio(request, portfolio_id):
    portfolio = Portfolio.objects.get(portfolio_id)
    if portfolio is None:
        raise Http404
    else:
        portfolio.delete()
        return HttpResponse(status=200)

def get_portfolio(request):
    pass

