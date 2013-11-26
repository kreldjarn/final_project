# -*- coding: utf-8 -*- 
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SkraningarForm(UserCreationForm):
	email = forms.EmailField(required=True, max_length=45, label="", widget=forms.TextInput(attrs={'placeholder': 'Netfang'}))
	username = forms.RegexField(required=True, max_length=30,
        regex=r'^[\w.@+-]+$', label="", widget=forms.TextInput(attrs={'placeholder': 'Notandanafn', 'autofocus': 'true'}))
	password1 = forms.CharField(required=True, max_length=45, label=(""),
        widget=forms.PasswordInput(attrs={'placeholder': 'Lykilorð'}))
	password2 = forms.CharField(required=True, max_length=45, label=(""),
        widget=forms.PasswordInput(attrs={'placeholder': 'Lykilorð endurtekið'}))

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')
    
    # Automatically saved, unless otherwise specified in the call
	def save(self, commit=True):
		user = super(SkraningarForm, self).save(commit=False)
		user.email = self.cleaned_data['email']

		if commit:
			user.save()
		return user