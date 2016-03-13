from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
import json
from stockportfolio.api.models import Portfolio, Stock
from datautils.yahoo_finance import get_current_price, get_company_name

def add_stock(request, portfolio_id):
    portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
    stock_ticker = request.GET.get('stock', None)
    if stock_ticker is not None:
        stock_price = get_current_price(stock_ticker)
        stock_name = get_company_name(stock_ticker)
        if stock_name is None or stock_price is None:
            raise Http404
        stock = Stock.objects.create(stock_price=stock_price, stock_name=stock_name, stock_ticker=stock_ticker)

def remove_stock(request, portfolio_id):
    portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
    stock_ticker = request.GET.get('stock', None)
    if stock_ticker is not None and portfolio is not None:
        stock = portfolio.portfolio_stocks.filter(stock_ticker=stock_ticker).first()
        if stock is not None:
            stock.delete()
            return HttpResponse(status=200)
    return HttpResponse(status=400)

def create_portfolio(request, user_id):
    user = User.objects.get(pk=user_id)
    if user is not None:
        portfolio = Portfolio.objects.create(portfolio_user=user)
        portfolio.save()
        raise Http404
    else:
        raise HttpResponse(status=200)

def delete_portfolio(request, portfolio_id):
    portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
    if portfolio is None:
        raise Http404
    else:
        portfolio.delete()
        return HttpResponse(status=200)

def get_portfolio(request, portfolio_id):
    portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
    if portfolio is None:
        raise Http404
    else:
        portfolio_dict = {}
        portfolio_dict["portfolio_id"] = portfolio.portfolio_id
        portfolio_dict["portfolio_userid"] = portfolio.portfolio_user.pk
        portfolio_dict["stocks"] = []
        portfolio_dict["risk_history"] = []
        for stock in portfolio.portfolio_stocks.all():
            stock_dict = {}
            stock_dict["ticker"] = stock.stock_ticker
            stock_dict["name"] = stock.stock_name
            portfolio_dict["stocks"].append(stock_dict)
        for risk in portfolio.portfolio_risk.all().order_by('risk_date'):
            risk_dict = {}
            risk_dict["risk_value"] = risk.risk_value
            risk_dict["risk_date"] = '{}'.format(risk.risk_date)
            portfolio_dict["risk_history"].append(risk_dict)

        return HttpResponse(content=json.dumps(portfolio_dict), status=200, content_type='application/json')


