import os
import random

import pandas
from django.test import TestCase

from stockportfolio.api import rec_utils
from stockportfolio.api.models import Portfolio, Stock, User, UserSettings
from stockportfolio.settings.base import BASE_DIR


class RecUtilsTestCase(TestCase):
    """Tests the rec_utils modules"""

    @classmethod
    def setUpClass(cls):
        """
        Set up the class for test with username, email and password

        :param cls: Class method variable
        """
        super(RecUtilsTestCase, cls).setUpClass()
        cls.user = User.objects.create_user(
            username='test', email='test@test.com', password='testing123')
        cls.portfolio = Portfolio.objects.create(portfolio_user=cls.user)
        cls.portfolio.save()
        cls._load_stocks()

    def setUp(self):
        """
        Setting up method

        :param self: Instance method variable
        """
        self.cls = RecUtilsTestCase

    @classmethod
    def tearDownClass(cls):
        """
        Tears down test class

        :param cls: Class method variable
        """
        super(RecUtilsTestCase, cls).tearDownClass()

    def test_stock_slice(self):
        """
        Tests the function to check if the stock_slice function works
        Stock slice gets random subset of stocks
        Checks if stock_slice returns some subset of stocks.

        :param self: Instance method variable
        """
        num_stocks = 10
        nslice = rec_utils.stock_slice(None, num_stocks)
        self.assertEqual(nslice, None)
        sslice = rec_utils.stock_slice(Stock.objects.all(), num_stocks)
        self.assertEqual(len(sslice), num_stocks)

    def test_get_portfolio_and_risk(self):
        """
        Tests to check if portfolio and risk are valid

        :param self: Instance method variable
        """
        user = self.cls.user
        usettings = UserSettings.objects.get_or_create(user=user)[0]
        p, r, u = rec_utils.get_portfolio_and_risk(user, usettings)
        self.assertIsNotNone(p)

    def test_get_recommendations(self):
        """
        Tests to check if the stock recommmendations are returned as
        expected

        :param self: Instance method variable
        """
        c = rec_utils._recommender_low_risk
        s = Stock.objects.all()
        recs = rec_utils.get_recommendations(c, s, 5, 0)
        self.assertTrue(len(recs) > 0)

    def test_fetch_tickers(self):
        """
        Tests to check if fetch_tickers is returning the tickers
        requested by the user

        :param self: Instance method variable
        """
        tickers = rec_utils.fetch_tickers(None)
        self.assertEqual(tickers, None)
        symbols = ['AAPL', 'GOOG', 'MSFT']
        user = User.objects.create_user(
            username='ticker', email='ticker@test.com', password='testing123')
        portfolio = Portfolio.objects.create(portfolio_user=user)
        for sym in symbols:
            rec_utils._add_stock(sym, 1, portfolio)
        tickers = rec_utils.fetch_tickers(portfolio)
        self.assertEqual(set(tickers), set(symbols))

    def test_determine_stock_quantities(self):
        """
        Tests to check if the stock_quantities being returned are
        the same as the one in the portfolio

        :param self: Instance method variable
        """
        curr = self.cls.portfolio
        f, v, l, h = rec_utils.determine_stock_quantities(curr, [])
        self.assertEqual(f, [])
        self.assertEqual(v, 0)
        self.assertEqual(l, 0)
        self.assertEqual(h, 0)
        symbols = ['AAPL', 'GOOG', 'MSFT']
        new = []
        for sym in symbols:
            stock = rec_utils._add_stock(sym, 1, curr)
            new.append(stock)
        f, v, l, h = rec_utils.determine_stock_quantities(curr, new)
        self.assertTrue(v >= 0)

    def test_stock_to_dict(self):
        """
        Tests to check if the stock data is the same as the stock_dictionary
        data

        :param self: Instance method variable
        """
        stock = rec_utils._add_stock('FB', 80, self.cls.portfolio)
        sdict = rec_utils.stock_to_dict(stock)
        self.assertEqual(sdict['ticker'], 'FB')
        self.assertEqual(sdict['name'], 'Facebook, Inc.')
        self.assertEqual(sdict['sector'], 'Technology')
        self.assertTrue(sdict['blurb'] != '')

    def test_fetch_target_value(self):
        """
        Tests to check if fetch_target values is within the targets set by
        the user

        :param self: Instance method variable
        """
        portfolio = None
        l, h = rec_utils._fetch_target_value(portfolio)
        self.assertTrue(l >= 10000 and l <= 20000)
        self.assertTrue(h >= 20000 and h <= 50000)

    def test_calculate_portfolio_value(self):
        """
        Tests to check if the portfolio value is as expected by the totalled
        value of stocks by their respective quantities

        :param self: Instance method variable
        """
        p = [('AAPL', 10, 130.4), ('TTPH', 2, 10),
             ('FC', 2, 1.2),      ('WU', 126, 4.6),
             ('TSLA', 19, 172.5), ('GOOG', 2, 666.42)]
        value = rec_utils._calculate_portfolio_value(p)
        self.assertEqual(value, 6516.34)

    def test_get_latest_stock_price(self):
        """
        Tests to check that when the function is called on an empty stock,
        it returns 0 as the stock_price

        :param self: Instance method variable
        """
        stock = None
        price = rec_utils._get_latest_stock_price(stock)
        self.assertEqual(price, 0)

    def test_get_latest_stock_risk(self):
        """
        Tests to check that when the function is called on an empty stock,
        it returns the beta as None

        :param self: Instance method variable
        """
        stock = None
        beta = rec_utils._get_latest_stock_risk(stock)
        self.assertEqual(beta, None)

    def test_get_latest_portfolio_risk(self):
        """
        Tests to check that when the function is called on an empty portfolio,
        it returns None as the portfolio risk

        :param self: Instance method variable
        """
        portfolio = None
        p_risk = rec_utils._get_latest_portfolio_risk(portfolio)
        self.assertEqual(p_risk, None)

    def test_get_all_sectors(self):
        """
        Tests to check that when the function is called on an empty portfolio,
        it returns an empty list as the sectors
        but when called on an actual portfolio,
        it returns a non-empty list

        :param self: Instance method variable
        """
        portfolio = None
        sectors = rec_utils._get_all_sectors(portfolio)
        self.assertEqual(sectors, [])
        sectors = rec_utils._get_all_sectors(self.cls.portfolio)
        self.assertNotEqual(sectors, [])

    @classmethod
    def _load_stocks(cls):
        """
        Checks to see if the stocks are being loaded correctly from the
        portfolio

        :param cls: Class method variable
        """
        fpath = os.path.join(
            BASE_DIR, 'api', 'datautils', 'secwiki_tickers.csv')
        df = pandas.read_csv(fpath)
        all_symbols = df['Ticker']
        symbols = []
        upper = len(all_symbols) - 1
        while len(symbols) < 200:
            symbol = all_symbols[random.randint(0, upper)]
            if symbol not in symbols:
                symbols.append(symbol)
                rec_utils._add_stock(symbol, 1, cls.portfolio)
