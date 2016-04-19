from datautils import rri as rri
from datautils import stock_info as stock_info
from stockportfolio.api.models import Portfolio, Risk, PortfolioRank, Stock
import numpy
from django.db.models import Count

def update_rri_for_all_portfolios():
    for portfolio in Portfolio.objects.all():
        stocks = portfolio.portfolio_stocks.all()
        if not stocks:
            continue
        risk = Risk(
            risk_value=rri.compute_portfolio_rri_for_today(stocks, 10))
        risk.save()
        portfolio.portfolio_risk.add(risk)
        portfolio.save()


def update_rank_for_all_portfolios():
    risks = []
    for portfolio in Portfolio.objects.all():
        risk_object = portfolio.portfolio_risk.order_by('-risk_date').first()
        if not risk_object:
            risk = 0
        else:
            risk = risk_object.risk_value
        risks.append((portfolio.portfolio_id, risk))
    risk_values = numpy.array(zip(*risks)[1])
    temp = risk_values.argsort()[::-1]
    rank_values = numpy.empty(len(risk_values), int)
    rank_values[temp] = numpy.arange(len(risk_values))
    ranks = zip(zip(*risks)[0], rank_values)
    for portfolio_id, rank in ranks:
        portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
        rank = PortfolioRank(value=rank+1, portfolio=portfolio)
        rank.save()


def update_rri_for_all_stocks():
    for stock in Stock.objects.all():
        risk = Risk(
            risk_value=stock_info.get_company_rri_for_today(
                stock.stock_ticker, 10))
        risk.save()
        stock.stock_risk.add(risk)
        stock.save()


def precompute_rri_for_all_stocks():
    stocks_to_precompute = (Stock.objects.values('stock_id')
                            .annotate(Count('stock_risk')).order_by()
                            .filter(stock_risk__count__lt=30))
    stocks = (Stock.objects
              .filter(stock_id__in=[
                      item['stock_id'] for item in stocks_to_precompute])
              .order_by('stock_id'))

    for stock in stocks:
        try:
            rris = stock_info.get_company_rri_for_days_back(
                stock.stock_ticker, 30)
            for date, value in rris:
                risk = Risk(risk_value=value, risk_date=date)
                risk.save()
                stock.stock_risk.add(risk)
                stock.save()
        except:
            continue

