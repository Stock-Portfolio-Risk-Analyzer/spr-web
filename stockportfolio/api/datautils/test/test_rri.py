import math
import unittest

from mock import Mock

from stockportfolio.api.datautils.rri import (compute_portfolio_rri_for_range,
                                              compute_stock_rri_for_range)


class TestRRI(unittest.TestCase):
    """
    Tests if rri computation works and provides positive risk
    """
    def test_compute_portfolio_rri_for_range1(self):
        apple = Mock()
        apple.stock.stock_ticker = 'AAPL'
        apple.quantity = 10
        netflix = Mock()
        netflix.stock.stock_ticker = 'NFLX'
        netflix.quantity = 10
        fb = Mock()
        fb.stock.stock_ticker = 'FB'
        fb.quantity = 10
        stocks = [apple, netflix, fb]
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        rri = compute_portfolio_rri_for_range(stocks, start_date, end_date)
        self.assertTrue(rri > 0)
    """
    Tests the compute_portfolio_rri_for_range function
    when quantity is zero
    """
    def test_compute_portfolio_rri_for_range2(self):
        apple = Mock()
        apple.stock.stock_ticker = 'AAPL'
        apple.quantity = 0
        netflix = Mock()
        netflix.stock.stock_ticker = 'NFLX'
        netflix.quantity = 0
        fb = Mock()
        fb.stock.stock_ticker = 'FB'
        fb.quantity = 0
        stocks = [apple, netflix, fb]
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        rri = compute_portfolio_rri_for_range(stocks, start_date, end_date)
        self.assertTrue(math.isnan(rri))
    """
    Tests rri calculation for single stock
    """
    def test_compute_stock_rri_for_range1(self):
        symbol = "AAPL"
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        rri = compute_stock_rri_for_range(symbol, start_date, end_date)
        self.assertTrue(rri > 0)
    """
    Tests rri calculation for different stock
    """
    def test_compute_stock_rri_for_range2(self):
        symbol = "GDDY"
        start_date = "03/03/2016"
        end_date = "03/13/2016"
        rri = compute_stock_rri_for_range(symbol, start_date, end_date)
        self.assertTrue(rri > 0)
