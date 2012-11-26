# -*- coding: utf-8 -*-

from django.contrib.gis import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from people.models import UserProfile,  PythonGroup, Survey


class UserRegisterForm(UserCreationForm):
    username = forms.EmailField(label="e-mail", max_length=64, help_text="e-mail as username")
    forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["username"]

        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user')
        widgets = {
                 'point': forms.HiddenInput(),
                 'python_frameworks': forms.CheckboxSelectMultiple(),
                 }


class PythonGroupForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        self.user = kargs.pop('user', None)
        self.commit = kargs.pop('commit', True)
        super(PythonGroupForm, self).__init__(*args, **kargs)

    def save(self, *args, **kargs):
        if self.instance.pk:
            if not self.instance.is_group_owner(self.user):
                raise forms.ValidationError("the request user is not the group owner")

        self.instance.user = self.user
        return super(PythonGroupForm, self).save(*args, **kargs)

    class Meta:
        model = PythonGroup
        exclude = ('user')
        widgets = {
                 'point': forms.HiddenInput(),
                 'date_add': forms.HiddenInput(),
                 'date_upd': forms.HiddenInput(),
                 }


class ProfileSearchForm(forms.Form):
    search_text = forms.CharField(required=False)

    def get_queryset(self):
        object_list = UserProfile.objects.all()
        if self.is_valid():
            if self.cleaned_data['search_text']:
                object_list = object_list.filter(name__icontains=self.cleaned_data['search_text'])

        return object_list


class GroupSearchForm(forms.Form):
    search_text = forms.CharField(required=False)

    def get_queryset(self):
        object_list = PythonGroup.objects.all()
        if self.is_valid():
            if self.cleaned_data['search_text']:
                search_text = self.cleaned_data['search_text']
                filter = Q(name__icontains=search_text) | Q(description__icontains=search_text) | Q(locality__icontains=search_text)
                object_list = object_list.filter(filter)

        return object_list


class SurveyForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        self.user = kargs.pop('user', None)
        self.commit = kargs.pop('commit', True)
        super(SurveyForm, self).__init__(*args, **kargs)

    def save(self, *args, **kargs):
        if self.instance.pk:
            if not self.instance.is_group_owner(self.user):
                raise forms.ValidationError("the request user is not the survey owner")

        self.instance.user = self.user
        return super(SurveyForm, self).save(*args, **kargs)

    class Meta:
        model = Survey
        exclude = ('user')
        widgets = {
                 'date_add': forms.HiddenInput(),
                 }


class SurveySearchForm(forms.Form):
    search_text = forms.CharField(required=False)

    def get_queryset(self):
        object_list = Survey.objects.all()

        return object_list
