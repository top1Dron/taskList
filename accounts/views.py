# from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import LoginForm, RegistrationForm, UserEditForm, ProfileEditForm
from accounts.models import Profile

# from taskList import settings


class LoginView(View):
    """View for sign in user. Includes get request, which shows
    login form page, and post request, which checked input data in form"""

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            cleanedData = form.cleaned_data
            user = authenticate(
                request,
                username = cleanedData['username'],
                password = cleanedData['password']
            )
            if user is None:
                return HttpResponse('Wrong login and/or password')

            if not user.is_active:
                return HttpResponse('Your account is forbidden')

            login(request, user)
            return HttpResponse('Welcome! Authenticated successful')

        return render(request, 'accounts/login.html', {'form': form})


    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


def register(request):
    """view for sign ip new user"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)

            return render(request, 'accounts/registration_complete.html', {'new_user': new_user})
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'user_form': form})


@login_required
def edit(request):
    """view for editing user profile data. Includes fields from User and Profile tables"""
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(request.POST, instance=request.user.profile, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('tasks:list')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        'accounts/edit.html',
        {'user_form': user_form, 'profile_form': profile_form, 'request': request.user},
    )