import unittest
from datetime import datetime as dt
from stockportfolio.api.datautils.rri import *
from stockportfolio.api.datautils.stock_info import *
from mock import Mock
import math

"""
Test methods in rri.py
Author: Shivam Gupta (sgupta40@illinois.edu)
        Laurynas Tamulevičius
"""


class TestStockInfo(unittest.TestCase):

    def test_get_company_industry(self):
        """ Tests the get_company_industry function """
        apple = Mock()
        apple.stock_ticker = 'AAPL'
        industry = get_company_industry(apple.stock_ticker)
        self.assertAlmostEqual(industry, "Electronic Equipment")

    def test_get_company_rri_for_today(self):
        """ Tests the get_company_rri_for_today function """
        netflix = Mock()
        netflix.stock_ticker = 'NFLX'
        netflix.stock_quantity = 0
        number_of_days_back = 4
        pre_rri  = compute_stock_rri_for_today(netflix.stock_ticker, number_of_days_back)
        this_rri = get_company_rri_for_today(netflix.stock_ticker, number_of_days_back)
        self.assertAlmostEqual(pre_rri, this_rri, places=3)

    def test_compute_stock_rri_for_range(self):
        """ Tests the compute_stock_rri_for_range function """
        symbol = "AAPL"
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        rri = compute_stock_rri_for_range(symbol, start_date, end_date)
        self.assertAlmostEqual(rri, 1.73629103182, places=3)

    def test_get_company_name(self):
        """ Tests the get_company_name function """
        fb = Mock()
        fb.stock_ticker = 'FB'
        industry = get_company_name(fb.stock_ticker)
        self.assertTrue(industry == "Facebook, Inc.")
        
    def test_get_company_sector(self):
        """ Tests the get_company_sector function """
        google = Mock()
        google.stock_ticker = 'GOOG'
        industry = get_company_sector(google.stock_ticker)
        self.assertTrue(industry == "Technology")
