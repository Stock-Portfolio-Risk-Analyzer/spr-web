import unittest
from datetime import datetime as dt

from stockportfolio.api.datautils.yahoo_finance import (get_company_name,
                                                        get_company_sector,
                                                        get_current_price,
                                                        get_pct_returns,
                                                        get_returns,
                                                        get_stock_data)


class TestYahooFinance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.symbol = 'GOOG'
        cls.symbol2 = 'AAPL'
        cls.start_date = dt(year=2016, month=1, day=1)
        cls.end_date = dt(year=2016, month=2, day=1)
        cls.test_date = dt(year=2016, month=2, day=1)

    def test_get_stock_data(self):
        data = get_stock_data(self.symbol, self.start_date, self.end_date)
        self.assertTrue(data.keys().__contains__('Open'))
        self.assertTrue(data.keys().__contains__('High'))
        self.assertTrue(data.keys().__contains__('Low'))
        self.assertTrue(data.keys().__contains__('Close'))
        self.assertTrue(data.keys().__contains__('Volume'))

        data_no_start_or_end = get_stock_data(self.symbol)
        self.assertTrue(data_no_start_or_end.keys().__contains__('Open'))
        self.assertTrue(data_no_start_or_end.keys().__contains__('High'))
        self.assertTrue(data_no_start_or_end.keys().__contains__('Low'))
        self.assertTrue(data_no_start_or_end.keys().__contains__('Close'))
        self.assertTrue(data_no_start_or_end.keys().__contains__('Volume'))

    def test_get_stock_data_multiple(self):
        data = get_stock_data(
            [self.symbol, 'AAPL'], self.start_date, self.end_date)
        self.assertTrue(data.keys().__contains__('Open'))
        self.assertTrue(data.keys().__contains__('High'))
        self.assertTrue(data.keys().__contains__('Low'))
        self.assertTrue(data.keys().__contains__('Close'))
        self.assertTrue(data.keys().__contains__('Volume'))

    def test_get_pct_returns(self):
        pct_returns = get_pct_returns(
            self.symbol, self.start_date, self.end_date)
        self.assertAlmostEqual(pct_returns[self.test_date], .0121811533129)

    def test_get_returns(self):
        returns = get_returns(self.symbol, self.start_date, self.end_date)
        self.assertAlmostEqual(returns[self.test_date], 9.049988)

    def test_get_current_price(self):
        current_price = get_current_price(self.symbol)
        self.assertTrue(type(current_price) is float)
        self.assertGreaterEqual(current_price, 500)

    def test_get_company_name(self):
        company_name = get_company_name(self.symbol)
        self.assertEqual(company_name, 'Google Inc.')

    def test_get_company_sector(self):
        company_sector = get_company_sector(self.symbol)
        self.assertEqual(company_sector, 'Technology')
