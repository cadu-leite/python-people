# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, redirect, render,redirect, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.gis.shortcuts import render_to_kml
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.utils import simplejson  as json
from django.core import serializers

from django.contrib.gis.db.models import *
from people.forms import UserProfileForm, UserRegisterForm, PythonGroupForm
from people.models import UserProfile, PythonFrameWorks, PythonGroup

from django.contrib.gis.geos import Polygon

import datetime as DateTime
def gender_count():
    q = list( UserProfile.objects.values( 'gender' ).annotate( Count('gender') ) )
    
    l = [[( ),i['gender__count']] for i in q ]
    l = [];    d = {}
    opts = {1:'male',2:'female',3:'other'}
    opts_color = {1:'#000897',2:'#CF0098',3:'#7C6700'}
    for i in q:
        if  ( i['gender__count'] != None) and  ( i['gender'] != None ):
            l.append([opts.get( i['gender']),i['gender__count']])
    return ( l)

def frameworks_count():
    q = list( PythonFrameWorks.objects.values().annotate( Count('userprofile') ) )
    l = [];    d = {}
    l = [[i['name'],i['userprofile__count']] for i in q ]

    return ( l)
     

def people_by_country():
    by_country  = UserProfile.objects.values('country').annotate(qtd = Count('id'))
    l = [[i['country'],i['qtd']] for i in by_country ]
    return (l )

def points(request):
    points = UserProfile.objects.kml()
    return render_to_kml("placemarks.kml", {'points' : points})
    
 
def home(request):
    pus = UserProfile.objects.filter(~Q(point=None))
    pygs = PythonGroup.objects.filter(~Q(point=None))
    pygs = pygs.order_by('-date_add')[:10]
    users= User.objects.all().order_by('-date_joined')[:10]
    #str_json = ups.geojson().values('user_id','name', 'gender','point')
    dpyu = [ { 'user_id':pu.id, 'name':pu.name, 'gender':pu.gender, 'x':pu.point.x, 'y': pu.point.y } for pu in pus ]
    dpygs = [ { 'pyg_id':pyg.id, 'name':pyg.name, 'description':pyg.description, 'x':pyg.point.x, 'y': pyg.point.y } for pyg in pygs ]
    
    return render(request,'home.html', {
        'pjson':json.dumps(dpyu), 
        'pygsjson':json.dumps(dpygs), 
        'users':users,'pygs':pygs[:10], 
        'gender_count':gender_count(), 
        'frameworks_count': json.dumps(frameworks_count()),
        'by_country' :json.dumps(list(people_by_country())),
        'people_total': User.objects.count(),
        })

class CreateWMsgView(CreateView):
    message=u''
    message_level = messages.INFO
    def form_valid(self, form):
        messages.add_message(self.request,self.message_level, self.message)
        return super(CreateWMsgView, self).form_valid(form)

def user_register(request, pk=None):
    view_kwargs = {
        'model': User, 
        'form_class': UserRegisterForm,
        'template_name': "people/register_form.html",
        'message':u'Your account has been created ! Sig in to fullfill your profile.',
        'message_level':messages.INFO,
    }

    if pk is None:
        view_kwargs['success_url'] = "/login/"
        return CreateWMsgView.as_view(**view_kwargs)(request)
    else:
        return UpdateView.as_view(**view_kwargs)(request, pk=pk)

def user_profile_upd(request):
    view_kwargs = {
        'model': UserProfile, 
        'form_class': UserProfileForm,
        #'success_url': "/adm/userprofile/%(id)d/",
        'success_url':  reverse('user-profile',   args=[request.user.get_profile().id] ),
        'template_name': "/people/userprofile_form.html",
    }
    
    user_profile, created = UserProfile.objects.get_or_create(user_id=request.user)
    
    if request.method == "POST":
        if user_profile.user.last_login.strftime("%d%m%Y%H%M%S") == user_profile.user.date_joined.strftime("%d%m%Y%H%M%S"):
            msg = u"Usuário registrado com sucesso!<br />Efetue o login no site."
            view_kwargs['success_url'] = settings.LOGIN_URL
        else:
            msg = u'Seus dados de perfil foram salvos.'
        messages.add_message(request, messages.INFO, msg)
    return UpdateView.as_view(**view_kwargs)(request, pk=user_profile.pk)  

def python_users_bounded(request, *args):
    
    pyus = UserProfile.objects.filter(point__contained = Polygon.from_bbox(args)).order_by('name')
    pyus.filter( ~Q(point=None))
    
    dpyu = [{ 'name':pyu.name, 'gender':pyu.gender, 'x':pyu.point.x, 'y': pyu.point.y, 'user_id':pyu.user_id } for pyu in pyus ]
    return HttpResponse(json.dumps(dpyu), 'json')
    

def python_group_list(request):
    return redirect(request)

class PythonGroupCreateView(CreateView):
    form_class = PythonGroupForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PythonGroupCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()        
        #return redirect(self.success_url)
        return redirect(reverse('python-group-detail', args=[obj.pk])) 
 
def python_group_crud(request, pk=None):
    view_kwargs = {
        'model': PythonGroup, 
        'form_class': PythonGroupForm,
        'template_name': "people/pythongroup_form.html",
    }
    
    if pk is None:
        view_kwargs['success_url'] = "/pythongroup/list/"
        return PythonGroupCreateView.as_view(**view_kwargs)(request)
    else:
        return UpdateView.as_view(**view_kwargs)(request, pk=pk)
    