# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm

def user_login_form (request):
    user_login_form = AuthenticationForm()

    return {'user_login_form':user_login_form }
