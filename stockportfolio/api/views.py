from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from datautils import yahoo_finance as yf
from datautils import stock_info
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from stockportfolio.api.models import Portfolio, Risk, UserSettings, Stock
from stockportfolio.api.utils import update_rri_for_all_portfolios, update_rank_for_all_portfolios
from registration.models import RegistrationManager
import datautils.portfolio_simulation as ps
from stockportfolio.api.api import get_portfolio
import string
import hashlib
from stockportfolio.api.forms import UpdateProfile
from django.core.urlresolvers import reverse
import feedparser
import re
import json



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
    feed = feedparser.parse("http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol="+ticker)
    sanitized_feed = []
    for entry in feed.entries:
        description = re.sub("<.*?>", "", entry.description)
        sanitized_feed.append({
            'title': entry.title,
            'link': entry.link,
            'description': description + "..."
            })
    context = {
        'stock_name': yf.get_company_name(ticker),
        'stock_ticker': ticker,
        'stock_sector': yf.get_company_sector(ticker),
        'stock_feeds' : sanitized_feed,
        'stock_values_month_back' : stock_info.get_price_for_number_of_days_back_from_today(ticker,30),
        'stock_values_week_back' : stock_info.get_price_for_number_of_days_back_from_today(ticker,7),
        'stock_values_year_back' : stock_info.get_price_for_number_of_days_back_from_today(ticker,365),
        'rri_values_week_back' : stock_info.get_company_rri_for_days_back(ticker,7),
        'rri_values_month_back' : stock_info.get_company_rri_for_days_back(ticker,30)
    }
    return render_to_response('modal/stock_interface.html', context)


from django.shortcuts import render

def simulate_portfolio(request, user_id):

    user = get_object_or_404(User, pk=user_id)
    if user is None:
        raise Http404
    portfolios = user.portfolio_set.all()
    p_list = []
    for p in portfolios:
        p_basic_info = {"id": p.pk, "name": p.portfolio_name}
        p_list.append(p_basic_info)


    portfolio = get_portfolio(request, 1)
    portfolio_stocks = json.loads(portfolio.__dict__['_container'][0])['stocks']
    portfolio_dict = {}
    for stock in portfolio_stocks:
        portfolio_dict[stock['ticker']] = stock['quantity']
    # print portfolio_dict
    return ps.plot_rolling_returns(1, portfolio_dict)
    # return render(request, "dashboard/simple_chart.html")#, {"the_script": script, "the_div": div})