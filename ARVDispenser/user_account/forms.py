from django import forms
from django.contrib.auth.forms import (UserCreationForm,AuthenticationForm)

class LoginForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder':'User Name','class':'form-control',
        'autofocus':'true'}))
    password=forms.CharField(widget=forms.PasswordInput(render_value=False,
        attrs={'placeholder':'Password','class':'form-control'}))

class RegistrationForm(UserCreationForm):
	def __init__(self,*args,**kwargs):
		super(RegistrationForm, self).__init__(*args,**kwargs)