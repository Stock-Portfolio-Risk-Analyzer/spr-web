import unittest
from datetime import datetime as dt
from stockportfolio.api.datautils.rri import *
from mock import Mock
import math

"""
Test methods in rri.py
Author: Shivam Gupta (sgupta40@illinois.edu)
        Rohan Kapoor (rkapoor6@illinois.edu)
"""


class TestRRI(unittest.TestCase):

    def test_compute_portfolio_rri_for_range1(self):
        """ Tests the compute_portfolio_rri_for_range function """
        apple = Mock()
        apple.stock_ticker = 'AAPL'
        apple.stock_quantity = 10
        netflix = Mock()
        netflix.stock_ticker = 'NFLX'
        netflix.stock_quantity = 10
        fb = Mock()
        fb.stock_ticker = 'FB'
        fb.stock_quantity = 10
        stocks = [apple, netflix, fb]
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        rri = compute_portfolio_rri_for_range(stocks, start_date, end_date)
        self.assertAlmostEqual(rri, 1.4811878169633279, places=3)

    def test_compute_portfolio_rri_for_range2(self):
        """ Tests the compute_portfolio_rri_for_range function when quantity is zero"""
        apple = Mock()
        apple.stock_ticker = 'AAPL'
        apple.stock_quantity = 0
        netflix = Mock()
        netflix.stock_ticker = 'NFLX'
        netflix.stock_quantity = 0
        fb = Mock()
        fb.stock_ticker = 'FB'
        fb.stock_quantity = 0
        stocks = [apple, netflix, fb]
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        rri = compute_portfolio_rri_for_range(stocks, start_date, end_date)
        self.assertTrue(math.isnan(rri))

    def test_compute_stock_rri_for_range1(self):
        """ Tests the compute_stock_rri_for_range function """
        symbol = "AAPL"
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        rri = compute_stock_rri_for_range(symbol, start_date, end_date)
        self.assertAlmostEqual(rri, 1.73629103182, places=3)

    def test_compute_stock_rri_for_range2(self):
        """ Tests the compute_stock_rri_for_range function """
        symbol = "GDDY"
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        rri = compute_stock_rri_for_range(symbol, start_date, end_date)
        self.assertAlmostEqual(rri, 2.2967252609958937, places=3)

    # @TODO: SHIVAM FIX PLEASE
    # def test_compute_portfolio_rri_validity(self):
    #     """ Tests the compute_portfolio_rri_for_range function """
    #     apple = Mock()
    #     apple.stock_ticker = 'AAPL'
    #     apple.stock_quantity = 10
    #     netflix = Mock()
    #     netflix.stock_ticker = 'NFLX'
    #     netflix.stock_quantity = 10
    #     fb = Mock()
    #     fb.stock_ticker = 'FB'
    #     fb.stock_quantity = 10
    #     stocks = [apple, netflix, fb]
    #     start_date = "03/03/2016"
    #     end_date = "03/13/2016"
    #     p_rri = compute_portfolio_rri_for_range(stocks, start_date, end_date)
    #     s_rri = compute_stock_rri_for_range(apple.stock_ticker, start_date, end_date)
    #     self.assertEqual(p_rri, s_rri)
