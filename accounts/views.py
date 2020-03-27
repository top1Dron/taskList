from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import LoginForm, RegistrationForm, UserEditForm, ProfileEditForm
from accounts.models import Profile

from django.core.mail import send_mail
from django.conf import settings


class LoginView(View):
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
            return HttpResponse('Welcome! The enter is successful')

        return render(request, 'accounts/login.html', {'form': form})


    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


def register(request):
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


@login_required
def mail(request):
    suject = 'Try to send'
    msg = 'Success sending mail'
    to = request.user.email
    res = send_mail(subject, msg, settings.SERVER_EMAIL)
    if res == 1:
        msg = 'Mail sent successfully'
    else:
        msg = 'Mail could not sent'
    return HttpResponse(msg)