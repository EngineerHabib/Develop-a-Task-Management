from django.contrib.auth.models import User
from TaskManager.models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['user', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
