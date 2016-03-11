from django.conf.urls import url

from . import views
from . import api
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<symbol>[A-Z]+)/$', views.ticker, name='ticker'),
    url(r'^user/(\d+)$', views.user_profile, name="user_profile"),
    url(r'^api/portfolio/(\d+)/addstock(?P<stock>\w+)$', api.add_stock, name="add_stock"),
    url(r'^api/portfolio/(\d+)/removestock(?P<stock>\w+)$', api.remove_stock, name="remove_stock"),
    url(r'^api/portfolio/create(?P<user_id>\w+)$', api.create_portfolio, name="create_portfolio"),
    url(r'^api/portfolio/(\d+)/delete$', api.delete_portfolio, name="delete_portfolio"),
    url(r'^api/portfolio/(\d+)$', api.get_portfolio, name="get_portfolio")
]
