import stockportfolio.api.views as views
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^api/', include('stockportfolio.api.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
	url(r'^accounts/password/change/$', 
        'django.contrib.auth.views.password_change', 
        {'post_reset_redirect' : '/accounts/password/change/done/',
        'template_name' : 'registration/password_change_form.html'}),
	url(r'^accounts/password/change/done/$', 
    	'django.contrib.auth.views.password_change_done', 
        {'template_name' : 'registration/password_change_done.html'})
	]
