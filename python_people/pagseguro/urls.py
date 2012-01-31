from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^checkout/$', 'pagseguro.views.checkout', name='pay-checkout'),
    url(r'^checkout_return/(?P<trans_code>([\w]-?)*)', 'pagseguro.views.checkout_return', name='pay-checkout_return'),
     
)
