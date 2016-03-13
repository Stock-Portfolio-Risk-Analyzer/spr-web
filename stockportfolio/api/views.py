from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from datautils import yahoo_finance as yf 
from django.contrib.auth.models import User
from stockportfolio.api.models import Portfolio

def index(request):
    portfolio = Portfolio.objects.get(pk=1)
    context = {"portfolio": portfolio}
    return render_to_response("index.html", context)

def ticker(request, symbol):
    # any api errors bubble up to the user
    return HttpResponse(yf.get_current_price(symbol))

def user_profile(request, user_id):
    user = User.objects.get(user_id)
    if user is None:
        raise Http404
    context =  {
        'user' : user
    }
    return render_to_response('user/user_profile.html')
