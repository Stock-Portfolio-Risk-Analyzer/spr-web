import pandas as pd
import datetime as dt
# import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from functools import partial
from matplotlib import gridspec
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


def get_cum_returns(returns, starting_value=None):
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


def one_dec_places(x, pos):
    """
    1/10 decimal places for plot ticks.
    :param x:
    :param pos:
    :return:
    """
    return '%.1f' % x


def percentage(x, pos):
    """
    Adds percentage sign to plot ticks.
    :param x:
    :param pos:
    :return:
    """
    return '%.0f%%' % x


def basic_linear_regression(x, y):
    length = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x_squared = sum(map(lambda a: a * a, x))
    sum_of_products = sum([x[i] * y[i] for i in range(length)])
    a = (sum_of_products - (sum_x * sum_y) / length) / (sum_x_squared - ((sum_x ** 2) / length))
    b = (sum_y - a * sum_x) / length
    return a, b

def alpha_beta(returns, benchmark_returns):
    """
    Calculates alpha and beta.
    :param returns: (pd.Series) daily returns (non-cumulative)
    :param benchmark_returns:  (pd.Series) benchmark daily returns (non-cumulative) used to calculate beta
    :return: (float) alpha, (float) beta
    """
    ret_index = returns.index
    beta, alpha = basic_linear_regression(benchmark_returns.loc[ret_index].values, returns.values)[:2]
    return alpha * 21, beta


def aggregate_returns(daily_returns, convert_to):
    """
    Aggregates returns by week, month, or year.
    Parameters
    ----------
    daily_returns : pd.Series
       Daily returns of the strategy, noncumulative.
        - See full explanation in tears.create_full_tear_sheet (returns).
    convert_to : str
        Can be 'weekly', 'monthly', or 'yearly'.
    Returns
    -------
    pd.Series
        Aggregated returns.
    """

    def cumulate_returns(x):
        return get_cum_returns(x)[-1]

    if convert_to == 'weekly':
        return daily_returns.groupby(
            [lambda x: x.year,
             lambda x: x.isocalendar()[1]]).apply(cumulate_returns)
    elif convert_to == 'monthly':
        return daily_returns.groupby(
            [lambda x: x.year, lambda x: x.month]).apply(cumulate_returns)
    elif convert_to == 'yearly':
        return daily_returns.groupby(
            [lambda x: x.year]).apply(cumulate_returns)
    else:
        ValueError(
            'convert_to must be {}, {} or {}'.format('weekly', 'monthly', 'yearly')
        )


def plot_rolling_returns(portfolio_id, portfolio, ax, volatility_match=False):
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
    ax.set_ylabel('Cumulative returns')
    ax.set_xlabel('')

    returns = get_portfolio_returns_series(portfolio)

    benchmark_returns = get_benchmark_returns('SPY')

    if volatility_match and benchmark_returns is None:
        raise ValueError('volatility_match requires passing of factor_returns.')
    elif volatility_match and benchmark_returns is not None:
        benchmark_vol = benchmark_returns.loc[returns.index].std()
        returns = (returns / returns.std()) * benchmark_vol

    cum_returns = get_cum_returns(returns, 1.0)
    y_axis_formatter = FuncFormatter(one_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))
    if benchmark_returns is not None:
        cum_factor_returns = get_cum_returns(
            benchmark_returns[cum_returns.index], 1.0)
        cum_factor_returns.plot(lw=2,
                                color='gray',
                                label='S&P 500 Benchmark Returns',
                                alpha=0.60,
                                ax=ax,)

    is_cum_returns = cum_returns
    is_cum_returns.plot(lw=3,
                        color='forestgreen',
                        alpha=0.6,
                        label='Portfolio {} Simulated Returns'.format(portfolio_id),
                        ax=ax, )

    ax.legend(loc='best')
    ax.axhline(1.0, linestyle='--', color='black', lw=2)
    return ax


