from datautils import rri as rri
from datautils import stock_info as stock_info
from datautils import yahoo_finance as yf
from stockportfolio.api.models import Portfolio, Risk, PortfolioRank, Stock, Price
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


def update_price_for_all_stocks():
    for stock in Stock.objects.all():
        price = Price(value=yf.get_current_price(stock.stock_ticker))
        price.save()
        stock.stock_price.add(price)
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


def precompute_prices_for_all_stocks():
    stocks_to_precompute = (Stock.objects.values('stock_id')
                            .annotate(Count('stock_price')).order_by()
                            .filter(stock_price__count__lt=365))
    stocks = (Stock.objects
              .filter(stock_id__in=[
                      item['stock_id'] for item in stocks_to_precompute])
              .order_by('stock_id'))

    for stock in stocks:
        try:
            prices = stock_info.get_price_for_number_of_days_back_from_today(
                stock.stock_ticker, 365)
            for timestamp, value in prices:
                price = Price(value=value, date=timestamp.to_datetime())
                price.save()
                stock.stock_price.add(price)
                stock.save()
        except:
            continue


def _calculate_risk(risk):
    """

    :param risk: (Risk)
    :return: (dict)
    """
    return {'risk_value': risk.risk_value,
            'risk_date': '{}'.format(risk.risk_date)}

