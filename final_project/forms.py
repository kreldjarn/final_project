from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SkraningarForm(UserCreationForm):
	email = forms.EmailField(required=True)

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