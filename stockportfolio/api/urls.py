from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^(?P<symbol>[A-Z]+)/$', views.ticker, name='ticker')
    url(r'^user/(\d+)', views.user_profile, name="user_profile")
]
