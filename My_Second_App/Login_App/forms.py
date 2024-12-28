from django import forms
from django.contrib.auth.forms import User
from .models import UserInfo


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password:','class':'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class UserInfoForm(forms.ModelForm):
    facebook_id = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta():
        model = UserInfo
        fields = ('facebook_id', 'profile_pic')
