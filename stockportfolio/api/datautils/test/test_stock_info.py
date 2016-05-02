import unittest
from datetime import datetime as dt

import stockportfolio.api.datautils.stock_info as stock_info


class TestStockInfo(unittest.TestCase):
    """
    Creates test fixture specifying time ranges
    """
    def setUp(self):
        self.start_date = dt(year=2016, month=1, day=1)
        self.end_date = dt(year=2016, month=1, day=31)
    """
    Tests if getting company name works
    """
    def test_get_company_name(self):
        symbol = 'AAPL'
        name = stock_info.get_company_name(symbol)
        self.assertEqual(name, 'Apple Inc.')
    """
    Tests if fetching sentiments for single stock works
    """
    def test_get_company_sector(self):
        symbol = 'AAPL'
        sector = stock_info.get_company_sector(symbol)
        self.assertEqual(sector, 'Consumer Goods')
    """
    Tests if rri for a week is caluclated correctly
    """
    def test_get_company_rri_for_a_week(self):
        symbol = 'MSFT'
        rlist = stock_info.get_company_rri_for_a_week(symbol)
        self.assertEqual(len(rlist), 7)
        self.assertIsNotNone(rlist[-1])
    """
    Tests if rri for a month is caluclated correctly
    """
    def test_get_company_rri_for_a_month(self):
        symbol = 'MSFT'
        rlist = stock_info.get_company_rri_for_a_month(symbol)
        self.assertEqual(len(rlist), 30)
        self.assertIsNotNone(rlist[-1])
    """
    Tests the volume of that stock moved in the market for last week 
    """
    def test_get_stock_volume_traded_for_a_week(self):
        symbol = 'FB'
        vlist = stock_info.get_stock_volume_traded_for_a_week(symbol)
        self.assertIsNotNone(vlist)
        self.assertEqual(len(vlist), 5)  # business days
        final_volume = vlist[-1]
        self.assertTrue(final_volume > 0)
    """
    Tests the volume of that stock moved in the market for last month
    """
    def test_get_stock_volume_traded_for_a_month(self):
        symbol = 'GOOG'
        vlist = stock_info.get_stock_volume_traded_for_a_month(symbol)
        self.assertIsNotNone(vlist)
        self.assertEqual(len(vlist), 20)  # business days
        final_volume = vlist[-1]
        self.assertTrue(final_volume > 0)