import unittest
from datetime import datetime as dt

import stockportfolio.api.datautils.yahoo_finance as yf


class TestYahooFinance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        TODO

        :return:
        """
        cls.symbol = 'GOOG'
        cls.symbol2 = 'AAPL'
        cls.start_date = dt(year=2016, month=1, day=1)
        cls.end_date = dt(year=2016, month=2, day=1)
        cls.test_date = dt(year=2016, month=2, day=1)

    def test_get_stock_data(self):
        """
        TODO

        :return:
        """
        data = yf.get_stock_data(self.symbol, self.start_date, self.end_date)
        self.assertTrue(data.keys().__contains__('Open'))
        self.assertTrue(data.keys().__contains__('High'))
        self.assertTrue(data.keys().__contains__('Low'))
        self.assertTrue(data.keys().__contains__('Close'))
        self.assertTrue(data.keys().__contains__('Volume'))

        data_no_start_or_end = yf.get_stock_data(self.symbol)
        self.assertTrue(data_no_start_or_end.keys().__contains__('Open'))
        self.assertTrue(data_no_start_or_end.keys().__contains__('High'))
        self.assertTrue(data_no_start_or_end.keys().__contains__('Low'))
        self.assertTrue(data_no_start_or_end.keys().__contains__('Close'))
        self.assertTrue(data_no_start_or_end.keys().__contains__('Volume'))

    def test_get_stock_data_multiple(self):
        """
        TODO

        :return:
        """
        data = yf.get_stock_data_multiple(
            [self.symbol, 'AAPL'], self.start_date, self.end_date)
        self.assertTrue(data['AAPL'].keys().__contains__('Open'))
        self.assertTrue(data['AAPL'].keys().__contains__('High'))
        self.assertTrue(data['AAPL'].keys().__contains__('Low'))
        self.assertTrue(data['AAPL'].keys().__contains__('Close'))
        self.assertTrue(data['AAPL'].keys().__contains__('Volume'))

    def test_get_pct_returns(self):
        """
        TODO

        :return:
        """
        pct_returns = yf.get_pct_returns(
            self.symbol, self.start_date, self.end_date)
        self.assertAlmostEqual(pct_returns[self.test_date], .0121811533129)

    def test_get_returns(self):
        """
        TODO

        :return:
        """
        returns = yf.get_returns(self.symbol, self.start_date, self.end_date)
        self.assertAlmostEqual(returns[self.test_date], 9.049988)

    def test_get_current_price(self):
        """
        TODO

        :return:
        """
        returns = yf.get_returns(self.symbol, self.start_date, self.end_date)
        self.assertAlmostEqual(returns[self.test_date], 9.049988)

    def test_get_current_price(self):
        current_price = yf.get_current_price(self.symbol)
        self.assertTrue(type(current_price) is float)
        self.assertGreaterEqual(current_price, 500)

    def test_get_company_name(self):
        """
        TODO

        :return:
        """
        company_name = yf.get_company_name(self.symbol)
        self.assertEqual(company_name, 'Google Inc.')

    def test_get_company_sector(self):
        company_sector = yf.get_company_sector(self.symbol)
        self.assertEqual(company_sector, 'Technology')