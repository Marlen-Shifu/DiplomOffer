from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *


class UserAuthenticationForm(AuthenticationForm):

	class Meta:
		fields = ['username', 'password']


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'phone_number')

