#! /usr/bin/env python
# _*_ coding:utf-8 _*_

from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password = forms.CharField(label="Password", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password"}))
    

class RegisterForm(forms.Form):
    gender=(
        ('male','男'),
        ('female','女'),
    )
    username = forms.CharField(label="Username", max_length=128,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Ensure password", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="email",
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    realname = forms.CharField(label="realname",
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_id_number = forms.IntegerField(label="user_id_number",
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_phone = forms.IntegerField(label="user_phone",
                            widget=forms.TextInput(attrs={'class': 'form-control'}))