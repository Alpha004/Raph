from django.contrib.auth.models import User
from django.forms import ModelForm, CheckboxInput
from django.contrib.auth.forms import UserCreationForm


__author__ = 'Jesus'

from django import forms

class Login(UserCreationForm):
    class Meta:
        model = User
        fields = {'username','password'}
        # Username = forms.CharField(label='Usuario:', max_length=10)
        # Password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(Login, self).__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs.update({'class': 'form-control'})
        # self.fields['password'].widget.attrs.update({'class': 'form-control'})

class CreateUser(ModelForm):
    class Meta:
        model = User
        fields = {'username','password','first_name','last_name','email','is_superuser'}
        widgets = {'is_superuser': CheckboxInput}
        help_texts = {
            'username':None
        }