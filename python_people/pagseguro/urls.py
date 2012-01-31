from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^checkout/$', 'pagseguro.views.checkout', name='pay-checkout'),
    #http://pythonpeople.znc.com.br/pagseguro/checkout/return
    url(r'^checkout/return/(?P<trans_code>([\w]-?)*)', 'pagseguro.views.checkout_return', name='pay-checkout_return'),
    #http://pythonpeople.znc.com.br/pagseguro/status/
    url(r'^transaction/status/(?P<trans_code>([\w]-?)*)', 'pagseguro.views.transaction_status', name='pay-status'),
     
)
