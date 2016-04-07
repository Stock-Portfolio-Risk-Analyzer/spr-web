from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from datautils import yahoo_finance as yf
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from stockportfolio.api.models import Portfolio, Risk
from stockportfolio.api.utils import update_rri_for_all_portfolios, update_rank_for_all_portfolios
from registration.models import RegistrationManager
import string
import hashlib
from stockportfolio.api.forms import UpdateProfile
from django.core.urlresolvers import reverse


def dashboard(request):
    if request.user.is_anonymous():
        return redirect("/")
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
    if request.user.username != un:
        request.user.username = un
        request.user.save()
    if request.user.email != email:
        request.user.email = email
        request.user.save()
        # r = RegistrationManager()
        # r.resend_activation_mail(request.user.email,"", request)
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


def calculate_all_rris(request):
    update_rri_for_all_portfolios()
    update_rank_for_all_portfolios()
    return HttpResponse(status=200)


def modify_account(request,username):
    args = {}
    user = User.objects.get(username = username)
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        print ("before validation")
        if form.is_valid():
            print ("Here ")
            form.save()
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            print form.errors
            print "not valid"

    else:
        form = UpdateProfile(instance = request.user)
    args['form'] = form
    return render(request, 'modal/modify_account.html', {"form": form})
