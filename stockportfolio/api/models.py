from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Risk(models.Model):
    """

    """
    risk_id = models.AutoField(primary_key=True)
    risk_value = models.FloatField(default=0.0)
    risk_date = models.DateTimeField()

    def __str__(self):
        return '{} @ {}'.format(self.risk_value, self.risk_date)

    def save(self, *args, **kwargs):
        if not self.risk_date:
            self.risk_date = timezone.now()
        super(Risk, self).save(*args, **kwargs)


class Price(models.Model):
    """

    """
    value = models.FloatField()
    date = models.DateTimeField()

class Stock(models.Model):
    """

    """
    stock_id = models.AutoField(primary_key=True)
    stock_ticker = models.CharField(max_length=8, default="")
    stock_name = models.CharField(max_length=200)
    stock_sector = models.CharField(max_length=200, default="Other")
    stock_risk = models.ManyToManyField(Risk)
    stock_price = models.ManyToManyField(Price)

    def __str__(self):
        return '{} {}'.format(self.stock_id, self.stock_ticker)


class StockPortfolio(models.Model):
    """

    """
    stock = models.ForeignKey(Stock)
    quantity = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.stock.stock_ticker)


class Portfolio(models.Model):
    """

    """
    portfolio_id = models.AutoField(primary_key=True)
    portfolio_name = models.CharField(max_length=50, null=True, blank=True)
    portfolio_user = models.ForeignKey(User)
    portfolio_risk = models.ManyToManyField(Risk)
    portfolio_stocks = models.ManyToManyField(StockPortfolio)

    def __str__(self):
        return self.portfolio_name if self.portfolio_name else "Unnamed"


class UserSettings(models.Model):
    """

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_portfolio = models.ForeignKey(
        Portfolio, on_delete=models.SET_NULL, null=True)


class PortfolioRank(models.Model):
    """

    """
    class Meta:
        unique_together = (("date", "portfolio"), )

    date = models.DateTimeField(auto_now=True, db_index=True)
    portfolio = models.ForeignKey(Portfolio)
    value = models.IntegerField()
