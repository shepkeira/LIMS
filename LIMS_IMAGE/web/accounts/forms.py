from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Client

class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class clientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('company_name', 'contact_person', 'phone_number', 'address', )