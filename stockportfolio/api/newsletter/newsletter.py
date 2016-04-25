import os
import time
from django.contrib.auth.models import User
import sendgrid
from stockportfolio.api.datautils.yahoo_finance import get_current_price


def send_emails():
    subscribers = User.objects.all()
    key = os.environ.get('SENDGRID_API_KEY')
    if key is None:
        return
    sg = sendgrid.SendGridClient(key, raise_errors=True)
    message = sendgrid.Mail()
    risk = []
    rank = []
    value = []
    p_name = []
    usernames = []
    for sub in subscribers:
        user_settings = sub.usersettings
        if user_settings.default_portfolio:
            portfolio = user_settings.default_portfolio
        else:
            portfolio = sub.portfolio_set.all().first()
        if portfolio is None:
            continue
        if sub.email is None or sub.email == '':
            continue
        usernames.append(sub.username)
        risk.append(round(portfolio.portfolio_risk.order_by('-risk_date').first().risk_value,3))
        rank.append(portfolio.portfoliorank_set.order_by('-date').first().value)
        p_value = 0
        for stock in portfolio.portfolio_stocks.all():
            current_price = get_current_price(stock.stock.stock_ticker)
            p_value += current_price*stock.quantity
        value.append(p_value)
        p_name.append(portfolio.portfolio_name)
        message.add_to(sub.email)

    message.set_substitutions({'-firstname-': usernames, '-pname-': p_name, '-pvalue-': value, '-prisk-': risk, '-prank-': rank})
    message.set_from('SPR Web <eespaillat94@gmail.com>')
    message.set_subject('Weekly Update')
    message.set_html('Body')
    message.set_text('Body')
    message.add_filter('templates', 'enable', '1')
    message.add_filter('templates', 'template_id', '4d48cfbe-750f-4b30-b0d1-5b907e3e730b')
    status, msg = sg.send(message)







