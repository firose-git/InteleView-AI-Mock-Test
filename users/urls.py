# users/urls.py

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='user_login'),
    path('logout/', views.logout_view, name='user_logout'),
    path('register/', views.register, name='register'),
    path('verify-otp/<str:email>/', views.verify_otp, name='verify_otp'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),
    path('resend-otp/<str:email>/', views.resend_otp, name='resend_otp'),
    # users/urls.py
path('profile/', views.profile, name='profile'),
path('profile/edit/', views.edit_profile, name='edit_profile'),
path('settings/', views.settings_view, name='settings'),
path('delete-account/', views.delete_account, name='delete_account'),
path('send-delete-otp/', views.send_delete_otp, name='send_delete_otp'),


]
