from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'unique': 'A user with that email address already exists.',
            'invalid': 'Enter a valid email address.',
        }
    )

    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'unique': 'A user with that username already exists.',
            'invalid': 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.',
        }
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ('email','username',  'password1', 'password2')


# class LoginForm(AuthenticationForm):
#     username = forms.CharField(
#         widget=forms.TextInput(attrs={'class':'form-control'}),
#         label = 'Username or Email'
#     )
    
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         label = 'Password'
#     )