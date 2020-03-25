from django.contrib.auth import views as auth_views
from django.urls import path

from accounts import views


urlpatterns = [
    # path('login/', views.LoginView.as_view(), name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
