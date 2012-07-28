from django.conf.urls.defaults import patterns, include, url

from django.contrib.auth.views import login, logout
from django.contrib import admin

from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'people.views.home', name='home'),

    url(r'', include('social_auth.urls')),

    url(r'^people/', include('people.urls')),
    url(r'^pagseguro/', include('pagseguro.urls')),
    #url(r'^feedback/', include('djangovoice.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout, {"next_page": "/"}, name='logout'),
    url(r'^register/$', 'people.views.user_register', name='user-register'),
    url(r'^base.html/$', 'django.views.generic.simple.direct_to_template', {'template': 'base.html'}),
    url(r'^login/twitter$', 'people.views.login_twitter',  name='login_twitter'),

    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),

    (r'^password_change/$', 'django.contrib.auth.views.password_change'),
    (r'^password_change/done/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password-reset'),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),



)
