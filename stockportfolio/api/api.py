import json
from datetime import datetime
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from stockportfolio.api.models import Portfolio, Stock
from datautils.yahoo_finance import get_current_price, get_company_name, get_company_sector


def add_stock(request, portfolio_id):
    """
    Add a stock to a portfolio.
    :param request:
    :param portfolio_id:
    :return:
    """
    portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
    assert(portfolio is not None)
    stock_ticker = request.GET.get('stock', None)
    if stock_ticker is not None:
        stock_name = get_company_name(stock_ticker)
        stock_quantity = request.GET.get('quantity', None)
        stock_sector = get_company_sector(stock_ticker)
        try:
            stock = Stock.objects.create(stock_name=stock_name, stock_ticker=stock_ticker,
                                         stock_quantity=stock_quantity, stock_sector=stock_sector)
            stock.save()
            portfolio.portfolio_stocks.add(stock)
        except None:
            raise Http404
        return HttpResponse(status=200)


def remove_stock(request, portfolio_id):
    """
    Remove a stock from the portfolio
    :param request:
    :param portfolio_id:
    :return:
    """
    portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
    stock_ticker = request.GET.get('stock', None)
    if stock_ticker is not None and portfolio is not None:
        stock = portfolio.portfolio_stocks.filter(stock_ticker=stock_ticker).first()
        if stock is not None:
            stock.delete()
            return HttpResponse(status=200)
    return HttpResponse(status=400)


def create_portfolio(request, user_id):
    """
    Creates a new portfolio model.
    :param request:
    :param user_id:
    :return:
    """
    assert(request is not None)
    user = User.objects.get(pk=user_id)
    if user is not None:
        portfolio = Portfolio.objects.create(portfolio_user=user)
        portfolio.save()
        raise Http404
    else:
        raise HttpResponse(status=200)


def delete_portfolio(request, portfolio_id):
    """
    Deletes a portfolio based on portfolio_id.
    :param request:
    :param portfolio_id:
    :return:
    """
    assert(request is not None)
    portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
    if portfolio is None:
        raise Http404
    else:
        portfolio.delete()
        return HttpResponse(status=200)


def get_portfolio_by_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if user is None:
        raise Http404
    portfolio = user.portfolio_set.all().first()
    if portfolio is None:
        portfolio = Portfolio.objects.create(portfolio_user=user)
    return get_portfolio(request, portfolio.pk)

def get_portfolio(request, portfolio_id):
    """

    :param request:
    :param portfolio_id:
    :return:
    """
    assert(request is not None)
    portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
    if portfolio is None:
        raise Http404
    else:
        portfolio_dict = {'portfolio_id': portfolio.portfolio_id,
                          'portfolio_userid': portfolio.portfolio_user.pk,
                          'stocks': [],
                          'risk_history': [],
                          'date_created': '{}'.format(datetime.now())}

        for stock in portfolio.portfolio_stocks.all():
            portfolio_dict['stocks'].append(_calculate_stock_info(stock))

        for risk in portfolio.portfolio_risk.all().order_by('risk_date'):
            portfolio_dict["risk_history"].append(_calculate_risk(risk))

        portfolio_dict['sector_allocations'] = _calculate_sector_allocations(portfolio)

        return HttpResponse(content=json.dumps(portfolio_dict), status=200, content_type='application/json')


def _calculate_stock_info(stock):
    """
    Get's some information for a stock such as symbol, name, price
    :param stock: (Stock)
    :return: (dict)
    """
    current_price = get_current_price(stock.stock_ticker)
    mkt_value = float(current_price*stock.stock_quantity)
    stock_dict = {'ticker': stock.stock_ticker,
                  'name': stock.stock_name,
                  'price': current_price,
                  'quantity': stock.stock_quantity,
                  'mkt_value': mkt_value,
                  'sector': stock.stock_sector}
    return stock_dict


def _calculate_risk(risk):
    """

    :param risk: (Risk)
    :return: (dict)
    """
    risk_dict = {'risk_value': risk.risk_value, 'risk_date': '{}'.format(risk.risk_date)}
    return risk_dict


def _calculate_sector_allocations(portfolio):
    """
    Calculates the sector allocations of a portfolio
    :param portfolio:
    :return: (dict (str):(float)) {"sector": pct_allocation}
    """
    sector_allocations_raw = {}
    for stock in portfolio.portfolio_stocks.all():
        current_price = get_current_price(stock.stock_ticker)
        mkt_value = float(current_price*stock.stock_quantity)
        try:
            sector_allocations_raw[get_company_sector(stock.stock_ticker)] += mkt_value
        except KeyError:
            sector_allocations_raw[get_company_sector(stock.stock_ticker)] = mkt_value

    # calculate sector allocations percentage
    total_mkt_value = sum(sector_allocations_raw.values())
    sector_allocations_pct = {}
    for sector, _mkt_value in sector_allocations_raw.iteritems():
        sector_allocations_pct[sector] = float(_mkt_value/total_mkt_value)

    return sector_allocations_pct
