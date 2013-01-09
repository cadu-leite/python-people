# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, redirect, render, HttpResponse, HttpResponseRedirect

import urllib
import urllib2
from xml.dom.minidom import parseString

#from pagseguro.settings import *
from django.conf import settings

def pagseguro_transaction_code_request():
    '''
    faz a chamada a API de pagamento
    url api pagamento  = PAGSEGURO_API_URL = (default) =
    https://ws.pagseguro.uol.com.br/v2/checkout
    retorno: codigo de pagamento
    proximo: redirecionar o usuário para finalizar o pagamento
             https://pagseguro.uol.com.br/v2/checkout/payment.html?code=<CODDE>
    documentacao:
        https://pagseguro.uol.com.br/v2/guia-de-integracao/api-de-pagamentos.html#v2-item-api-de-pagamentos-direcionando-o-comprador

    exemplo retorno:
        <?xml version="1.0" encoding="ISO-8859-1"?>
        <checkout>
            <code>8CF4BE7DCECEF0F004A6DFA0A8243412</code>
            <date>2010-12-02T10:11:28.000-02:00</date>
        </checkout>

    retorno erros:
    <?xml version="1.0" encoding="UTF-8"?>
    <errors>
        <error>
            <code>11004</code>
            <message>Currency is required.</message>
        </error>
        <error>
            <code>11005</code>
            <message>Currency invalid value: 100</message>
        </error>
    </errors>
    '''

    PAYMENT_DATA = [("email", "xxxxxxxx@gmail.com"),
        ("token", settings.PAGSEGURO_API_TOKEN),
        ("currency", "BRL"),
        ("itemId1", "0001" ),
        ("itemDescription1", "Anuidade APYB"),
        ("itemAmount1", "5.00"),
        ("itemQuantity1", "1"),
        ("itemWeight1", "0"),
        ("reference", "1" ),
        # docs: https://pagseguro.uol.com.br/integracao/pagina-de-redirecionamento.jhtml
        ("redirectURL","http://pythonpeople.znc.com.br/pagseguro/checkout/return"), 
                        
        ]

    encoded_data=urllib.urlencode(PAYMENT_DATA)

    req=urllib2.Request(settings.PAGSEGURO_API_URL, encoded_data)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    #retorno=urllib2.urlopen(req).read()
    
    
    try:
        retorno=urllib2.urlopen(req)
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
            code = None 
            return code
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            code = None 
            return code 
    else:
        pagseguro_api_xml_response=retorno.read()
        #https://pagseguro.uol.com.br/v2/guia-de-integracao/api-de-pagamentos.html#v2-item-api-de-pagamentos-resposta
        dom = parseString(pagseguro_api_xml_response)
        code_tag = dom.getElementsByTagName('code')
        code =  code_tag[0].firstChild.data
        return code

def checkout(request):
    code  = pagseguro_transaction_code_request()
    
    #return redirect(reverse('python-group-detail', args=[0]))
    #return redirect('https://pagseguro.uol.com.br/v2/checkout/payment.html?code=4962B50F85853F3224030FB90DF194B1')
     #*********** #*********** #*********** #*********** #***********
    #***********   com redirect nao funca, com httpresponseredirect funfa!!! ARGH!!!!
    return HttpResponseRedirect('https://pagseguro.uol.com.br/v2/checkout/payment.html?code=%s'%(code))

def checkout_return(request, trans_code=None):
    '''
    retorno automatico apos a geracao do boleto
    http://www.pythonpeople.znc.com.br/pagamento/checkout/return?trans_code=xxxxxxxx-EA29-416B-A6C9-FC6588E7AC8C
    '''

    print request

    return  render(request, 'pagseguro/return.html', {'retorno':request})

def transaction_status(request, trans_code=None):
    '''
    retorno automatico de dados do pagseguro
    
    '''

    print request

    return  render(request, 'pagseguro/status.html', {'status':request})
