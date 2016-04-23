import json
from datetime import datetime
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from stockportfolio.api.models import Portfolio, Stock, UserSettings, PortfolioRank, StockPortfolio
from datautils.yahoo_finance import get_current_price, get_company_name, get_company_sector
from django.shortcuts import get_object_or_404
from stockportfolio.api.utils import _calculate_risk


def add_stock(request, portfolio_id):
    """
    Add a stock to a portfolio.
    :param request:
    :param portfolio_id:
    :return:
    """
    portfolio = get_object_or_404(Portfolio, portfolio_id=portfolio_id)
    if portfolio.portfolio_user.pk is not request.user.pk:
        return HttpResponse(status=403)
    stock_ticker = request.GET.get('stock', None)
    stock_quantity = request.GET.get('quantity', None)
    if stock_ticker is not None:
        added = _add_stock_helper(portfolio, stock_quantity, stock_ticker)
        if not added:
            raise Http404
        else:
            return HttpResponse(status=200)


def remove_stock(request, portfolio_id):
    """
    Remove a stock from the portfolio
    :param request:
    :param portfolio_id:
    :return:
    """
    portfolio = get_object_or_404(Portfolio, portfolio_id=portfolio_id)
    if portfolio.portfolio_user.pk is not request.user.pk:
        return HttpResponse(status=403)
    stock_ticker = request.GET.get('stock', None)
    if stock_ticker is not None and portfolio is not None:
        sp = portfolio.portfolio_stocks.filter(
            stock__stock_ticker=stock_ticker).first()
        if sp is not None:
            sp.delete()
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
        return HttpResponse(json.dumps({"id" : portfolio.pk}), status=200)
    else:
        raise Http404


def delete_portfolio(request, portfolio_id):
    """
    Deletes a portfolio based on portfolio_id.
    :param request:
    :param portfolio_id:
    :return:
    """
    portfolio = get_object_or_404(Portfolio, portfolio_id=portfolio_id)
    if portfolio.portfolio_user.pk is not request.user.pk:
        return HttpResponse(status=403)
    portfolio.delete()
    return HttpResponse(status=200)


def get_portfolio_by_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_settings = UserSettings.objects.get_or_create(user=user)[0]
    if user_settings.default_portfolio:
        portfolio = user_settings.default_portfolio
    else:
        portfolio = user.portfolio_set.all().first()
    if portfolio is None:
        portfolio = Portfolio.objects.create(portfolio_user=user)
    return get_portfolio(request, portfolio.pk)


