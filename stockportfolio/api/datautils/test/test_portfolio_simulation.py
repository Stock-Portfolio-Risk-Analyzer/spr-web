import unittest
import pandas as pd
import datetime as dt
import stockportfolio.api.datautils.yahoo_finance as yf
import stockportfolio.api.datautils.portfolio_simulation as ps

class TestPortfolioSimulation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.start_date = dt.datetime(year=2008, month=1, day=1)
        cls.end_date = dt.datetime(year=2016, month=4, day=20)
        cls.dates = pd.date_range(cls.start_date, cls.end_date)

        cls.portfolio = {
            'AAPL': 5,
            'MSFT': 10,
            'ORCL': 15
        }

        cls.price_field = 'Adj Close'
        cls.test_symbol = 'IBM'
        cls.test_qty = 100

    def test_get_portfolio_returns_series(self):
        portfolio_returns_series = ps.get_portfolio_returns_series(self.portfolio,
                                                                   start_date=self.start_date,
                                                                   end_date=self.end_date,
                                                                   price_field=self.price_field)

        for day in self.dates:
            try:
                total_portfolio_value_prev_day = 0
                total_portfolio_value_curr_day = 0
                for symbol, quantity in self.portfolio.items():
                    prev_day = day.to_datetime()-dt.timedelta(days=1)
                    prev_price = yf.get_stock_data(symbol, prev_day, prev_day)[self.price_field][prev_day]
                    prev_position_value = prev_price*quantity
                    total_portfolio_value_prev_day += prev_position_value

                    curr_price = yf.get_stock_data(symbol, day, day)[self.price_field][day]
                    curr_position_value = curr_price*quantity
                    total_portfolio_value_curr_day += curr_position_value

                change = total_portfolio_value_curr_day-total_portfolio_value_prev_day
                pct_change = change/total_portfolio_value_prev_day
                self.assertEqual(pct_change, portfolio_returns_series[day])

            except Exception as e:
                # no data for this day (i.e. not a trading day)
                pass

    def test_get_portfolio_value_series(self):
        portfolio_value_series = ps.get_portfolio_value_series(self.portfolio,
                                                               start_date=self.start_date,
                                                               end_date=self.end_date,
                                                               price_field=self.price_field)

        for day in self.dates:
            try:
                total_portfolio_value = 0
                for symbol, quantity in self.portfolio.items():
                    price = yf.get_stock_data(symbol, day.to_datetime(), day.to_datetime())
                    price = price[self.price_field][day]
                    position_value = price*quantity
                    total_portfolio_value += position_value
                print portfolio_value_series[day], total_portfolio_value
                self.assertEqual(portfolio_value_series[day], total_portfolio_value)
            except Exception as e:
                # no data for this day (i.e. not a trading day)
                pass

    def test_get_position_value_series(self):
        position_value_series = ps.get_position_value_series(self.test_symbol, self.test_qty,
                                                             start_date=self.start_date,
                                                             end_date=self.end_date,
                                                             price_field=self.price_field)
        for day in self.dates:
            try:
                price = yf.get_stock_data(self.test_symbol, day.to_datetime(), day.to_datetime())
                price = price[self.price_field][day]
                position_value = price*self.test_qty
                self.assertEqual(position_value_series[day], position_value)
            except Exception as e:
                # no data for this day (i.e. not a trading day)
                pass



    def test_simulate_returns(self):
        returns = ps.get_portfolio_returns_series(self.portfolio)

    def calculate_alpha_beta(self):
        pass