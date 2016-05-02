import csv
import json
import operator
import random
import time
from datetime import datetime

from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import stockportfolio.api.rec_utils as rec_utils
from datautils.yahoo_finance import (get_company_name, get_company_sector,
                                     get_current_price)
from stockportfolio.api.forms import PortfolioUploadForm
from stockportfolio.api.models import (Portfolio, PortfolioRank,
                                       PortfolioValue, Stock, StockPortfolio,
                                       UserSettings)
from stockportfolio.api.utils import _calculate_risk


def add_stock(request, portfolio_id):
    """
    Adds Stock to Portfolio

    :param request: HTTP Request Object
    :param portfolio_id: (int) ID for the Portoflio Object
    :return: HTTPResponse
        - CODE - 200 if successful, 403 if unauthorized user is
        requesting, 400 if specified stock not found in Database
    """
    portfolio = get_object_or_404(Portfolio, portfolio_id=portfolio_id)
    if portfolio.portfolio_user.pk is not request.user.pk:
        return HttpResponse(status=403)
    stock_ticker = request.GET.get('stock', None)
    stock_quantity = request.GET.get('quantity', None)
    overwrite = request.GET.get('overwrite', None)
    if stock_ticker:
        if overwrite:
            added = _add_stock_helper(
                portfolio, stock_quantity, stock_ticker, False)
        else:
            added = _add_stock_helper(portfolio, stock_quantity, stock_ticker)
        if not added:
            raise Http404
        else:
            return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


def remove_stock(request, portfolio_id):
    """
    Removes Stock from Portfolio

    :param request: HTTP Request Object
    :param portfolio_id: (int) ID for the Portoflio Object
    :return: HTTPResponse
     - CODE - 200 if successful, 403 if unauthorized user is requesting, 400 if
     specified stock or portfolio are not found in Database
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
    Creates a portfolio for a specified user.

    :param request: HTTP Request Object
    :param user_id: (int) ID for the User Object
    :return: HTTPResponse
    - JSON - {'id'(portfolio_id)} - id of newly created portfolio
    - CODE - 200 if successful, 404 if user not found.
    """
    assert(request is not None)
    user = User.objects.get(pk=user_id)
    if user is not None:
        portfolio = Portfolio.objects.create(portfolio_user=user)
        portfolio.save()
        return HttpResponse(json.dumps({"id": portfolio.pk}), status=200)
    else:
        raise Http404


def delete_portfolio(request, portfolio_id):
    """
    Deletes the specified portfolio from the Database.

    :param request: HTTP Request Object
    :param portfolio_id: (int) ID for the Portoflio Object
    :return: HTTPResponse
     - CODE - 200 if successful, 403 if unauthorized user is requesting.
    """
    portfolio = get_object_or_404(Portfolio, portfolio_id=portfolio_id)
    if portfolio.portfolio_user.pk is not request.user.pk:
        return HttpResponse(status=403)
    portfolio.delete()
    return HttpResponse(status=200)


def get_portfolio_by_user(request, user_id):
    """
    Returns the default portfolio for the user if it has one specified
    else it returns one of the portfolio's of the user (random), if the
    user doesn't have one it will create a new one.

    :param request: HTTP Request Object
    :param user_id: (int) ID for the User Object
    :return: HTTPResponse
    - JSON - Look at get_portfolio documentation function for JSON info.
    - CODE - 200 if successful, 404 if not found.
    """
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
    """
        Returns the list of portfolios for the user with their name and id.

        :param request: HTTP Request Object
        :param user_id: (int) ID for the User Object
        :return: HTTPResponse
        - JSON - {'portfolio_list': [{"id"(portfolio_id),
                    "name"(portfolio_name)},...]}
        - CODE - 200 if successful, 404 if not found.
    """
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


def get_public_portfolio(request, portfolio_id):
    """
    Returns public information for a specified portfolio.

    :param request: (HTTPRequest) HTTP Request Object
    :param portfolio_id: (int) Portfolio unique id
    :return: {'portfolio_id' (int), 'name' (str), 'stocks':[(stock_info),...]}
    """
    portfolio = get_object_or_404(Portfolio, portfolio_id=portfolio_id)

    portfolio_dict = {'portfolio_id': portfolio.portfolio_id,
                      'name': portfolio.portfolio_name,
                      'stocks': []}

    for stock in portfolio.portfolio_stocks.all():
        portfolio_dict['stocks'].append(_calculate_stock_info(stock))

    return HttpResponse(content=json.dumps(portfolio_dict),
                        status=200, content_type='application/json')