def rolling_beta(returns, benchmark_returns, rolling_window=21 * 6):
    """
    Calculates the rolling beta (given the rolling_window) of the portfolio simulation vs the benchmark_returns.
    :param returns: (pd.Series) noncumulative daily returns of portfolio
    :param benchmark_returns: (pd.Series) noncumulative daily returns of the benchmark
    :param rolling_window: (int) size of rolling window in days
    :return: (pd.Series) rolling beta
    See https://en.wikipedia.org/wiki/Beta_(finance) for more details.
    """
    if benchmark_returns.ndim > 1:
        return benchmark_returns.apply(partial(rolling_beta, returns), rolling_window=rolling_window)
    else:
        out = pd.Series(index=returns.index)
        for beg, end in zip(returns.index[0:-rolling_window], returns.index[rolling_window:]):
            out.loc[end] = alpha_beta(returns.loc[beg:end], benchmark_returns.loc[beg:end])[1]
        return out


def plot_rolling_beta(returns, benchmark_returns, ax):
    """
    Plots the rolling 6-month and 12-month beta versus date.
    :param returns: (pd.Series) noncumulative daily returns of portfolio
    :param benchmark_returns: (pd.Series) noncumulative daily returns of the benchmark
    :param ax: (matplotlib.Axes)
    :return:
    """
    if ax is None:
        ax = plt.gca()
    y_axis_formatter = FuncFormatter(one_dec_places)
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))
    ax.set_title("Rolling Portfolio Beta to S&P500 index")
    ax.set_ylabel('Beta')
    rb_1 = rolling_beta(returns, benchmark_returns, rolling_window=21 * 6)
    rb_1.plot(color='steelblue', lw=3, alpha=0.6, ax=ax)
    rb_2 = rolling_beta(returns, benchmark_returns, rolling_window=21 * 12)
    rb_2.plot(color='grey', lw=3, alpha=0.4, ax=ax)
    ax.set_ylim((-2.5, 2.5))
    ax.axhline(rb_1.mean(), color='steelblue', linestyle='--', lw=3)
    ax.axhline(0.0, color='black', linestyle='-', lw=2)
    ax.set_xlabel('')
    ax.legend(['6-mo rolling beta', '12-mo rolling beta'], loc='best')
    return ax


def get_max_drawdown_underwater(underwater):
    """
    Determine peak/valley/recover dates of underwater drawdown periods.
    :param underwater: (pd.DataFrame)
    :return: peak, valley, recovery
    """
    valley = np.argmax(underwater)  # end of the period
    peak = underwater[:valley][underwater[:valley] == 0].index[-1]
    try:
        recovery = underwater[valley:][underwater[valley:] == 0].index[0]
    except IndexError:
        recovery = np.nan
    return peak, valley, recovery


def get_top_drawdowns(returns, top=10):
    """
    Finds top drawdowns, sorted by drawdown amount.
    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in tears.create_full_tear_sheet.
    top : int, optional
        The amount of top drawdowns to find (default 10).
    Returns
    -------
    drawdowns : list
        List of drawdown peaks, valleys, and recoveries. See get_max_drawdown.
    """

    returns = returns.copy()
    df_cum = get_cum_returns(returns, 1.0)
    running_max = np.maximum.accumulate(df_cum)
    underwater = running_max - df_cum

    drawdowns = []
    for t in range(top):
        peak, valley, recovery = get_max_drawdown_underwater(underwater)
        # Slice out draw-down period
        if not pd.isnull(recovery):
            underwater.drop(underwater[peak: recovery].index[1:-1],
                            inplace=True)
        else:
            underwater = underwater.loc[:peak] # still in drawdown period

        drawdowns.append((peak, valley, recovery))
        if (len(returns) == 0) or (len(underwater) == 0):
            break

    return drawdowns


