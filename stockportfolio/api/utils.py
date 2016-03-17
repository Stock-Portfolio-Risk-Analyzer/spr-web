from datautils import rri as rri
from stockportfolio.api.models import Portfolio, Risk


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
