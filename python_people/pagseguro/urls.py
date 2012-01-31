from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^checkout/$', 'payment.views.checkout', name='pay-checkout'),
    url(r'^checkout_return/$', 'payment.views.checkout_return', name='pay-checkout_return'),
     
)
