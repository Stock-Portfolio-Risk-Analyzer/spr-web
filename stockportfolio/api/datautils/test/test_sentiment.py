import unittest
from datetime import datetime as dt
import stockportfolio.api.datautils.sentiment as stm


class TestSentiment(unittest.TestCase):

    def test_get_stock_sentiment(self):
        """
        Tests if fetching sentiments for single stock works
        """

        rticker = 'AAPL'
        rstm = stm.get_stock_sentiment(rticker)
        self.assertEqual(rstm, -1)
        fticker = 'Z134'
        fstm = stm.get_stock_sentiment(fticker)
        self.assertTrue(fstm == -1 or fstm == 1)

    def test_get_sentiment_of_a_portfolio(self):
        """
        Tests if fetching sentiments for portfolio works
        """

        p = ['AAPL', 'GOOG', 'MSFT', 'FAST', 'DYII']
        pstm = stm.get_sentiment_of_a_portfolio(p)
        self.assertTrue(pstm != 0)

    def test_get_stock_sentiment_for_a_range(self):
        """
        Tests if fetching sentiments for a interval of time works
        """

        symbol = 'AAPL'
        start_date = dt(year=2016, month=1, day=1)
        end_date = dt(year=2016, month=1, day=31)
        rstm = stm.get_stock_sentiment_for_a_range(
            symbol, start_date, end_date)
        end_stm = rstm[-1]
        self.assertTrue(len(rstm) != 0)
        self.assertAlmostEqual(end_stm, 0.029)

    def test_get_average_stock_sentiment_for_a_range(self):
        """
        Tests if fetching average sentiment for single stock works 
        """

        symbol = 'AAPL'
        start_date = dt(year=2016, month=1, day=1)
        end_date = dt(year=2016, month=1, day=31)
        astm = stm.get_average_stock_sentiment_for_a_range(
            symbol, start_date, end_date)
        self.assertAlmostEqual(astm, 0.0751612903226)

    def test_get_market_sentiment(self):
        """
        Tests if fetching market sentiment works
        """

        mstm = stm.get_market_sentiment()
        self.assertTrue(-1 <= mstm <= 1)