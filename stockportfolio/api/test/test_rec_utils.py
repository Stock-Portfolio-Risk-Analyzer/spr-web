import os
import random

import pandas
from django.test import TestCase

from stockportfolio.api import rec_utils
from stockportfolio.api.models import Portfolio, Stock, User, UserSettings
from stockportfolio.settings.base import BASE_DIR


class RecUtilsTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(RecUtilsTestCase, cls).setUpClass()
        cls.user = User.objects.create_user(
            username='test', email='test@test.com', password='testing123')
        cls.portfolio = Portfolio.objects.create(portfolio_user=cls.user)
        cls.portfolio.save()
        cls._load_stocks()

    def setUp(self):
        self.cls = RecUtilsTestCase

    @classmethod
    def tearDownClass(cls):
        super(RecUtilsTestCase, cls).tearDownClass()

    def test_stock_slice(self):
        num_stocks = 10
        nslice = rec_utils.stock_slice(None, num_stocks)
        self.assertEqual(nslice, None)
        sslice = rec_utils.stock_slice(Stock.objects.all(), num_stocks)
        self.assertEqual(len(sslice), num_stocks)

    def test_get_portfolio_and_risk(self):
        user = self.cls.user
        usettings = UserSettings.objects.get_or_create(user=user)[0]
        p, r, u = rec_utils.get_portfolio_and_risk(user, usettings)
        self.assertIsNotNone(p)

    def test_get_recommendations(self):
        c = rec_utils._recommender_low_risk
        s = Stock.objects.all()
        recs = rec_utils.get_recommendations(c, s, 5, 0)
        self.assertTrue(len(recs) > 0)

    def test_fetch_tickers(self):
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
        stock = rec_utils._add_stock('FB', 80, self.cls.portfolio)
        sdict = rec_utils.stock_to_dict(stock)
        self.assertEqual(sdict['ticker'], 'FB')
        self.assertEqual(sdict['name'], 'Facebook, Inc.')
        self.assertEqual(sdict['sector'], 'Technology')
        self.assertTrue(sdict['blurb'] != '')

    def test_fetch_target_value(self):
        portfolio = None
        l, h = rec_utils._fetch_target_value(portfolio)
        self.assertTrue(l >= 10000 and l <= 20000)
        self.assertTrue(h >= 20000 and h <= 50000)

    def test_calculate_portfolio_value(self):
        p = [('AAPL', 10, 130.4), ('TTPH', 2, 10),
             ('FC', 2, 1.2),      ('WU', 126, 4.6),
             ('TSLA', 19, 172.5), ('GOOG', 2, 666.42)]
        value = rec_utils._calculate_portfolio_value(p)
        self.assertEqual(value, 6516.34)

    def test_get_latest_stock_price(self):
        stock = None
        price = rec_utils._get_latest_stock_price(stock)
        self.assertEqual(price, 0)

    def test_get_latest_stock_risk(self):
        stock = None
        beta = rec_utils._get_latest_stock_risk(stock)
        self.assertEqual(beta, None)

    def test_get_latest_portfolio_risk(self):
        portfolio = None
        p_risk = rec_utils._get_latest_portfolio_risk(portfolio)
        self.assertEqual(p_risk, None)

    def test_get_all_sectors(self):
        portfolio = None
        sectors = rec_utils._get_all_sectors(portfolio)
        self.assertEqual(sectors, [])
        sectors = rec_utils._get_all_sectors(self.cls.portfolio)
        self.assertNotEqual(sectors, [])

    @classmethod
    def _load_stocks(cls):
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
