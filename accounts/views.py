from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from accounts.forms import LoginForm


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