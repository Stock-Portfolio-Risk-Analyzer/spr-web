from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from datautils import yahoo_finance as yf
from datautils import stock_info
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from stockportfolio.api.models import Portfolio, Risk, UserSettings, Stock
from stockportfolio.api.utils import update_rri_for_all_portfolios, update_rank_for_all_portfolios
from registration.models import RegistrationManager
import string
import hashlib
from stockportfolio.api.forms import UpdateProfile
from django.core.urlresolvers import reverse
import feedparser
import re
import json
from stockportfolio.api.utils import _calculate_risk, _calculate_price


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
    context = {
        "user": request.user, "gravatar": g_url,
        "form": form}
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

def stock_interface(request,ticker):
    ticker = ticker.upper()
    feed = feedparser.parse("http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol="+ticker)
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
        'stock_feeds' : sanitized_feed,
        'risk_history': json.dumps(risk_history),
        'price_history': json.dumps(price_history),
        'current_price' : stock.stock_price.all().order_by('date').last().value
    }
    return render_to_response('modal/stock_interface.html', context)
