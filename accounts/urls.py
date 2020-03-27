from accounts import views
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy


app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'password-change/', 
        auth_views.PasswordChangeView.as_view(
                success_url=reverse_lazy('accounts:password_change_done')), 
        name='password-change'
    ),
    path('password-change/done/', 
        auth_views.PasswordChangeDoneView.as_view(), 
        name='password_change_done'
    ),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),

    path(
        'pwd-reset/', 
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('accounts:pwd_reset_done')), 
        name='password_reset'
    ),
    path('pwd-reset/done', 
        auth_views.PasswordResetDoneView.as_view(),
         name='pwd_reset_done'),
    path(
        'pwd-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('accounts:password_reset_complete')),
        name='password_reset_confirm'
    ),
    path(
        'pwd-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path('sendmail/', views.mail, name='sendmail'),
]
