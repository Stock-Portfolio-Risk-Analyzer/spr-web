from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


"""Database models for the application""" 

class Risk(models.Model):
    """
    Inherited from the Frameworks Model Class. Holds Risk information
    for a specific portfolio or stock.
    Includes:
        risk_id: AutoField - DB ID for Object
        risk_value: FloatField - Risk value for Stock.
        risk_date: DateTimeField - Date, often set to calculation date.

    """
    risk_id = models.AutoField(primary_key=True)
    risk_value = models.FloatField(default=0.0)
    risk_date = models.DateTimeField()

    def __str__(self):
        """
        Creates a string representation for the model.

        :return: String Representation of Risk, '(Risk Value) @ (Date)'
        """
        return '{} @ {}'.format(self.risk_value, self.risk_date)

    def save(self, *args, **kwargs):
        """
        Overwritten Save Function for Risk, makes sure we save
        the timezone.

        :param args: Arguments for Overwritten function
        :param kwargs: Keyword Arguments for Overwritten function
        :return: Saved Risk Object
        """
        if not self.risk_date:
            self.risk_date = timezone.now()
        super(Risk, self).save(*args, **kwargs)


class Price(models.Model):
    """
    Inherited from the Django's Frameworks Model Class.
    Holds Price information for a specific Stock.
    Includes:
        value: FloatField - Price of Stock
        date: DateTimeField - Date, often set to calculation date.

    """
    value = models.FloatField()
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        """
        Overwritten Save Function for Risk, makes sure we save
        the timezone.

        :param args: Arguments for Overwritten function
        :param kwargs: Keyword Arguments for Overwritten function
        :return: Saved Risk Object
        """
        if not self.date:
            self.date = timezone.now()
        super(Price, self).save(*args, **kwargs)


class Stock(models.Model):
    """
    Inherited from the Django's Frameworks Model Class.
    Holds Stock information for a specific Stock.
    Includes:
        stock_id: AutoField - DB ID for Object
        stock_ticker: CharField - Holds Stock Symbol
        stock_name: CharField - Holds Company Full Name
        stock_sector: CharField - Holds Sector Stock Belongs To (default=Other)
        stock_risk: ManyToManyField(Risk) - List of Risk Objects
        generated for stock.
        stock_price: ManyToManyField(Price) - List of Prices calculated
        for stock.

    """
    stock_id = models.AutoField(primary_key=True)
    stock_ticker = models.CharField(max_length=8, default="")
    stock_name = models.CharField(max_length=200)
    stock_sector = models.CharField(max_length=200, default="Other")
    stock_risk = models.ManyToManyField(Risk)
    stock_price = models.ManyToManyField(Price)

    def __str__(self):
        """
        Creates a string representation for the model.

        :return: String Representation of Risk,
        '(Stock ID in DB) @ (Stock Ticker)'
        """
        return '{} {}'.format(self.stock_id, self.stock_ticker)

    def __iter__(self):
        """
        Overwritten Iterator for Stock Objects, which iterates on three values
        stock_ticker, stock_name, stock_sector.

        :return: iter object
        """
        return iter([self.stock_ticker, self.stock_name, self.stock_sector])


class StockPortfolio(models.Model):
    """
    Inherited from the Django's Frameworks Model Class.
    Holds Tuple of Stock and Quantity, which is what a User's portfolio
    uses to connect a stock to a quantity for a user.
    Includes:
        stock: ForeignKey - Foreign Key to DB Stock Object
        quantity: CharField - Holds Stock Symbol
        stock_name: IntegerField - Holds Quantity of Stock

    """
    stock = models.ForeignKey(Stock)
    quantity = models.IntegerField()

    def __str__(self):
        """
        Creates a string representation for the model.

        :return: String Representation of StockPortfolio, '(Stock Ticker)'
        """
        return '{}'.format(self.stock.stock_ticker)


class Portfolio(models.Model):
    """
    Inherited from the Django's Frameworks Model Class.
    Holds a User's Portfolio Information.
    Includes:
        portfolio_id: AutoField - DB ID for Object
        portfolio_name: CharField - Holds Name for Portfolio (can be
         blank/null)
        portfolio_user: ForeignKey - Holds the User this portfolio belongs to.
        portfolio_risk: ManyToManyField(Risk) - Holds all the Risk Objects
         computed for a portfolio.
        portfolio_stocks: ManyToManyField(StockPortfolio) - List of Stocks on
         Portfolio

    """
    portfolio_id = models.AutoField(primary_key=True)
    portfolio_name = models.CharField(max_length=50, null=True, blank=True)
    portfolio_user = models.ForeignKey(User)
    portfolio_risk = models.ManyToManyField(Risk)
    portfolio_stocks = models.ManyToManyField(StockPortfolio)

    def __str__(self):
        """
            Creates a string representation for the model.

            :return: String Representation of Portfolo, '(Stock Name)'
            """
        return self.portfolio_name if self.portfolio_name else "Unnamed"


class UserSettings(models.Model):
    """
    Inherited from the Django's Frameworks Model Class.
    Holds a User's Settings
    Includes:
        user: ForeignKey(User) - Holds User for this UserSettings
        default_portfolio: ForeignKey(Porfolio) - Holds Default/Primary
         Portfolio for User.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_portfolio = models.ForeignKey(
        Portfolio, on_delete=models.SET_NULL, null=True)


class PortfolioRank(models.Model):
    """
    Inherited from the Django's Frameworks Model Class.
    Holds the rank for portfolio.
    Includes:
        date: DateTimeField - Automatically Timestamped when created.
        portfolio: ForeignKey(Porfolio) - Holds the Portfolio the Rank
         belongs to.
        value: IntegerField - Holds the Rank Value for Portfolio.

    """
    class Meta:
        unique_together = (("date", "portfolio"), )

    date = models.DateTimeField(auto_now=True, db_index=True)
    portfolio = models.ForeignKey(Portfolio)
    value = models.IntegerField()


class PortfolioValue(models.Model):
    """
    Inherited from the Django's Frameworks Model Class.
    Holds the total value for portfolio.
    Includes:
        date: DateTimeField - Automatically Timestamped when created.
        portfolio: ForeignKey(Porfolio) - Holds the Portfolio the
         Value belongs to.
        value: FloatField - Holds the total value of the portfolio

    """

    class Meta:
        unique_together = (("date", "portfolio"), )

    date = models.DateTimeField(auto_now=True, db_index=True)
    portfolio = models.ForeignKey(Portfolio)
    value = models.FloatField()
