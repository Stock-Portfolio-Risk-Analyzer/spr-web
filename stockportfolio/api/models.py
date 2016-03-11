from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Stock(models.Model):
    stock_id = models.AutoField(primary_key=True)
    stock_price = models.FloatField(default=0)
    stock_ticker = models.CharField(max_length="8" ,default="")
    stock_name = models.CharField(max_length=200)
    stock_beta = models.FloatField(default=0.0)

    def __str__(self):
        return self.stock_id + " " + self.stock_ticker + " " + self.stock_beta


class Portfolio(models.Model):
    portfolio_id = models.AutoField(primary_key=True)
    portfolio_stocks = models.ManyToManyField(Stock)
    portfolio_user = models.ForeignKey(User)
    portfolio_risk = models.FloatField(default=0.0)

    def __str__(self):
        return self.portfolio_id + " " + self.portfolio_risk



