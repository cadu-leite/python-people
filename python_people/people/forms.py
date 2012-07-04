# -*- coding: utf-8 -*-

from django.contrib.gis import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from django.utils.translation import ugettext_lazy as _
from people.models import UserProfile,  PythonGroup


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
