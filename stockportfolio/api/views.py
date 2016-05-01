import hashlib
import json
import random
import re
import string
import time
import requests

import feedparser
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)
from django.template.context_processors import csrf

import datautils.portfolio_simulation as ps
import stockportfolio.api.rec_utils as rec_utils
from stockportfolio.api.api import _calculate_stock_info
from stockportfolio.api.datautils import yahoo_finance as yf
from stockportfolio.api.datautils import sentiment, stock_info
from stockportfolio.api.forms import PortfolioUploadForm, UpdateProfile
from stockportfolio.api.models import Portfolio, Stock, UserSettings
from stockportfolio.api.utils import (_calculate_price, _calculate_risk,
                                      update_rank_for_all_portfolios,
                                      update_rri_for_all_portfolios)


def dashboard(request):
    if request.user.is_anonymous():
        return redirect("/")
    email = string.lower(string.strip(request.user.email, string.whitespace))
    g_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email).hexdigest()
    user_settings = UserSettings.objects.get_or_create(user=request.user)[0]
    form = UpdateProfile(instance=request.user)
    form.fields['default_portfolio'].queryset = Portfolio.objects.filter(
        portfolio_user=request.user)
    form.fields['default_portfolio'].initial = user_settings.default_portfolio

    stock_tickers = list(Stock.objects.all().values_list("stock_ticker"))
    stock_tickers.extend(Stock.objects.all().values_list("stock_name"))
    if stock_tickers:
        stock_tickers = zip(*stock_tickers)
        stock_tickers = json.dumps(stock_tickers[0])
    else:
        stock_tickers = json.dumps(['No stocks', 'No stocks found'])

    upload_portfolio_form = PortfolioUploadForm()
    context = {
        "user": request.user, "gravatar": g_url,
        "form": form,
        "upload_portfolio_form": upload_portfolio_form,
        "stock_tickers": stock_tickers,
    }
    context.update(csrf(request))
    return render_to_response("index.html", context)


def landing(request):
    """Renders the landing page"""
    if request.user.is_anonymous():
        return render_to_response('landing.html')
    else:
        return redirect("/dashboard/")


def ticker(request, symbol):
    # any api errors bubble up to the user
    return HttpResponse(yf.get_current_price(symbol))


def company_name(request, symbol):
    # any api errors bubble up to the user
    return HttpResponse(yf.get_company_name(symbol))


def user_profile(request, user_id):
    user = User.objects.get(user_id)
    if user is None:
        raise Http404
    context = {
        'user': user
    }
    return render_to_response('user/user_profile.html', context)


def calculate_all_rris(request):
    update_rri_for_all_portfolios()
    update_rank_for_all_portfolios()
    return HttpResponse(status=200)


def modify_account(request):
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dashboard'))
    form = UpdateProfile(instance=request.user)
    return render(request, 'modal/modify_account.html', {"form": form})


def stock_interface(request, ticker):
    ticker = ticker.upper()
    stock = get_object_or_404(
        Stock, Q(stock_ticker=ticker) | Q(stock_name__iexact=ticker))
    ticker = stock.stock_ticker
    feed = feedparser.parse(
        "http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol=" + ticker)
    sanitized_feed = []
    for entry in feed.entries:
        description = re.sub("<.*?>", "", entry.description)
        sanitized_feed.append({
            'title': entry.title,
            'link': entry.link,
            'description': description + "..."
        })
    stock = Stock.objects.get(stock_ticker=ticker)
    risk_history = []
    price_history = []
    for risk in stock.stock_risk.all().order_by('risk_date'):
        risk_history.append(_calculate_risk(risk))
    for price in stock.stock_price.all().order_by('date'):
        price_history.append(_calculate_price(price))

    context = {
        'stock_name': stock.stock_name,
        'stock_ticker': ticker,
        'stock_sector': stock.stock_sector,
        'stock_feeds': sanitized_feed,
        'risk_history': json.dumps(risk_history),
        'price_history': json.dumps(price_history),
        'current_price': stock.stock_price.all().order_by('date').last().value,
        'sentiment_value': sentiment.get_stock_sentiment(ticker)
    }
    return render_to_response('modal/stock_interface.html', context)


def stock_rec(request, portfolio_id, rec_type):
    recs = rec_utils.stock_recommender(request, portfolio_id, rec_type)
    message = ''
    if rec_type == 'stable':
        title = 'And now for something completely the same'
        message = 'Here are some stocks that will \
            minimize changes to your risk'
    elif rec_type == 'high_risk':
        title = 'Go big or go home!'
        message = 'Adding these stocks to your portfolio \
            will increase its risk'
    elif rec_type == 'low_risk':
        title = 'Slow and steady wins the race.'
        message = 'Using these stocks, lower your portfolio\'s risk'
    else:
        title = 'Get out of your niche.'
        message = 'Here are some stocks with sectors not in your portfolio'
    context = {
        'title': title,
        'message': message,
        'stocks': recs
    }
    return render_to_response('modal/recommendation.html', context)


def generate_portfolio(request):
    """
    Generates one of several types of portfolios, possibly with input from
    either the user's default portfolio or their first portfolio if they have
    not selected a default. If there are no user portfolios, a risk between
    -2.5 and 2.5 is selected.
    :param request
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
            lambda x: x <= p_risk,
            all_stocks, random.randint(lower_bound, upper_bound))
    elif(p_type == 'diverse'):
        message = 'We chose this portfolio with sector diversity in mind.'
        new_portfolio = rec_utils.get_sector_stocks(
            portfolio, all_stocks,
            random.randint(lower_bound, upper_bound), True)
    else:
        message = 'We chose this portfolio to be risker'
        if is_user_portfolio:
            message += ' than your current default portfolio.'
        else:
            ' than ' + str(p_risk)
        new_portfolio = rec_utils.get_recommendations(
            lambda x: x > p_risk, all_stocks,
            random.randint(lower_bound, upper_bound))
    new_portfolio, v, tlow, thi = rec_utils.determine_stock_quantities(
        portfolio, new_portfolio)
    end = time.time() - start
    message += ' The targeted range for the portfolio value was '
    message += '${:,.2f}'.format(tlow) + ' to ' + '${:,.2f}'.format(thi) + '.'
    message += ' The actual value is ' + '${:,.2f}'.format(v) + '.'
    message += ' Portfolio generation took {:,.2f} seconds.'.format(end)
    symbols = []
    quantities = []
    for stock in new_portfolio:
        symbols.append(stock['ticker'].encode('ascii'))
        quantities.append(stock['quantity'])
    context = {'message': message,
               'symbols': symbols,
               'quantities': quantities,
               'portfolio': new_portfolio}
    context.update(csrf(request))
    return render_to_response('modal/gen_portfolio.html', context)


def simulate_portfolio(request, portfolio_id):
    if not settings.ADVANCED_SETTINGS['SIMULATION_ENABLED']:
        url = settings.ADVANCED_SETTINGS['REMOTE_SIMULATION_URL'] + request.path
        return requests.get(url).content()

    portfolio = get_object_or_404(Portfolio, portfolio_id=portfolio_id)
    if not portfolio.portfolio_stocks.count() > 0:
        return HttpResponse(status=400)
    portfolio_stocks = []
    for stock in portfolio.portfolio_stocks.all():
        portfolio_stocks.append(_calculate_stock_info(stock))

    portfolio_dict = {}
    for stock_dict in portfolio_stocks:
        portfolio_dict[stock_dict['ticker']] = stock_dict['quantity']
    return ps.create_returns_tear_sheet(
        portfolio.portfolio_name, portfolio_dict)