def gen_drawdown_table(returns, n_drawdown_periods=10):
    """
    Generates drawdown tables for the top n_drawdown_periods
    :param returns: (pd.Series) noncumulative daily returns
    :param n_drawdown_periods: (int) number of drawdown periods
    :return:
    """
    cum_returns = get_cum_returns(returns, 1.0)
    drawdown_periods = get_top_drawdowns(returns, top=n_drawdown_periods)
    df_drawdowns = pd.DataFrame(index=list(range(n_drawdown_periods)),columns=['net drawdown in %',
                                                                               'peak date',
                                                                               'valley date',
                                                                               'recovery date',
                                                                               'duration'])

    for i, (peak, valley, recovery) in enumerate(drawdown_periods):
        if pd.isnull(recovery):
            df_drawdowns.loc[i, 'duration'] = np.nan
        else:
            df_drawdowns.loc[i, 'duration'] = len(pd.date_range(peak, recovery, freq='B'))
        df_drawdowns.loc[i, 'peak date'] = (peak.to_pydatetime().strftime('%Y-%m-%d'))
        df_drawdowns.loc[i, 'valley date'] = (valley.to_pydatetime().strftime('%Y-%m-%d'))
        if isinstance(recovery, float):
            df_drawdowns.loc[i, 'recovery date'] = recovery
        else:
            df_drawdowns.loc[i, 'recovery date'] = (recovery.to_pydatetime().strftime('%Y-%m-%d'))
        df_drawdowns.loc[i, 'net drawdown in %'] = \
            ((cum_returns.loc[peak] - cum_returns.loc[valley]) / cum_returns.loc[peak]) * 100

    df_drawdowns['peak date'] = pd.to_datetime(df_drawdowns['peak date'], unit='D')
    df_drawdowns['valley date'] = pd.to_datetime(df_drawdowns['valley date'], unit='D')
    df_drawdowns['recovery date'] = pd.to_datetime(df_drawdowns['recovery date'], unit='D')

    return df_drawdowns


# def plot_drawdown_periods(returns, ax, n_drawdown_periods=10):
#     """
#     Plots cumulative returns and highlights top drawdown periods.
#     :param returns: (pd.Series)
#     :param n_drawdown_periods: (int) number of drawdown periods
#     :param ax: (matplotlib.Axes) axes to plot on
#     :return: (matplotlib.Axes) axes to plot on
#     """
#     y_axis_formatter = FuncFormatter(one_dec_places)
#     ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))
#     df_cum_rets = get_cum_returns(returns, starting_value=1.0)
#     df_drawdowns = gen_drawdown_table(returns, n_drawdown_periods=n_drawdown_periods)
#
#     df_cum_rets.plot(ax=ax)
#     lim = ax.get_ylim()
#     colors = sns.cubehelix_palette(len(df_drawdowns))[::-1]
#     for i, (peak, recovery) in df_drawdowns[['peak date', 'recovery date']].iterrows():
#         if pd.isnull(recovery):
#             recovery = returns.index[-1]
#         ax.fill_between((peak, recovery), lim[0], lim[1],
#                         alpha=.4,
#                         color=colors[i])
#
#     ax.set_title('Top %i Drawdown Periods' % n_drawdown_periods)
#     ax.set_ylabel('Cumulative returns')
#     ax.legend(['Portfolio'], loc='upper left')
#     ax.set_xlabel('')
#     return ax


# def plot_monthly_returns_heatmap(returns, ax):
#     """
#     Plots a heatmap of returns by month.
#     :param returns: (pd.Series)
#     :param ax: (matplotlib.Axes)
#     :return: (matplotlib.Axes)
#     """
#
#     monthly_ret_table = aggregate_returns(returns, 'monthly')
#     monthly_ret_table = monthly_ret_table.unstack().round(3)
#
#     sns.heatmap(monthly_ret_table.fillna(0) * 100.0,
#                 annot=True,
#                 annot_kws={"size": 9},
#                 alpha=1.0,
#                 center=0.0,
#                 cbar=False,
#                 cmap=matplotlib.cm.RdYlGn,
#                 ax=ax)
#     ax.set_ylabel('Year')
#     ax.set_xlabel('Month')
#     ax.set_title("Monthly Returns (%)")
#     return ax


