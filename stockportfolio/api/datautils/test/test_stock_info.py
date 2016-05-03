import unittest
from datetime import datetime as dt

import stockportfolio.api.datautils.stock_info as stock_info

"""Tests the stock_info module"""

class TestStockInfo(unittest.TestCase):
    """Tests the stock_info module"""

    def setUp(self):
        """
        Creates test fixture specifying time ranges
        """

        self.start_date = dt(year=2016, month=1, day=1)
        self.end_date = dt(year=2016, month=1, day=31)

    def test_get_company_name(self):
        """
        Tests if getting company name works
        """

        symbol = 'AAPL'
        name = stock_info.get_company_name(symbol)
        self.assertEqual(name, 'Apple Inc.')

    def test_get_company_sector(self):
        """
        Tests if fetching sentiments for single stock works
        """

        symbol = 'AAPL'
        sector = stock_info.get_company_sector(symbol)
        self.assertEqual(sector, 'Consumer Goods')

    def test_get_company_rri_for_a_week(self):
        """
        Tests if rri for a week is caluclated correctly
        """

        symbol = 'MSFT'
        rlist = stock_info.get_company_rri_for_a_week(symbol)
        self.assertTrue(len(rlist) > 0)
        self.assertIsNotNone(rlist[-1])

    def test_get_company_rri_for_a_month(self):
        """
        Tests if rri for a month is caluclated correctly
        """

        symbol = 'MSFT'
        rlist = stock_info.get_company_rri_for_a_month(symbol)
        self.assertTrue(len(rlist) > 0)
        self.assertIsNotNone(rlist[-1])

    def test_get_stock_volume_traded_for_a_week(self):
        """
        Tests the volume of that stock moved in the market for last week
        """

        symbol = 'FB'
        vlist = stock_info.get_stock_volume_traded_for_a_week(symbol)
        self.assertIsNotNone(vlist)
        self.assertTrue(len(vlist) > 0)  # business days
        final_volume = vlist[-1]
        self.assertTrue(final_volume > 0)

    def test_get_stock_volume_traded_for_a_month(self):
        """
        Tests the volume of that stock moved in the market for last month
        """

        symbol = 'GOOG'
        vlist = stock_info.get_stock_volume_traded_for_a_month(symbol)
        self.assertIsNotNone(vlist)
        self.assertTrue(len(vlist) > 0)  # business days
        final_volume = vlist[-1]
        self.assertTrue(final_volume > 0)
