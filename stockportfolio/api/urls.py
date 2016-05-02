"""
This is the URL module.

"""

from django.conf.urls import url

from stockportfolio.api import api, views

urlpatterns = [
    url(r'^(?P<symbol>[A-Z]+)/$', views.ticker, name='ticker'),
    url(
        r'^name/(?P<symbol>[A-Z]+)/$',
        views.company_name, name='company_name'),
    url(
        r'^user/(?P<portfolio_id>\d+)$',
        views.user_profile, name="user_profile"),
    url(
        r'^user/(?P<user_id>\d+)/getportfolio$',
        api.get_portfolio_by_user, name="get_portfolio_by_user"),
    url(
        r'^user/(?P<user_id>\d+)/getportfoliolist$',
        api.get_list_of_portfolios, name="get_portfolio_list_by_user"),
    url(
        r'^portfolio/(?P<portfolio_id>\d+)/addstock$',
        api.add_stock, name="add_stock"),
    url(
        r'^portfolio/(?P<portfolio_id>\d+)/removestock$',
        api.remove_stock, name="remove_stock"),
    url(
        r'^portfolio/create/(?P<user_id>\w+)$',
        api.create_portfolio, name="create_portfolio"),
    url(
        r'^portfolio/(?P<portfolio_id>\d+)/delete$',
        api.delete_portfolio, name="delete_portfolio"),
    url(
        r'^portfolio/(?P<portfolio_id>\d+)$',
        api.get_portfolio, name="get_portfolio"),
    url(
        r'^modify_account/$', views.modify_account, name='modify_account'),
    url(
        r'^portfolio/(?P<portfolio_id>\d+)/modify$',
        api.modify_portfolio_form_post, name="modify_portfolio_form_post"),
    url(
        r'^portfolio/(?P<portfolio_id>\d+)/modify_gen$',
        api.modify_gen, name="modify_gen"),
    url(
        r'^portfolio/(?P<portfolio_id>\d+)/download$',
        api.download_porfolio_data, name="download_portfolio_data"),
    url(
        r'^portfolio/upload',
        api.upload_portfolio_data, name="upload_portfolio_data"),
    url(
        r'^utils/calculate-rri/$',
        views.calculate_all_rris, name='utils_calculate_rri'),
    url(
        r'^(?P<ticker>[\w\+.,! ]+)/details',
        views.stock_interface, name='stock_interface'),
    url(
        r'^top-ten/(?P<category>\d+)$',
        api.list_top_portfolios, name='top_portfolios'),
    url(
        r'^top-ten/portfolio/(?P<portfolio_id>\d+)$',
        api.get_public_portfolio, name='get_public_portfolio'),
    url(
        r'^portfolio/(?P<portfolio_id>\d+)/simulateportfolio',
        views.simulate_portfolio, name="simulate_portfolio"),
    url(
        r'^portfolio/(?P<portfolio_id>\d+)/(?P<rec_type>\w+)/recommendation$',
        views.stock_rec, name="stock_rec"),
    url(
        r'^portfolio/generate_portfolio$',
        views.generate_portfolio, name="generate_portfolio")
]
