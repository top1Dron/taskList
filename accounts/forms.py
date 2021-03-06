from accounts.models import Profile
from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """Form for login user"""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    """Form for user registration on the site"""

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password do not match')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    """Form for edit user info"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """Form to edit user profile info"""
    class Meta:
        model = Profile
        fields = ('birthdate', 'API_KEY', 'API_SECRET')