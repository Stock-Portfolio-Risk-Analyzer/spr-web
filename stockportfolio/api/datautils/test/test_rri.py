import unittest
from datetime import datetime as dt
from stockportfolio.api.datautils.rri import *

"""
Test methods in rri.py
Author: Shivam Gupta (sgupta40@illinois.edu)
        Rohan Kapoor (rkapoor6@illinois.edu)
"""


class TestRRI(unittest.TestCase):

    def test_compute_portfolio_rri_for_range1(self):
        """ Tests the compute_portfolio_rri_for_range function """
        stock_list = ["AAPL", "NFLX", "FB"]
        quantity_list = [10, 10, 10]
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        rri = compute_portfolio_rri_for_range(stock_list, quantity_list, start_date, end_date)
        self.assertEqual(rri, 1.48118245233)

    def test_compute_portfolio_rri_for_range2(self):
        """ Tests the compute_portfolio_rri_for_range function when quantity is zero"""
        stock_list = ["AAPL", "NFLX", "FB"]
        quantity_list = [0, 0, 0]
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        rri = compute_portfolio_rri_for_range(stock_list, quantity_list, start_date, end_date)
        self.assertEqual(rri, nan) #TODO: <type 'numpy.float64'> mai nan kaise likhe?

    def test_compute_stock_rri_for_range1(self):
        """ Tests the compute_stock_rri_for_range function """
        symbol = "AAPL"
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        rri = compute_stock_rri_for_range(symbol, start_date, end_date)
        self.assertEqual(rri, 1.73629103182)

    def test_compute_stock_rri_for_range2(self):
        """ Tests the compute_stock_rri_for_range function """
        symbol = "GDDY"
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        rri = compute_stock_rri_for_range(symbol, start_date, end_date)
        self.assertEqual(rri, 1.73629103182)

    def test_compute_portfolio_rri_validity(self):
        """ Tests the compute_portfolio_rri_for_range function """
        stock_list = ["AAPL", "NFLX", "FB"]
        quantity_list = [10, 0, 0]
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        p_rri = compute_portfolio_rri_for_range(stock_list, quantity_list, start_date, end_date)
        s_rri = compute_stock_rri_for_range(symbol, start_date, end_date)
        self.assertEqual(p_rri, s_rri)