def get_portfolio(request, portfolio_id):
    """
    Returns thorough information for the specified portfolio_id

    :param request: HTTP Request Object
    :param portfolio_id: (int) ID for the Portfolio Object
    :return: HTTPResponse
    - JSON -
    {'portfolio_id'(int), 'name'(str), 'portfoio_user_id'(int),
    'stocks'(list), 'risk_history'(list), 'date_created'(list),
    'rank'(list), 'sector_alloactions'(list)}
    - CODE - 200 if successful, 404 if not found.
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

        portfolio_dict['sector_allocations'] = _calculate_sector_allocations(
            portfolio)

        return HttpResponse(content=json.dumps(portfolio_dict),
                            status=200, content_type='application/json')


def modify_portfolio_form_post(request, portfolio_id):
    """
    Parses Portfolio Form Post. Given our Front-End generates a dynamic
    form, since the user is allowed to add rows and remove them we had
    to parse it manually.

    :param request: (HTTPRequest) HTTP Request Object
    :param portfolio_id: (int) id of the portfolio to be modified
    :return: HTTPResponse
    - JSON -
        if invalid the json will include:
        {"success" : "false", "message": an error message}
        if valid the json will include:
        {"success" : "true"}
    - CODE - 200 if successful, 400 if invalid
    """
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
            return HttpResponse(json.dumps({"success": "true"}))
        err_message = ["The following stock symbols are invalid:"]
        err_message.extend(invalid_stocks)
        err_message = " ".join(err_message)
        err_message = json.dumps({"success": "false", "message": err_message})
        return HttpResponse(content=err_message,
                            status=400,
                            content_type="application/json charset=utf-8")


def generate_portfolio(request):
    """
    Generates one of several types of portfolios, possibly with input from
    either the user's default portfolio or their first portfolio if they have
    not selected a default. If there are no user portfolios, a risk between
    -2.5 and 2.5 is selected.

    :param request: (HTTPRequest) HTTP Request Object
    :return: HTTPResponse
    - CODE - 200 if successful, 403 if unauthorized
    - JSON - {"message"(str)} Useful message on why the portfolio was
     generated.
    """
    if request.user.is_anonymous():
        return HttpResponse(status=403)
    upper_bound = random.randint(16, 20)
    lower_bound = random.randint(3, 10)
    start = time.time()
    user_settings = UserSettings.objects.get_or_create(user=request.user)[0]
    portfolio, p_risk, is_user_portfolio = rec_utils.get_portfolio_and_risk(
        request.user, user_settings)
    rec_utils.fetch_tickers(portfolio)
    all_stocks = rec_utils.stock_slice(Stock.objects.all(), 1000)
    new_portfolio = None
    message = ""
    r = random.Random(int(time.time()))
    p_type = r.choice(['safe', 'risky', 'diverse'])
    if(p_type == 'safe'):
        message = 'We chose this portfolio to have a lower risk'
        if is_user_portfolio:
            message += ' than your current default portfolio.'
        else:
            ' number than ' + str(p_risk)
        new_portfolio = rec_utils.get_recommendations(
            lambda x: x <= p_risk, all_stocks, random.randint(
                lower_bound, upper_bound))
    elif(p_type == 'diverse'):
        message = 'We chose this portfolio with sector diversity in mind.'
        new_portfolio = rec_utils.get_sector_stocks(
            portfolio, all_stocks, random.randint(lower_bound, upper_bound),
            True)
    else:
        message = 'We chose this portfolio to be risker'
        if is_user_portfolio:
            message += ' than your current default portfolio.'
        else:
            ' than ' + str(p_risk)
        new_portfolio = rec_utils.get_recommendations(
            lambda x: x > p_risk, all_stocks, random.randint(
                lower_bound, upper_bound))
    new_portfolio, v, tlow, thi = rec_utils.determine_stock_quantities(
        portfolio, new_portfolio)

    end = time.time() - start
    message += ' The targeted range for the portfolio value was '
    message += '${:,.2f}'.format(tlow) + ' to ' + '${:,.2f}'.format(thi) + '.'
    message += ' The actual value is ' + '${:,.2f}'.format(v) + '.'
    message += ' Portfolio generation took {:,.2f} seconds.'.format(end)
    generated_dict = {'message': message,
                      'portfolio': new_portfolio}

    return HttpResponse(content=json.dumps(generated_dict), status=200,
                        content_type='application/json')


@csrf_exempt
def modify_gen(request, portfolio_id):
    """
    Adds a generated portfolio stocks into the specified portfolio_id.

    :param request: (HTTPRequest) HTTP Request Object - includes form data
     with {'data': {'symbols'(list), 'quantities'(list}, 'name'(str)}}
    :param portfolio_id: (int) Portfolio ID where generated portfolio
     will be added.
    :return: (HTTPResponse) 200 if successful, 403 if forbidden, 404
     if Portfolio was not found.
    """
    if request.method == 'POST':
        data = request.POST.get("data", None)
        data = json.loads(data)
        user_portfolio = get_object_or_404(Portfolio,
                                           portfolio_id=portfolio_id)
        for i in range(len(data["symbols"])):
            stock = data["symbols"][i]
            quantity = data["quantities"][i]
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
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def list_top_portfolios(request, category):
    """
    Searches the DB and returns json list of top portfolios for specified
    category.

    :param request: (HTTPRequest) HTTP Request Object
    :param category: (int)
        0 - most risky
        1 - least risky
        2 - most valuable
        3 - least valuable
    """
    category = int(category)
    if category < 0 or category > 3:
        return HttpResponse(status=400)
    portfolios = []
    if category == 0 or category == 1:
        rank = PortfolioRank.objects.order_by('-date').first()
        if not rank:
            return HttpResponse(status=400)
        date = rank.date.date()
        ranks = PortfolioRank.objects.filter(
            date__year=date.year, date__month=date.month, date__day=date.day)
        if category == 0:
            filtered = ranks.order_by('value').distinct('value')[:10]
        elif category == 1:
            filtered = ranks.order_by('-value').distinct('value')[:10]
    elif category == 2 or category == 3:
        value = PortfolioValue.objects.order_by('-date').first()
        if not value:
            return HttpResponse(status=400)
        date = value.date.date()
        values = PortfolioValue.objects.filter(
            date__year=date.year, date__month=date.month, date__day=date.day)
        if category == 2:
            filtered = (values.distinct('portfolio__portfolio_id')
                        .order_by('portfolio__portfolio_id'))
            filtered = sorted(
                filtered, key=operator.attrgetter('value'), reverse=True)[:10]
        elif category == 3:
            filtered = (values.distinct('portfolio__portfolio_id')
                        .order_by('portfolio__portfolio_id'))
            filtered = sorted(
                filtered, key=operator.attrgetter('value'))[:10]
    for idx, fr in enumerate(filtered):
        p = fr.portfolio
        rri = p.portfolio_risk.order_by('-risk_date').first()
        rri = 0 if not rri else rri.risk_value
        value = p.portfoliovalue_set.order_by('-date').first()
        value = 0 if not value else value.value
        p_info = {
            'id': p.portfolio_id,
            'rank': idx + 1,
            'name': p.portfolio_name,
            'rri': rri,
            'value': value}
        portfolios.append(p_info)
    return HttpResponse(content=json.dumps(portfolios), status=200,
                        content_type='application/json')


def download_porfolio_data(request, portfolio_id):
    """
    Downloads a CSV file representation for the specified portfolio.

    :param request: (HTTPRequest) HTTP Request Object
    :param portfolio_id: ID for the portfolio we wish to download.
    :return: (HTTPResponse) with attachment named 'backup-[portfolio_name].csv'
    """
    portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
    if portfolio.portfolio_user.pk is not request.user.pk:
        return HttpResponse(status=403)
    response = HttpResponse(content_type='text/csv')
    portfolio_name = portfolio.portfolio_name
    portfolio_name = portfolio_name if portfolio_name else 'portfolio'
    portfolio_name = 'attachment; filename="backup-{}.csv"'.format(
        portfolio_name)
    response['Content-Disposition'] = portfolio_name
    writer = csv.writer(response)
    writer.writerow(['symbol', 'name', 'sector', 'quantity', 'risk'])
    for sp in portfolio.portfolio_stocks.all():
        stock = sp.stock
        last_risk = stock.stock_risk.all().order_by('risk_date').last()
        if last_risk is None:
            last_risk = 0
        else:
            last_risk = last_risk.risk_value
        writer.writerow([stock.stock_ticker, stock.stock_name,
                         stock.stock_sector, sp.quantity,
                         last_risk])
    return response


def upload_portfolio_data(request):
    """
    Uses Portfolio Form to allow user to upload a Portfolio Information CSV
    File.

    :param request: (HTTPRequest) Request Object
    :return: HTTPResponse
     - CODE - 200 if successful, 500 if invalid portfolio_id or if invalid
     form fields.
     - JSON - {'portfolio_id' (int)} of newly created portfolio.
    """
    if request.method == 'POST':
        form = PortfolioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio_id = _parse_portfolio_file(
                request.FILES['file'], request.user)
            if portfolio_id is None:
                return HttpResponse(status=500)
            return HttpResponse(
                content=json.dumps({"portfolio_id": portfolio_id}), status=200,
                content_type='application/json')
        return HttpResponse(status=500)


def _parse_portfolio_file(file, user):
    """
    Parses a csv File extracts symbols and quantities and creates a portfolio
    for the specified user.

    :param file: (File) CSV Format File with Portfolio Informaiton
    :param user: (User) User to add the protfolio object
    :return: ID for Portfolio Object Created, None if failed to create one.
    """
    df = csv.DictReader(file)
    portfolio = Portfolio.objects.create(portfolio_user=user)
    for row in df:
        try:
            stock = Stock.objects.get(stock_ticker=row["symbol"])
            stockportfolio = StockPortfolio.objects.create(
                stock=stock, quantity=row["quantity"])
            stockportfolio.save()
            portfolio.portfolio_stocks.add(stockportfolio)
        except None:
            return None
    return portfolio.pk


def _diversify_by_sector(portfolio):
    """
    Returns a list of Stock objects which are from sectors not currently
    included in the specified porfolio

    :param portfolio: (Portfolio) Portfolio object to check for sectors
    :return: stocks from various sectors not present in portfolio
    """
    sectors = list(portfolio.portfolio_stocks.
                   values_list('stock_sector').distinct())
    q = Stock.objects.all()
    for sector in sectors:
        q.exclude(stock_sector=sector)
    return list(q)


def _add_stock_helper(portfolio, stock_quantity, stock_ticker, overwrite=True):
    """
    Given a portfolio object it creates and adds a stock object to it.

    :param portfolio: (Portfolio) Portfolio to add stocks to
    :param stock_quantity: (int) quantity of stocks to be added
    :param stock_ticker: (str) stock symbol to be added
    :param overwrite: if stock exists it is ovewritted with new quantity.
    :return: True if successful, False otherwise.
    """
    stock_name = get_company_name(stock_ticker)
    stock_sector = get_company_sector(stock_ticker)
    try:
        stock = Stock.objects.get_or_create(
            stock_name=stock_name,
            stock_ticker=stock_ticker,
            stock_sector=stock_sector)[0]
        sp = portfolio.portfolio_stocks.get_or_create(
            stock=stock, defaults={'quantity': float(stock_quantity)})[0]
        if overwrite:
            sp.quantity = stock_quantity
        else:
            sp.quantity += float(stock_quantity)
        sp.save()
        return True
    except None:
        return False


def _verify_stock_ticker_validity(stocks, quantity):
    """
    Verifies if Stock Tickers are valid, by checking through our DB of Stocks.
    Both stock and quantity have a one-to-one correspondence for each stock
    symbol and their corresponding quantity.

    :param stocks: list(str) - List of Stock Symbols
    :param quantity: list(str) - List of Stock Quantities
    :return: list(str) - List of Invalid Stock Symbols, can be empty list.
    """
    invalid_stocks = []
    for stock in stocks.values():
        try:
            get_company_name(stock)
        except (KeyError, IndexError):
            invalid_stocks.append(stock)
    # remove any invalid stocks with quantity 0
    for i, stock in stocks.items():
        if stock in invalid_stocks and int(quantity[i]) == 0:
            invalid_stocks.remove(stock)

    return invalid_stocks


def _calculate_stock_info(stock_portfolio):
    """
    Get's some information for a stock such as symbol, name, price.

    :param stock: (Stock)
    :return: (dict)
    """
    stock = stock_portfolio.stock
    current_price = get_current_price(stock.stock_ticker)
    if not current_price:
        current_price = 0.0
    mkt_value = float(current_price * stock_portfolio.quantity)
    stock_dict = {'ticker': stock.stock_ticker,
                  'name': stock.stock_name,
                  'price': current_price,
                  'quantity': stock_portfolio.quantity,
                  'mkt_value': mkt_value,
                  'sector': stock.stock_sector}
    return stock_dict


def _calculate_sector_allocations(portfolio):
    """
    Calculates the sector allocations of a portfolio.

    :param portfolio: (Portfolio)
    :return: (dict (str):(float)) {"sector": pct_allocation}
    """
    sector_allocations_raw = {}
    for sp in portfolio.portfolio_stocks.all():
        current_price = get_current_price(sp.stock.stock_ticker)
        if not current_price:
            current_price = 0.0
        mkt_value = float(current_price * sp.quantity)
        sector = get_company_sector(sp.stock.stock_ticker)
        try:
            sector_allocations_raw[sector] += mkt_value
        except KeyError:
            sector_allocations_raw[sector] = mkt_value

    # calculate sector allocations percentage
    total_mkt_value = sum(sector_allocations_raw.values())
    sector_allocations_pct = {}
    for sector, _mkt_value in sector_allocations_raw.iteritems():
        sector_allocations_pct[sector] = float(_mkt_value / total_mkt_value)

    return sector_allocations_pct
