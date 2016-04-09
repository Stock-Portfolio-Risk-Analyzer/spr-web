from django.conf.urls import url

from . import views
from . import api
urlpatterns = [
    url(r'^(?P<symbol>[A-Z]+)/$', views.ticker, name='ticker'),
    url(r'^user/(?P<portfolio_id>\d+)$', views.user_profile, name="user_profile"),
    url(r'^user/(?P<user_id>\d+)/getportfolio$', api.get_portfolio_by_user, name="get_portfolio_by_user"),
    url(r'^user/(?P<user_id>\d+)/getportfoliolist$', api.get_list_of_portfolios, name="get_portfolio_list_by_user"),
    url(r'^portfolio/(?P<portfolio_id>\d+)/addstock$', api.add_stock, name="add_stock"),
    url(r'^portfolio/(?P<portfolio_id>\d+)/removestock$', api.remove_stock, name="remove_stock"),
    url(r'^portfolio/create/(?P<user_id>\w+)$', api.create_portfolio, name="create_portfolio"),
    url(r'^portfolio/(?P<portfolio_id>\d+)/delete$', api.delete_portfolio, name="delete_portfolio"),
    url(r'^portfolio/(?P<portfolio_id>\d+)$', api.get_portfolio, name="get_portfolio"),
    url(r'^modify_account/$', views.modify_account, name='modify_account'),
    url(r'^portfolio/(?P<portfolio_id>\d+)/modify$', api.modify_portfolio_form_post, name="modify_portfolio_form_post"),
    url(r'^utils/calculate-rri/$', views.calculate_all_rris, name='utils_calculate_rri'),
    url(r'^portfolio/(?P<portfolio_id>\d+)/stock_rec$', api.stock_rec, name="stock_rec")
]
