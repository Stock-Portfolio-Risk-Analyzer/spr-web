from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class Stock(models.Model):
    """

    """
    stock_id = models.AutoField(primary_key=True)
    stock_quantity = models.IntegerField(default=0)
    stock_ticker = models.CharField(max_length=8, default="")
    stock_name = models.CharField(max_length=200)
    stock_beta = models.FloatField(default=0.0)
    stock_sector = models.CharField(max_length=200, default="Other")

    def __str__(self):
        return '{} {} {}'.format(self.stock_id, self.stock_ticker, self.stock_beta)


class Risk(models.Model):
    """

    """
    risk_id = models.AutoField(primary_key=True)
    risk_value = models.FloatField(default=0.0)
    risk_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} @ {}'.format(self.risk_value, self.risk_date)


class Portfolio(models.Model):
    """

    """
    portfolio_id = models.AutoField(primary_key=True)
    portfolio_name = models.CharField(max_length=50, null=True, blank=True)
    portfolio_stocks = models.ManyToManyField(Stock)
    portfolio_user = models.ForeignKey(User)
    portfolio_risk = models.ManyToManyField(Risk)

    def __str__(self):
        return '{} {}'.format(self.portfolio_id, self.portfolio_risk)


class UserSettings(models.Model):
    """

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_portfolio = models.ForeignKey(
        Portfolio, on_delete=models.SET_NULL, null=True)
