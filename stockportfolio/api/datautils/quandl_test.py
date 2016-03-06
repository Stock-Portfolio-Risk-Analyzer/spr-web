import unittest
from datetime import datetime as dt
from quandl_info import *

class TestQuandl(unittest.TestCase):

    def test_get_stock_data(self):
        start = dt(year=2015, month=1, day=5)
        end   = dt(year=2015, month=1, day=6)
        data = get_stock_data("GOOG", start, end)
        self.assertEqual(data['Close'][0], 513.87) 
    
    def test_get_stock_data_multiple(self):
        start = dt(year=2015, month=1, day=5)
        end   = dt(year=2015, month=1, day=6)
        data = get_stock_data_multiple(["GOOG","AAPL"],  start, end)
        self.assertEqual(data['GOOG']['Close'][0], 513.87)
        self.assertEqual(data['AAPL']['Close'][0], 106.25)
 
    def test_get_pct_returns(self):
        start = dt(year=2015, month=1, day=5)
        end   = dt(year=2015, month=1, day=6)
        close_pct = -0.0231770681301      
        qclose_pct = get_pct_returns("GOOG", start, end)[1]
        self.assertTrue(abs(qclose_pct - close_pct) < 0.001)        

    def test_get_returns(self):
        start = dt(year=2015, month=1, day=5)
        end   = dt(year=2015, month=1, day=6)
        close = -11.910000000000025 
        self.assertEqual(get_returns("GOOG", start, end)[1], close)         
    
    def test_get_options_data(self):
        expected_options = ['Open', 'High', 'Low', 'Close', 'Volume', 
                            'Ex-Dividend', 'Split Ratio', 'Adj. Open', 
                            'Adj. High', 'Adj. Low', 'Adj. Close', 
                            'Adj. Volume']
        options = get_options_data_quandl("GOOG")
        self.assertTrue(all(map(lambda x: x in options, expected_options)))

