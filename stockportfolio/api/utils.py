from datautils import rri as rri
from stockportfolio.api.models import Portfolio, Risk, PortfolioRank
from scipy.stats import rankdata


def update_rri_for_all_portfolios():
    for portfolio in Portfolio.objects.all():
        stocks = portfolio.portfolio_stocks.all()
        if not stocks:
            continue
        risk = Risk(
            risk_value=rri.compute_portfolio_rri_for_today(stocks, 10))
        risk.save()
        portfolio.portfolio_risk.add(risk)
        portfolio.save()


def update_rank_for_all_portfolios():
    risks = []
    for portfolio in Portfolio.objects.all():
        risk_object = portfolio.portfolio_risk.order_by('-risk_date').first()
        if not risk_object:
            risk = 0
        else:
            risk = risk_object.risk_value
        risks.append((portfolio.portfolio_id, risk))
    risk_values = zip(*risks)[1]
    rank_values = len(risk_values) - rankdata(risk_values,
                                              method='ordinal') + 1
    ranks = zip(zip(*risks)[0], rank_values)
    for portfolio_id, rank in ranks:
        portfolio = Portfolio.objects.get(portfolio_id=portfolio_id)
        rank = PortfolioRank(value=rank, portfolio=portfolio)
        rank.save()
