from django.contrib import admin
from stockportfolio.api.models import Stock, Portfolio, Risk
# Register your models here.
admin.site.register(Stock)
admin.site.register(Portfolio)
admin.site.register(Risk)