def get_list_of_portfolios(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user is None:
        raise Http404
    portfolios = user.portfolio_set.all()
    p_list = []
    for p in portfolios:
        p_basic_info = {"id": p.pk, "name": p.portfolio_name}
        p_list.append(p_basic_info)
    return HttpResponse(content=json.dumps({"portfolio_list": p_list}),
                        status=200, content_type='application/json')


def get_portfolio(request, portfolio_id):
    """

    :param request:
    :param portfolio_id:
    :return:
    """
    assert(request is not None)
    portfolio = get_object_or_404(Portfolio, portfolio_id=portfolio_id)
    rank = PortfolioRank.objects.filter(
        portfolio=portfolio).order_by('-date').first()
    if rank:
        rank = rank.value
    if portfolio.portfolio_user.pk is not request.user.pk:
        return HttpResponse(status=403)
    else:
        portfolio_dict = {'portfolio_id': portfolio.portfolio_id,
                          'name': portfolio.portfolio_name,
                          'portfolio_userid': portfolio.portfolio_user.pk,
                          'stocks': [],
                          'risk_history': [],
                          'date_created': '{}'.format(datetime.now()),
                          'rank': rank}

        for stock in portfolio.portfolio_stocks.all():
            portfolio_dict['stocks'].append(_calculate_stock_info(stock))

        for risk in portfolio.portfolio_risk.all().order_by('risk_date'):
            portfolio_dict["risk_history"].append(_calculate_risk(risk))

        portfolio_dict['sector_allocations'] = _calculate_sector_allocations(portfolio)

        return HttpResponse(content=json.dumps(portfolio_dict),
                            status=200, content_type='application/json')


def modify_portfolio_form_post(request, portfolio_id):
    if request.method == 'POST':
        data = request.POST.get("data", None)
        data = json.loads(data)
        invalid_stocks = _verify_stock_ticker_validity(data["symbols"],
                                                       data["quantities"])
        if data is not None and len(invalid_stocks) == 0:
            user_portfolio = get_object_or_404(Portfolio,
                                               portfolio_id=portfolio_id)
            for i in range(len(data["symbols"])):
                stock = data["symbols"][str(i)]
                quantity = int(data["quantities"][str(i)])
                user_id = request.user.id
                if user_portfolio.portfolio_user.pk is not request.user.pk:
                    return HttpResponse(status=403)
                user_has_stock = user_portfolio.portfolio_stocks.filter(
                    stock__stock_ticker=stock).exists()
                if user_has_stock:
                    if quantity <= 0:
                        user_portfolio.portfolio_stocks.all().get(
                            stock__stock_ticker=stock).delete()
                    else:
                        user_portfolio.portfolio_stocks.filter(
                            stock__stock_ticker=stock).update(
                                        quantity=quantity)
                elif quantity > 0:
                    _add_stock_helper(user_portfolio, quantity, stock)
            if data["name"]:
                user_portfolio.portfolio_name = data["name"]
                user_portfolio.save()
            return HttpResponse(json.dumps({"success" : "true"}))
        err_message = ["The following stock symbols are invalid:"]
        err_message.extend(invalid_stocks)
        err_message = " ".join(err_message)
        err_message = json.dumps({"success" : "false","message" : err_message})
        return HttpResponse(content=err_message,
                            status=400,
                            content_type="application/json charset=utf-8")


def stock_rec(request, portfolio_id):
    """
    Returns stock recommendations in several categories based on a specific
    portfolio
    :param request
    :param portfolio_id
    """
    portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
    if portfolio.portfolio_user.pk is not request.user.pk:
        return HttpResponse(status=403)
    risks = portfolio.portfolio_risk.all()
    if len(risks) == 0:
        err = 'No recommendations available at this time.'
        err_dict = { 'low':err,
                     'high': err,
                     'stable':err,
                     'diverse':err }
        return HttpResponse(content=json.dumps(err_dict), status=200,
                        content_type='application/json')
    p_risk = risks[0].risk_value
    jsonify = lambda x: { i:x.__dict__[i]
                         # Django inserts a "_state" attribute into every
                         # model. We don't need it in our json, so it's
                         # removed here
                         for i in x.__dict__ if i !=  "_state" }
    less_risk = map(jsonify,
                    list(Stock.objects.exclude(stock_beta__lt=p_risk)))
    more_risk = map(jsonify,
                    list(Stock.objects.exclude(stock_beta__gt=p_risk)))
    diverse   = map(jsonify,
                    list(_diversify_by_sector(portfolio)))
    # stock w/ in a 20% range of current portfolio riskiness
    stable = map(jsonify, list(Stock.objects.exclude(
                         stock_beta__gt=(1.1 * p_risk)
                   ).exclude(
                           stock_beta__lt=0.9 * p_risk
                   )))
    rec_dict = {'low'    :less_risk[:4],
                'high'   :more_risk[:4],
                'diverse':diverse[:4],
                'stable' :stable[:4] }
    return HttpResponse(content=json.dumps(rec_dict), status=200,
                        content_type='application/json')


def _diversify_by_sector(portfolio):
    """
    :param portfolio
    :return stocks from various sectors not present in portfolio
    """
    sectors = list(portfolio.portfolio_stocks.
                   values_list('stock_sector').distinct())
    q = Stock.objects.all()
    for sector in sectors:
        q.exclude(stock_sector=sector)
    return list(q)


def _add_stock_helper(portfolio, stock_quantity, stock_ticker):
    stock_name = get_company_name(stock_ticker)
    stock_sector = get_company_sector(stock_ticker)
    try:
        stock = Stock.objects.get_or_create(
            stock_name=stock_name,
            stock_ticker=stock_ticker,
            stock_sector=stock_sector)[0]
        sp = StockPortfolio(stock=stock, quantity=stock_quantity)
        sp.save()
        portfolio.portfolio_stocks.add(sp)
        return True
    except None:
        return False


def _verify_stock_ticker_validity(stocks, quantity):
    invalid_stocks = []
    for stock in stocks.values():
        try:
            stock_sector = get_company_name(stock)
        except (KeyError, IndexError):
            invalid_stocks.append(stock)
    #remove any invalid stocks with quantity 0
    for i, stock in stocks.items():
        if stock in invalid_stocks and int(quantity[i]) == 0:
            invalid_stocks.remove(stock)

    return invalid_stocks


def _calculate_stock_info(stock_portfolio):
    """
    Get's some information for a stock such as symbol, name, price
    :param stock: (Stock)
    :return: (dict)
    """
    stock = stock_portfolio.stock
    current_price = get_current_price(stock.stock_ticker)
    mkt_value = float(current_price*stock_portfolio.quantity)
    stock_dict = {'ticker': stock.stock_ticker,
                  'name': stock.stock_name,
                  'price': current_price,
                  'quantity': stock_portfolio.quantity,
                  'mkt_value': mkt_value,
                  'sector': stock.stock_sector}
    return stock_dict


def _calculate_sector_allocations(portfolio):
    """
    Calculates the sector allocations of a portfolio
    :param portfolio:
    :return: (dict (str):(float)) {"sector": pct_allocation}
    """
    sector_allocations_raw = {}
    for sp in portfolio.portfolio_stocks.all():
        current_price = get_current_price(sp.stock.stock_ticker)
        mkt_value = float(current_price*sp.quantity)
        sector = get_company_sector(sp.stock.stock_ticker)
        try:
            sector_allocations_raw[sector] += mkt_value
        except KeyError:
            sector_allocations_raw[sector] = mkt_value

    # calculate sector allocations percentage
    total_mkt_value = sum(sector_allocations_raw.values())
    sector_allocations_pct = {}
    for sector, _mkt_value in sector_allocations_raw.iteritems():
        sector_allocations_pct[sector] = float(_mkt_value/total_mkt_value)

    return sector_allocations_pct


