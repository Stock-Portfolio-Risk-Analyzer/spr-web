from django.shortcuts import render
from django.http import HttpResponse
from datautils import yahoo_finance as yf 

def index(request):
    return HttpResponse("hello")

def ticker(request, symbol):
    # any api errors bubble up to the user
    return HttpResponse(yf.get_current_price(symbol))
