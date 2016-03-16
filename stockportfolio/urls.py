import stockportfolio.api.views as views
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^modify_account/(?P<username>\w+)/$', views.modify_account, name='modify_account'),
    url(r'^api/', include('stockportfolio.api.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls'))
]
