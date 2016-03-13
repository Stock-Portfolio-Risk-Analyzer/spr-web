import unittest
from stockportfolio.api.datautils.yahoo_finance import *


class TestYahooFinance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.symbol = 'GOOG'

    def test_get_stock_data(self):
        start_date = dt(year=2016, month=1, day=1)
        end_date = dt(year=2016, month=2, day=1)
        data = get_stock_data(self.symbol, start_date, end_date)
        self.assertTrue(data.keys().__contains__('Open'))
        self.assertTrue(data.keys().__contains__('High'))
        self.assertTrue(data.keys().__contains__('Low'))
        self.assertTrue(data.keys().__contains__('Close'))
        self.assertTrue(data.keys().__contains__('Volume'))

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
