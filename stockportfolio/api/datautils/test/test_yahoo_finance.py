import unittest
from stockportfolio.api.datautils.yahoo_finance import *

class TestYahooFinance(unittest.TestCase):

    def test_get_current_price(self):
        symbol = 'GOOG'
        current_price = get_current_price(symbol)
        self.assertTrue(type(current_price) is float)
        self.assertGreaterEqual(current_price, 400)

if __name__ == "__main__":
    unittest.main()
