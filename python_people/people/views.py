# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.conf import settings

from django.utils.decorators import method_decorator
from django.utils import simplejson  as json

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.gis.shortcuts import render_to_kml
from django.contrib.gis.db.models import *
from django.contrib.gis.geos import Polygon
from django.contrib import messages

from django.shortcuts import render, redirect, HttpResponse

from django.views.generic import ListView, CreateView, UpdateView

from people.forms import UserProfileForm, ProfileSearchForm, UserRegisterForm, PythonGroupForm, GroupSearchForm, SurveySearchForm, SurveyForm
from people.models import UserProfile, PythonFrameWorks, PythonGroup, Survey


def gender_count():
    profiles = list(UserProfile.objects.values('gender').annotate(Count('gender')))
    l = list()
    opts = {1: 'male', 2: 'female', 3: 'other'}
    for i in profiles:
        if (i['gender__count'] != None) and (i['gender'] != None):
            l.append([opts.get(i['gender']), i['gender__count']])
    return (l)


def frameworks_count():
    q = list(PythonFrameWorks.objects.values().annotate(Count('userprofile')))
    l = list()
    l = [[i['name'], i['userprofile__count']] for i in q]
    return (l)


def people_by_country():
    by_country = UserProfile.objects.values('country').annotate(qtd=Count('id')).order_by('-qtd')[:10]
    l = [[i['country'], i['qtd']] for i in by_country]
    return (l)


def points(request):
    points = UserProfile.objects.kml()
    return render_to_kml("placemarks.kml", {'points': points})


def home(request):
    pus = UserProfile.objects.filter(~Q(point=None))
    pygs = PythonGroup.objects.filter(~Q(point=None))
    pygs = pygs.order_by('-date_add')[:10]
    users = User.objects.all().order_by('-date_joined')[:10]
    #str_json = ups.geojson().values('user_id','name', 'gender','point')
    dpyu = [{'user_id':pu.id, 'name':pu.name, 'gender':pu.gender, 'x':pu.point.x, 'y': pu.point.y} for pu in pus]
    dpygs = [{'pyg_id':pyg.id, 'name':pyg.name, 'description':pyg.description, 'x':pyg.point.x, 'y': pyg.point.y} for pyg in pygs]

    return render(request, 'home.html', {
        'pjson': json.dumps(dpyu),
        'pygsjson': json.dumps(dpygs),
        'users': users,
        'pygs': pygs[:10],
        'gender_count': gender_count(),
        'frameworks_count': json.dumps(frameworks_count()),
        'by_country': json.dumps(list(people_by_country())),
        'people_total': User.objects.count(),
        })


def login_twitter(request):
    '''
    callback view from twitter
    '''
    return redirect(reverse('user-profile-form'))


class CreateWMsgView(CreateView):
    message = u''
    message_level = messages.INFO

    def form_valid(self, form):
        messages.add_message(self.request, self.message_level, self.message)
        return super(CreateWMsgView, self).form_valid(form)


def user_register(request, pk=None):
    view_kwargs = {
        'model': User,
        'form_class': UserRegisterForm,
        'template_name': "people/register_form.html",
        'message': u'Your account has been created ! Sig in to fullfill your profile.',
        'message_level': messages.INFO,
    }

    if pk is None:
        view_kwargs['success_url'] = "/login/"
        return CreateWMsgView.as_view(**view_kwargs)(request)
    else:
        return UpdateView.as_view(**view_kwargs)(request, pk=pk)


def user_profile_crud(request):
    python_groups = None
    if request.user.is_authenticated():

        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.name = profile.name or request.user.first_name

        form = UserProfileForm(request.POST or None, instance=profile)

        python_groups = profile.user.pythongroup_set.all()

        if request.POST:
            if form.is_valid():
                form.save()
    else:
        form = None
        messages.add_message(request, messages.INFO, 'You may sign in to update your profile.')
    return render(request,
        "people/userprofile_form.html",
        {'form': form,
        'python_groups': python_groups},
        )


def python_group_crud(request, pk=None):

    try:
        group = PythonGroup.objects.get(pk=pk)
        if not group.is_group_owner(request.user):
            group = None
            messages.add_message(request, messages.INFO, 'You cannot update this python user group.')
            return redirect(reverse('python-group-list'))
    except:
        group = None

    form = PythonGroupForm(request.POST or None, instance=group, user=request.user)

    if request.POST:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'The group data was sucessfully updated')
            return redirect(reverse('python-group-detail', args=[group.pk]))
        else:
            messages.add_message(request, messages.ERROR, 'There are erros in your request. Please check the messages below.')
    return render(request,
        "people/pythongroup_form.html",
        {'form': form},
        )


def python_users_bounded(request, *args):

    pyus = UserProfile.objects.filter(point__contained=Polygon.from_bbox(args)).order_by('name')
    pyus.filter(~Q(point=None))

    dpyu = [{'name': pyu.name, 'gender': pyu.gender, 'x': pyu.point.x, 'y': pyu.point.y, 'user_id':pyu.user_id} for pyu in pyus]
    return HttpResponse(json.dumps(dpyu), 'json')


class SearchListView(ListView):
    form_class = None

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        context['frm_srch'] = self.get_form()
        qs_data = context['frm_srch'].data
        context['query_string'] = ''
        if qs_data:
            qs_data.pop('page', '1')
            context['query_string'] = qs_data.urlencode()

        return context

    def get_queryset(self):
        if self.form_class is None:
            return super(SearchListView, self).get_queryset()
        return self.get_form().get_queryset()

    def get_form(self):
        #if not hasattr(self, '_inst_form'):
        #   setattr(self, '_inst_form', self.form_class(self.request.GET.copy() or None))
        #return self._inst_form
        return self.form_class(self.request.GET.copy() or None)


class ProfileListView(SearchListView):
    form_class = ProfileSearchForm
    paginate_by = 20

profile_list = ProfileListView.as_view()


class GroupListView(SearchListView):
    form_class = GroupSearchForm
    paginate_by = 20

group_list = GroupListView.as_view()


def survey_crud(request, pk=None):

    try:
        survey = Survey.objects.get(pk=pk)
        if not group.is_group_owner(request.user):
            group = None
            messages.add_message(request, messages.INFO, 'You cannot update this python user group.')
            return redirect(reverse('python-group-list'))
    except:
        survey = None

    form = SurveyForm(request.POST or None, instance=survey, user=request.user)

    if request.POST:
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'The survey was sucessfully updated')
            return redirect(reverse('python-survey-detail', args=[group.pk]))
        else:
            messages.add_message(request, messages.ERROR, 'There are erros in your request. Please check the messages below.')
    return render(request,
        "people/survey_form.html",
        {'form': form},
        )


class SurveyListView(SearchListView):
    form_class = SurveySearchForm
    paginate_by = 20

survey_list = SurveyListView.as_view()

