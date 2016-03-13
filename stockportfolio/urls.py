import stockportfolio.api.views
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', stockportfolio.api.views.index, name='index'),
    url(r'^api/', include('stockportfolio.api.urls')), 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls'))
]
