import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from django.http import HttpResponse
from yahoo_finance import get_stock_data
from matplotlib.ticker import FuncFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas


def get_benchmark_returns(benchmark='SPY', start_date=None, end_date=None, price_field='Adj Close'):
    """
    Get the daily (non-cumulative) percent returns for the benchmark.
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :param benchmark: (str) default: SPY (S&P 500 index)
    :param price_field: (str) default: 'Adj Close'
    :return: (pd.Series)
    """
    if start_date is None:
        start_date = dt.datetime(year=2008, month=1, day=1)
    if end_date is None:
        end_date = dt.datetime.today()

    benchmark_price_series = get_stock_data(benchmark, start_date=start_date, end_date=end_date)[price_field]

    return benchmark_price_series.pct_change().dropna()


def get_portfolio_returns_series(portfolio, start_date=None, end_date=None, price_field='Adj Close'):
    """
    Simulates portfolio returns assuming the portfolio was bought on start_date and held through end_date
    :param portfolio:
    :param start_date:
    :param end_date:
    :param price_field:
    :return:
    """
    if start_date is None:
        start_date = dt.datetime(year=2008, month=1, day=1)
    if end_date is None:
        end_date = dt.datetime.today()

    portfolio_value_series = get_portfolio_value_series(portfolio,
                                                        start_date=start_date,
                                                        end_date=end_date,
                                                        price_field=price_field)

    portfolio_returns_series = portfolio_value_series.pct_change().dropna()
    return portfolio_returns_series


def get_portfolio_value_series(portfolio, start_date=None, end_date=None, price_field='Adj Close'):
    """
    Generate a time-series of the portfolio assuming the portfolio was bought on start_date and held through end_date.
    :param portfolio: (dict) symbol:quantity
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :param price_field: (str) default: 'Adj Close'
    :return:
    """
    if start_date is None:
        start_date = dt.datetime(year=2008, month=1, day=1)
    if end_date is None:
        end_date = dt.datetime.today()

    position_values = []
    date_range = pd.date_range(start_date, end_date)
    for symbol, quantity in portfolio.items():
        position_value_series = get_position_value_series(symbol, quantity, start_date, end_date, price_field)
        position_values.append(position_value_series)

    portfolio_value_series = pd.Series(data=0, index=date_range)
    for symbol_value_series in position_values:
        portfolio_value_series = portfolio_value_series+symbol_value_series

    portfolio_value_series = portfolio_value_series.dropna()
    return portfolio_value_series


def get_position_value_series(symbol, quantity, start_date=None, end_date=None, price_field='Adj Close'):
    """
    Generate a time-series of a single position's value assuming it was bought on start_date and held through end_date.
    :param symbol: (str)
    :param quantity: (float)
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :param price_field: (str)
    :return: (pd.Series)
    """

    if start_date is None:
        start_date = dt.datetime(year=2008, month=1, day=1)
    if end_date is None:
        end_date = dt.datetime.today()

    price_series = get_stock_data(symbol, start_date, end_date)[price_field]
    holdings = pd.Series(data=quantity, index=pd.date_range(start_date, end_date))
    position_value_series = (price_series*holdings).dropna()
    return position_value_series


def cum_returns(returns, starting_value=None):
    """
    Compute cumulative returns from simple (non-cumulative) returns.
    :param returns: (pd.Series) non-cumulative returns
    :param starting_value: (float) optional, default=1
    :return: (pd.Series)
    """
    if pd.isnull(returns.iloc[0]):
        returns.iloc[0] = 0.

    df_cum = np.exp(np.log(1 + returns).cumsum())

    if starting_value is None:
        return df_cum - 1

    return df_cum * starting_value


def one_dec_places(x):
    """
    1/10 decimal places for plot ticks.
    :param x:
    :param pos:
    :return:
    """
    return '%.1f' % x


def plot_rolling_returns(portfolio_id, portfolio, benchmark_returns=None,
                         legend_loc='best', volatility_match=False):
    """
    Plots cumulative rolling returns versus some benchmarks'.
    Portfolio simulated returns are in green, benchmark the gray line.

    :param portfolio_id: (int)
    :param portfolio: (dict) ticker:quantity
    :param benchmark_returns: (pd.Series) will load by default if None
    :param legend_loc: (matplotlib.loc) optional
    :param volatility_match: (bool) optional
    :return: (HttpResponse) of a png
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylabel('Cumulative returns')
    ax.set_xlabel('')

    returns = get_portfolio_returns_series(portfolio)
    if benchmark_returns is None:
        benchmark_returns = get_benchmark_returns('SPY')

    if volatility_match and benchmark_returns is None:
        raise ValueError('volatility_match requires passing of factor_returns.')
    elif volatility_match and benchmark_returns is not None:
        benchmark_vol = benchmark_returns.loc[returns.index].std()
        returns = (returns / returns.std()) * benchmark_vol

    cum_rets = cum_returns(returns, 1.0)

    y_axis_formatter = FuncFormatter(one_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))
    if benchmark_returns is not None:
        cum_factor_returns = cum_returns(
            benchmark_returns[cum_rets.index], 1.0)
        cum_factor_returns.plot(lw=2,
                                color='gray',
                                label='S&P 500 Benchmark Returns',
                                alpha=0.60,
                                ax=ax,)

    is_cum_returns = cum_rets

    is_cum_returns.plot(lw=3,
                        color='forestgreen',
                        alpha=0.6,
                        label='Portfolio {} Simulated Returns'.format(portfolio_id),
                        ax=ax, )

    if legend_loc is not None:
        ax.legend(loc=legend_loc)
    ax.axhline(1.0, linestyle='--', color='black', lw=2)

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
