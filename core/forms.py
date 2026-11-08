from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Chore, Member

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class ChoreForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ["household", "assigned_member", "title", "description", "category", "priority", "points", "due_date",]

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["user", "household", "role", "display_name", "avatar_colour"]