def plot_annual_returns(returns, ax):
    """
    Plots a bar graph of returns by year.
    :param returns: (pd.Series)
    :param ax: (matploblib.Axes)
    :return: (matplotlib.Axes)
    """
    x_axis_formatter = FuncFormatter(percentage)
    ax.xaxis.set_major_formatter(FuncFormatter(x_axis_formatter))
    ax.tick_params(axis='x', which='major', labelsize=10)

    annual_returns = pd.DataFrame(aggregate_returns(returns, 'yearly'))
    ax.axvline(100 * annual_returns.values.mean(),
               color='steelblue',
               linestyle='--',
               lw=4,
               alpha=0.7)
    (100 * annual_returns.sort_index(ascending=False)).plot(ax=ax, kind='barh', alpha=0.70)
    ax.axvline(0.0, color='black', linestyle='-', lw=3)
    ax.set_ylabel('Year')
    ax.set_xlabel('Returns')
    ax.set_title("Annual Returns")
    ax.legend(['mean'])
    return ax


def plot_monthly_returns_dist(returns, ax):
    """
    Plots a distribution of monthly returns.
    :param returns: (pd.Series)
    :param ax: (matplotlib.Axes)
    :return: (matplotlib.Axes)
    """
    x_axis_formatter = FuncFormatter(percentage)
    ax.xaxis.set_major_formatter(FuncFormatter(x_axis_formatter))
    ax.tick_params(axis='x', which='major', labelsize=10)

    monthly_ret_table = aggregate_returns(returns, 'monthly')
    ax.hist(100 * monthly_ret_table,
            color='orangered',
            alpha=0.80,
            bins=20,)
    ax.axvline(100 * monthly_ret_table.mean(),
               color='gold',
               linestyle='--',
               lw=4,
               alpha=1.0)

    ax.axvline(0.0, color='black', linestyle='-', lw=3, alpha=0.75)
    ax.legend(['mean'])
    ax.set_ylabel('Number of months')
    ax.set_xlabel('Returns')
    ax.set_title("Distribution of Monthly Returns")
    return ax


def create_returns_tear_sheet(portfolio_id, portfolio, benchmark_rets=None):
    """
    Generate a number of plots for analyzing a portfolio simulation.
    :param portfolio_id:
    :param portfolio:
    :param benchmark_rets:
    :return: (HttpResponse)
    """

    returns = get_portfolio_returns_series(portfolio)
    if benchmark_rets is None:
        benchmark_rets = get_benchmark_returns('SPY')
        benchmark_rets.index = pd.DatetimeIndex([i.replace(tzinfo=None) for i in benchmark_rets.index])

    vertical_sections = 10
    fig = plt.figure(figsize=(14, vertical_sections * 6))
    gs = gridspec.GridSpec(vertical_sections, 3, wspace=0.5, hspace=0.5)
    ax_rolling_returns = plt.subplot(gs[:2, :])
    ax_rolling_returns_vol_match = plt.subplot(gs[2, :], sharex=ax_rolling_returns)
    ax_rolling_beta = plt.subplot(gs[3, :], sharex=ax_rolling_returns)
    ax_drawdown = plt.subplot(gs[4, :], sharex=ax_rolling_returns)
    ax_monthly_heatmap = plt.subplot(gs[5, 0])
    ax_annual_returns = plt.subplot(gs[5, 1])
    ax_monthly_dist = plt.subplot(gs[5, 2])

    # plots
    plot_rolling_returns(portfolio_id, portfolio, ax=ax_rolling_returns, volatility_match=False)
    ax_rolling_returns.set_title('Cumulative Returns')
    plot_rolling_returns(portfolio_id, portfolio, ax=ax_rolling_returns_vol_match, volatility_match=True)
    ax_rolling_returns_vol_match.set_title('Cumulative returns volatility matched to benchmark.')
    plot_rolling_beta(returns, benchmark_rets, ax=ax_rolling_beta)
    # plot_drawdown_periods(returns, ax=ax_drawdown, n_drawdown_periods=5)
    # plot_monthly_returns_heatmap(returns, ax=ax_monthly_heatmap)
    plot_annual_returns(returns, ax=ax_annual_returns)
    plot_monthly_returns_dist(returns, ax=ax_monthly_dist)

    for ax in fig.axes:
        plt.setp(ax.get_xticklabels(), visible=True)

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
