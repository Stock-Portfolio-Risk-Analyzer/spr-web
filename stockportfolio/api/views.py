from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, Http404
from datautils import yahoo_finance as yf
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from stockportfolio.api.models import Portfolio
import string
import hashlib

def dashboard(request):
    email = string.lower(string.strip(request.user.email, string.whitespace))
    g_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email).hexdigest()
    context = {"user" : request.user, "gravatar": g_url}
    context.update(csrf(request))
    return render_to_response("index.html", context)


def landing(request):
    """Renders the landing page"""
    return render_to_response('landing.html')

def profile(request):
    un = request.POST['accountName']
    email = request.POST['accountEmail']
    request.user.username = un;
    request.user.email = email;
    request.user.save() 
    return redirect('dashboard')

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
